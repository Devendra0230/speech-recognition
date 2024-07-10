from django.db import models


class VoiceCommand(models.Model):
    command = models.CharField(max_length=100)
    action = models.TextField()
    
class TextToSpeech(models.Model):
    text = models.TextField()
    audio_file = models.FileField(upload_to='audio/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]
