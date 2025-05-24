from django.core.management.base import BaseCommand
from chatbot.models import Rule
from chatbot.services import LLMService
import os

class Command(BaseCommand):
    help = 'Enhances responses using OpenAI'

    def handle(self, *args, **options):
        if not os.getenv('OPENAI_API_KEY'):
            self.stdout.write(
                self.style.ERROR('OPENAI_API_KEY environment variable is not set')
            )
            return

        llm_service = LLMService()
        rules = Rule.objects.all()

        for rule in rules:
            try:
                # Create a prompt to enhance the response
                prompt = f"""Given this pattern: "{rule.pattern}"
                And this current response: "{rule.response}"
                
                Please provide an enhanced, more natural response that:
                1. Maintains the same meaning
                2. Is more conversational
                3. Is more engaging
                
                Return only the enhanced response, nothing else."""

                # Get enhanced response from OpenAI
                enhanced_response = llm_service.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that enhances chatbot responses."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=150
                ).choices[0].message.content.strip()

                # Update the rule with enhanced response
                rule.response = enhanced_response
                rule.save()

                self.stdout.write(
                    self.style.SUCCESS(f'Enhanced response for: {rule.pattern}')
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error enhancing response for {rule.pattern}: {str(e)}')
                ) 