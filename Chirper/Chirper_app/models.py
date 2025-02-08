from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
# Create your models here.

class Chirp(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]
    

class User(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=20)


    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
