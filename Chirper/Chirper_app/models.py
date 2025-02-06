from django.db import models
from django.utils.timezone import now

# Create your models here.

class Chirp(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
    
 