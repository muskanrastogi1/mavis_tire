from django.core.management.base import BaseCommand
from chatbot.models import ConversationState, FlowTransition
import json

class Command(BaseCommand):
    help = 'Adds the diagram flows to the database'

    def handle(self, *args, **options):
        # Clear existing states and transitions
        ConversationState.objects.all().delete()
        FlowTransition.objects.all().delete()
        
        # Define states with their default next states and responses
        states_data = [
            {
                'state': 'greeting',
                'default_next_state': 'ask_for_store',
                'default_response': 'Hi! I am Mavis Tire\'s AI assistant. How can I help you today?'
            },
            {
                'state': 'ask_for_store',
                'default_next_state': 'ask_for_size_or_vehicle',
                'default_response': 'Which Mavis Tire is your local store?'
            },
            {
                'state': 'ask_for_size_or_vehicle',
                'default_next_state': 'ask_for_size',
                'default_response': 'Okay. Do you know the size?'
            },
            {
                'state': 'ask_for_size',
                'default_next_state': 'provide_options',
                'default_response': 'What is your tire size? (e.g., 205/65R16)'
            },
            {
                'state': 'provide_options',
                'default_next_state': 'confirm_installation',
                'default_response': 'We have X tire available today at your location.'
            },
            {
                'state': 'confirm_installation',
                'default_next_state': 'schedule_appointment',
                'default_response': 'Would you like to schedule an appointment for today?'
            },
            {
                'state': 'schedule_appointment',
                'default_next_state': 'confirmation',
                'default_response': 'How about on Saturday?'
            },
            {
                'state': 'confirmation',
                'default_next_state': 'farewell',
                'default_response': 'Thank you for your interest! Is there anything else you\'d like to know about tires?'
            },
            {
                'state': 'farewell',
                'default_next_state': 'greeting',
                'default_response': 'Hello! I\'m your Mavis Tire information assistant. How can I help you today?'
            }
        ]

        # Create states
        for state_data in states_data:
            state = ConversationState.objects.create(
                state=state_data['state'],
                default_next_state=state_data['default_next_state'],
                default_response=state_data['default_response'],
                required_info={},
                collected_info={}
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created state: {state.state}\n'
                f'  - Default Next State: {state.default_next_state}\n'
                f'  - Default Response: {state.default_response}'
            ))

        # Create default transitions for each state
        for state_data in states_data:
            FlowTransition.objects.create(
                current_state=state_data['state'],
                next_state=state_data['default_next_state'],
                trigger_pattern='__default__',
                response=state_data['default_response'],
                required_info={}
            )
            self.stdout.write(self.style.SUCCESS(
                f'Created default transition: {state_data["state"]} -> {state_data["default_next_state"]}'
            ))

        self.stdout.write(self.style.SUCCESS('Finished adding diagram flows with default transitions.'))
