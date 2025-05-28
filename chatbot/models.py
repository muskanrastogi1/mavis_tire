from django.db import models
from django.utils import timezone

# Create your models here.

class Rule(models.Model):
    pattern = models.CharField(max_length=255)
    response = models.CharField(max_length=255)

    def __str__(self):
        return f"Rule: {self.pattern} -> {self.response}"

class Message(models.Model):
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation_state = models.ForeignKey('ConversationState', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"

class ConversationState(models.Model):
    STATE_CHOICES = [
        ('greeting', 'Greeting'),
        ('ask_for_store', 'Asking for Store'),
        ('ask_for_size_or_vehicle', 'Asking for Size or Vehicle'),
        ('ask_for_size', 'Asking for Size'),
        ('ask_for_vehicle', 'Asking for Vehicle'),
        ('provide_options', 'Providing Options'),
        ('price_sensitive', 'Price Sensitive Path'),
        ('quality_brand_focused', 'Quality/Brand Focused Path'),
        ('brand_sensitive', 'Brand Sensitive Path'),
        ('confirm_installation', 'Confirming Installation'),
        ('schedule_appointment', 'Scheduling Appointment'),
        ('ask_about_saturday', 'Asking about Saturday'),
        ('ask_about_discount', 'Asking about Discount'),
        ('start_ticket', 'Starting Ticket'),
        ('confirmation', 'Confirmation'),
        ('farewell', 'Farewell'),
        ('contact_other', 'Contact Other'),
    ]

    state = models.CharField(max_length=30, choices=STATE_CHOICES)
    next_state = models.CharField(max_length=30, choices=STATE_CHOICES, null=True, blank=True)
    default_next_state = models.CharField(max_length=30, choices=STATE_CHOICES, null=True, blank=True)
    default_response = models.TextField(blank=True)
    required_info = models.JSONField(default=dict, blank=True)
    collected_info = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"State: {self.state} -> Default Next: {self.default_next_state}"

class FlowTransition(models.Model):
    current_state = models.CharField(max_length=30, choices=ConversationState.STATE_CHOICES)
    next_state = models.CharField(max_length=30, choices=ConversationState.STATE_CHOICES)
    trigger_pattern = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.current_state} -> {self.next_state} on '{self.trigger_pattern}'"

class VehicleModel(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Camry", "Civic", "F-150"
    make = models.CharField(max_length=100)  # e.g., "Toyota", "Honda", "Ford"
    services = models.TextField()  # Description of services offered
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.make} {self.name}"

    class Meta:
        unique_together = ('make', 'name')

class TireBrand(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Michelin", "Goodyear", "Bridgestone"
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class TireSize(models.Model):
    brand = models.ForeignKey(TireBrand, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=50)  # e.g., "205/55R16", "225/45R17"
    price_range = models.CharField(max_length=100)  # e.g., "$100-$150", "$150-$200"
    features = models.TextField()  # Description of features
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.name} - {self.size}"

    class Meta:
        unique_together = ('brand', 'size')
