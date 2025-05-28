from django.core.management.base import BaseCommand
from chatbot.models import ConversationState

class Command(BaseCommand):
    help = 'Adds all conversation states to the database'

    def handle(self, *args, **kwargs):
        states = [
            {
                'state': 'greeting',
                'default_next_state': 'ask_for_store',
                'default_response': 'Hi! I am Mavis Tire\'s AI assistant. How can I help you today?'
            },
            {
                'state': 'ask_for_store',
                'default_next_state': 'ask_for_size_or_vehicle',
                'default_response': 'Which Mavis Tire store would you like to visit?'
            },
            {
                'state': 'ask_for_size_or_vehicle',
                'default_next_state': 'ask_for_size',
                'default_response': 'Would you like to specify a tire size or tell me about your vehicle?'
            },
            {
                'state': 'ask_for_size',
                'default_next_state': 'provide_options',
                'default_response': 'What tire size are you looking for?'
            },
            {
                'state': 'provide_options',
                'default_next_state': 'confirm_installation',
                'default_response': 'Based on your needs, I recommend these options: Michelin Defender and General Altimax. Would you like to proceed with installation?'
            },
            {
                'state': 'confirm_installation',
                'default_next_state': 'schedule_appointment',
                'default_response': 'Great! Would you like to schedule an appointment for the installation?'
            },
            {
                'state': 'schedule_appointment',
                'default_next_state': 'confirmation',
                'default_response': 'What time would work best for you?'
            },
            {
                'state': 'confirmation',
                'default_next_state': 'farewell',
                'default_response': 'Perfect! Your appointment has been scheduled. Is there anything else you need help with?'
            },
            {
                'state': 'farewell',
                'default_next_state': 'greeting',
                'default_response': 'Thank you for choosing Mavis Tire! Have a great day!'
            }
        ]

        for state_data in states:
            ConversationState.objects.get_or_create(
                state=state_data['state'],
                defaults={
                    'default_next_state': state_data['default_next_state'],
                    'default_response': state_data['default_response']
                }
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created state: {state_data["state"]}')) 