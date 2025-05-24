from django.core.management.base import BaseCommand
from chatbot.models import Rule

class Command(BaseCommand):
    help = 'Adds initial rules to the chatbot database'

    def handle(self, *args, **kwargs):
        rules = [
            {
                'pattern': 'hello',
                'response': 'Hi there! How can I help you today?'
            },
            {
                'pattern': 'how are you',
                'response': "I'm doing well, thank you for asking! How can I assist you?"
            },
            {
                'pattern': 'bye',
                'response': 'Goodbye! Have a great day!'
            },
            {
                'pattern': 'help',
                'response': "I'm here to help! Just ask me any questions you have."
            },
            {
                'pattern': 'thanks',
                'response': "You're welcome! Is there anything else I can help you with?"
            }
        ]

        for rule_data in rules:
            Rule.objects.get_or_create(
                pattern=rule_data['pattern'],
                defaults={'response': rule_data['response']}
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully added rule: {rule_data["pattern"]}')
            ) 