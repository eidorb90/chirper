from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    is_chirp_reply = models.BooleanField(default=True)

    chirp = models.ForeignKey(Chirp, on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def clean(self):
        if (self.chirp is None and self.parent_reply is None) or (self.chirp and self.parent_reply):
            raise ValidationError("A reply must be connected to either a 'Chirp' or another 'Reply'")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.content[0:50]
    
