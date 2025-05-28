from django.core.management.base import BaseCommand
from chatbot.models import ConversationState, Message, VehicleModel
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Resets the chatbot by clearing all states and messages, then reloads states and vehicle models'

    def handle(self, *args, **kwargs):
        # Clear all existing data
        self.stdout.write('Clearing all existing data...')
        ConversationState.objects.all().delete()
        Message.objects.all().delete()
        VehicleModel.objects.all().delete()
        
        # Reload states
        self.stdout.write('Reloading conversation states...')
        call_command('add_states')
        
        # Add vehicle models
        self.stdout.write('Adding vehicle models...')
        vehicle_models = [
            {
                'make': 'Toyota',
                'name': 'Camry',
                'services': 'Tire installation, wheel alignment, brake service, oil changes'
            },
            {
                'make': 'Honda',
                'name': 'Civic',
                'services': 'Tire installation, wheel alignment, brake service, oil changes, general maintenance'
            },
            {
                'make': 'Ford',
                'name': 'F-150',
                'services': 'Tire installation, wheel alignment, brake service, oil changes, truck-specific services'
            }
        ]
        
        for model_data in vehicle_models:
            VehicleModel.objects.create(**model_data)
            self.stdout.write(self.style.SUCCESS(f'Added vehicle model: {model_data["make"]} {model_data["name"]}'))
        
        self.stdout.write(self.style.SUCCESS('Chatbot has been reset and reloaded successfully!')) 