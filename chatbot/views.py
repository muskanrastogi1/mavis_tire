from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rule, Message
from .services import LLMService
import json

def home(request):
    return render(request, 'chatbot/home.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').lower().strip()
            
            # Get relevant responses based on keywords in the user's message
            potential_responses = []
            
            # Common variations of general words
            greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
            help_words = ['help', 'assist', 'support', 'guide', 'how to', 'what can you do']
            thanks_words = ['thanks', 'thank you', 'appreciate', 'grateful']
            goodbye_words = ['bye', 'goodbye', 'see you', 'exit', 'quit', 'end']
            
            # Check for general responses first
            if any(word in user_message for word in greetings):
                general_rules = Rule.objects.filter(pattern__in=['hello', 'hi'])
                potential_responses.extend(general_rules.values_list('response', flat=True))
            
            elif any(word in user_message for word in help_words):
                general_rules = Rule.objects.filter(pattern='help')
                potential_responses.extend(general_rules.values_list('response', flat=True))
            
            elif any(word in user_message for word in thanks_words):
                general_rules = Rule.objects.filter(pattern='thanks')
                potential_responses.extend(general_rules.values_list('response', flat=True))
            
            elif any(word in user_message for word in goodbye_words):
                general_rules = Rule.objects.filter(pattern__in=['bye', 'goodbye', 'see you', 'exit'])
                potential_responses.extend(general_rules.values_list('response', flat=True))
            
            # If no general matches, check for specific queries
            if not potential_responses:
                # Check for vehicle-related queries
                if any(word in user_message for word in ['tire', 'specification', 'car', 'vehicle', 'make', 'model']):
                    vehicle_rules = Rule.objects.filter(pattern__startswith='What are the tire specifications')
                    potential_responses.extend(vehicle_rules.values_list('response', flat=True))
                
                # Check for product-related queries
                if any(word in user_message for word in ['product', 'tire', 'price', 'cost', 'tell me about']):
                    product_rules = Rule.objects.filter(pattern__startswith='Tell me about')
                    potential_responses.extend(product_rules.values_list('response', flat=True))
            
            # If still no matches, provide a default help message
            if not potential_responses:
                potential_responses = [
                    "I can help you with:\n"
                    "1. Tire specifications for vehicles\n"
                    "2. Product information about tires\n"
                    "3. General questions\n\n"
                    "Try asking about a specific vehicle or tire product!"
                ]
            
            try:
                # Initialize LLMService only when needed
                llm_service = LLMService()
                # Use LLM to filter and select the best response
                selected_response = llm_service.filter_response(user_message, list(potential_responses))
            except ValueError as e:
                # Handle missing API key
                return JsonResponse({
                    'error': 'OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable.'
                }, status=500)
            except Exception as e:
                # Handle other LLM-related errors
                selected_response = potential_responses[0] if potential_responses else "I'm sorry, I couldn't process that request."
            
            # Save the conversation
            Message.objects.create(
                user_message=user_message,
                bot_response=selected_response
            )
            
            return JsonResponse({
                'response': selected_response
            })
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
