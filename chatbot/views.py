from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Rule, Message
from .services import LLMService
import json

llm_service = LLMService()

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            # Get all potential responses from the database
            potential_responses = list(Rule.objects.values_list('response', flat=True))
            
            # Use LLM to filter and select the best response
            selected_response = llm_service.filter_response(user_message, potential_responses)
            
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
