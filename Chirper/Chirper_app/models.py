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
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=255, blank=True)
    location = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Edit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=255, blank=True)
    location = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    
