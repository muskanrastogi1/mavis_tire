from django.core.management.base import BaseCommand
from chatbot.models import Rule

class Command(BaseCommand):
    help = 'Adds or updates default rules for general responses'

    def handle(self, *args, **kwargs):
        default_rules = [
            {
                'pattern': 'hello',
                'response': 'Hello! I\'m your Mavis Tire information assistant. How can I help you today?'
            },
            {
                'pattern': 'hi',
                'response': 'Hi there! I can help you with Mavis tire specifications and product information. What would you like to know?'
            },
            {
                'pattern': 'help',
                'response': 'I can help you with:\n1. Tire specifications for vehicles\n2. Product information about tires\n3. General questions\n\nTry asking about a specific vehicle or tire product!'
            },
            {
                'pattern': 'thanks',
                'response': 'You\'re welcome! Is there anything else you\'d like to know about tires?'
            },
            {
                'pattern': 'bye',
                'response': 'Goodbye! Feel free to come back if you have more questions about tires!'
            },
            {
                'pattern': 'goodbye',
                'response': 'Goodbye! Feel free to come back if you have more questions about tires!'
            },
            {
                'pattern': 'see you',
                'response': 'Goodbye! Feel free to come back if you have more questions about tires!'
            },
            {
                'pattern': 'exit',
                'response': 'Goodbye! Feel free to come back if you have more questions about tires!'
            }
        ]

        for rule_data in default_rules:
            rule, created = Rule.objects.update_or_create(
                pattern=rule_data['pattern'],
                defaults={'response': rule_data['response']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created rule: {rule_data["pattern"]}')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully updated rule: {rule_data["pattern"]}')
                ) 