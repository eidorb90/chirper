from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.files.storage import default_storage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid
import os

# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(
        upload_to='profile_pic/', 
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],
        blank=True, 
        null=True,
        default='profile_pic/default.png'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        # Check if updating an existing user with a new profile image
        if self.pk:  
            old_profile_image = User.objects.filter(pk=self.pk).values_list('profile_image', flat=True).first()
            if old_profile_image and old_profile_image != self.profile_image.name:
                # Delete the old file from storage
                if old_profile_image != 'profile_pic/default.png':  # Avoid deleting the default image
                    default_storage.delete(old_profile_image)

        if self.profile_image:
            img = Image.open(self.profile_image)
            img.thumbnail((300,300), Image.LANCZOS)
            if img.mode != "RGB":
                img = img.convert('RGB')
            
            buffer = BytesIO()
            img.save(buffer, format='PNG', quality=85)
            filename = f'{self.username}{self.id}.png'

            self.profile_image.save(
                filename,
                ContentFile(buffer.getvalue()),
                save=False
            )            

        super().save(*args, **kwargs)
    

class Chirp(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chirps')
    likes = models.ManyToManyField(User, related_name='liked_chirps', blank=True)

    def __str__(self):
        return self.content[:50]

class Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    is_chirp_reply = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)


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
    

