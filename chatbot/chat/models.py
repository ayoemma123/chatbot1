from django.db import models


class ChatLog(models.Model):
    user_message = models.TextField()
    predicted_intent = models.CharField(max_length=50)
    response_sent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.predicted_intent}"
