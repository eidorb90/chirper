from django.db import models
from django.utils.timezone import now
import uuid

# Create your models here.

class Chirp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return self.content[:50]

class Reply(models.Model):
    chirp = models.ForeignKey(Chirp, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(max_length=255)
    created_at = models.DateField(auto_now_add=True)