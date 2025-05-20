from django.db import models

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

    def __str__(self):
        return f"User: {self.user_message} | Bot: {self.bot_response}"
