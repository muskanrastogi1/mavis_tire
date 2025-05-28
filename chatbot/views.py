from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ConversationState, Message, VehicleModel, TireBrand, TireSize
import json
import logging

logger = logging.getLogger(__name__)

# Global variable to track if flow has completed once
flow_completed = False

def home(request):
    return render(request, 'chatbot/home.html')

def process_separate_message(message):
    """Process messages after flow completion and return appropriate response"""
    message = message.lower()
    
    # Check for tire brand queries
    if any(word in message for word in ['tire', 'brand', 'michelin', 'goodyear', 'bridgestone']):
        try:
            # Extract potential brand name
            words = message.split()
            for word in words:
                if len(word) > 2:  # Avoid very short words
                    brand = TireBrand.objects.filter(name__icontains=word).first()
                    if brand:
                        # Get all sizes for this brand
                        sizes = TireSize.objects.filter(brand=brand)
                        size_info = "\n".join([f"- {size.size}: {size.price_range}" for size in sizes])
                        return f"Yes, we carry {brand.name} tires. {brand.description}\n\nAvailable sizes and prices:\n{size_info}\n\nWould you like to know more about any specific size?"
        except Exception as e:
            logger.error(f"Error looking up tire brand: {str(e)}")
    
    # Check for tire size queries
    if any(char in message for char in ['/', 'R']):  # Common in tire sizes like 205/55R16
        try:
            # Look for size pattern in the message
            words = message.split()
            for word in words:
                if '/' in word and 'R' in word:
                    size = TireSize.objects.filter(size__icontains=word).first()
                    if size:
                        return f"Yes, we have {size.brand.name} tires in size {size.size}.\nPrice range: {size.price_range}\nFeatures: {size.features}\n\nWould you like to know more about this tire or check availability?"
        except Exception as e:
            logger.error(f"Error looking up tire size: {str(e)}")
    
    # Check for vehicle model queries
    if any(word in message for word in ['model', 'vehicle', 'car', 'truck', 'suv']):
        try:
            # Extract potential model name
            words = message.split()
            for word in words:
                if len(word) > 2:  # Avoid very short words
                    model = VehicleModel.objects.filter(name__icontains=word).first()
                    if model:
                        return f"Yes, we service {model.name}. We offer {model.services} for this model. Would you like to know more about our services for {model.name}?"
        except Exception as e:
            logger.error(f"Error looking up vehicle model: {str(e)}")
    
    # Store related queries
    if any(word in message for word in ['store', 'location', 'near', 'closest']):
        return "We have multiple Mavis Tire locations. Could you please share your zip code so I can find the closest store to you?"
    
    # Hours related queries
    elif any(word in message for word in ['hour', 'open', 'close', 'time']):
        return "Our stores are typically open Monday through Saturday from 7:00 AM to 7:00 PM, and Sunday from 8:00 AM to 5:00 PM. However, hours may vary by location. Would you like to know the hours for a specific store?"
    
    # Services related queries
    elif any(word in message for word in ['service', 'offer', 'do', 'provide']):
        return "We offer a wide range of automotive services including tire sales and installation, wheel alignment, brake service, oil changes, and general auto repair. What specific service are you interested in?"
    
    # Price related queries
    elif any(word in message for word in ['price', 'cost', 'how much', 'expensive']):
        return "Our prices vary depending on the service and your vehicle. Could you please specify which service you're interested in?"
    
    # Appointment related queries
    elif any(word in message for word in ['appointment', 'schedule', 'book', 'reserve']):
        return "You can schedule an appointment through our website, by calling your local store, or by visiting in person. Would you like me to help you find the contact information for your nearest store?"
    
    # Default response for unrecognized queries
    else:
        return "I'm here to help with any questions about our stores, services, or appointments. Could you please provide more details about what you're looking for?"

@csrf_exempt
def chat(request):
    global flow_completed
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            logger.info(f"User message: {user_message}")
            
            # If flow has completed once, process the message directly
            if flow_completed:
                response = process_separate_message(user_message)
                Message.objects.create(
                    user_message=user_message,
                    bot_response=response
                )
                return JsonResponse({
                    'response': response,
                    'state': 'separate_message'
                })
            
            # Get current state
            current_state = ConversationState.objects.order_by('-created_at').first()
            
            # If no state exists, create greeting state
            if not current_state:
                logger.info("No state found, creating greeting state")
                current_state = ConversationState.objects.create(
                    state='greeting',
                    default_next_state='ask_for_store',
                    default_response='Hi! I am Mavis Tire\'s AI assistant. How can I help you today?',
                    required_info={},
                    collected_info={}
                )
            
            logger.info(f"Current state: {current_state.state}")
            
            # Get next state
            next_state_name = current_state.default_next_state
            logger.info(f"Next state name: {next_state_name}")
            
            # Find the next state object
            next_state = ConversationState.objects.filter(state=next_state_name).first()
            if not next_state:
                logger.error(f"Next state {next_state_name} not found!")
                return JsonResponse({'error': f'State {next_state_name} not found'}, status=400)
            
            logger.info(f"Found next state: {next_state.state}")
            response = next_state.default_response
            
            # Create a new state object for the next state
            new_state = ConversationState.objects.create(
                state=next_state_name,
                default_next_state=next_state.default_next_state,
                default_response=next_state.default_response,
                required_info={},
                collected_info={}
            )
            logger.info(f"Created new state: {new_state.state}")
            
            # Save message
            Message.objects.create(
                user_message=user_message,
                bot_response=response
            )
            
            # If we're in farewell state, clear all states and mark flow as completed
            if next_state_name == 'farewell':
                logger.info("Reached farewell state, clearing all states and marking flow as completed")
                ConversationState.objects.all().delete()
                flow_completed = True
            
            return JsonResponse({
                'response': response,
                'state': next_state_name
            })
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({
                'error': 'Invalid JSON in request body'
            }, status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
