from django.core.management.base import BaseCommand
from chatbot.models import FlowTransition

class Command(BaseCommand):
    help = 'Adds default flow transitions for the conversation'

    def handle(self, *args, **kwargs):
        default_transitions = [
            {
                'current_state': 'greeting',
                'next_state': 'vehicle_info',
                'trigger_pattern': 'tire specifications',
                'response': 'I can help you with tire specifications. Could you please tell me your vehicle make and model?',
                'required_info': {'make': None, 'model': None}
            },
            {
                'current_state': 'greeting',
                'next_state': 'product_info',
                'trigger_pattern': 'product information',
                'response': 'I can help you with product information. What specific tire product would you like to know about?',
                'required_info': {'product': None}
            },
            {
                'current_state': 'vehicle_info',
                'next_state': 'tire_specs',
                'trigger_pattern': 'make model',
                'response': 'Great! Let me look up the tire specifications for your {make} {model}.',
                'required_info': {'make': None, 'model': None}
            },
            {
                'current_state': 'tire_specs',
                'next_state': 'confirmation',
                'trigger_pattern': 'specifications found',
                'response': 'Here are the tire specifications for your vehicle. Would you like to know more about any specific aspect?',
                'required_info': {}
            },
            {
                'current_state': 'product_info',
                'next_state': 'confirmation',
                'trigger_pattern': 'product details',
                'response': 'Here are the details about the product. Would you like to know more about any specific aspect?',
                'required_info': {}
            },
            {
                'current_state': 'confirmation',
                'next_state': 'farewell',
                'trigger_pattern': 'no more questions',
                'response': 'Thank you for your interest! Is there anything else you\'d like to know about tires?',
                'required_info': {}
            },
            {
                'current_state': 'farewell',
                'next_state': 'greeting',
                'trigger_pattern': 'new question',
                'response': 'Hello! I\'m your Mavis Tire information assistant. How can I help you today?',
                'required_info': {}
            }
        ]

        for transition_data in default_transitions:
            transition, created = FlowTransition.objects.update_or_create(
                current_state=transition_data['current_state'],
                next_state=transition_data['next_state'],
                trigger_pattern=transition_data['trigger_pattern'],
                defaults={
                    'response': transition_data['response'],
                    'required_info': transition_data['required_info']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created transition: {transition_data["current_state"]} -> {transition_data["next_state"]}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated transition: {transition_data["current_state"]} -> {transition_data["next_state"]}')
                ) 