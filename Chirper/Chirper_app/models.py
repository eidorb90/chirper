"""
Brodie Rogers
models.py
<brodie.rogers@cune.students.edu>

Description:
    This is the file in which we create the different models for our database
    Django uses Object relational mapping (ORM) this allows us to define our
    tables for each model as a Python class.

"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import uuid


class User(AbstractUser):
    """
    User model that extends Django's AbstractUser.

    Attributes:
        id (UUIDField): Primary key for the user, generated automatically.
        email (EmailField): Unique email address for the user.
        created_at (DateTimeField): Timestamp when the user was created.
        username (CharField): Unique username for the user.
        private (BooleanField): Indicates if the user's profile is private.
        profile_image (ImageField): Profile image of the user with validation for file extensions.
        followers (ManyToManyField): Many-to-many relationship to represent followers and following users.

    Methods:
        __str__(): Returns the username of the user.
        set_password(raw_password): Sets the user's password.
        save(*args, **kwargs): Custom save method to handle profile image processing.
    """
    # Create the meta data for the model
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=50, unique=True)
    private = models.BooleanField(default=False)

    profile_image = models.ImageField(
        upload_to="profile_pic/",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg", "gif"])],
        blank=True,
        null=True,
        default="profile_pic/default.png",
    )

    # This creates a ManyToMany relationship between two different users
    followers = models.ManyToManyField(
        "self", through="UserFollowing", symmetrical=False, related_name="following"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):
        # Check if the instance is being updated
        if not self._state.adding:
            try:
                old_instance = self.__class__.objects.get(pk=self.pk)
            except self.__class__.DoesNotExist:
                old_instance = None
        else:
            old_instance = None

        # Process new profile image if it has changed
        if (
            old_instance
            and old_instance.profile_image != self.profile_image
            and self.profile_image
        ):
            img = Image.open(self.profile_image)
            img.thumbnail((300, 300), Image.LANCZOS)
            if img.mode != "RGB":
                img = img.convert("RGB")

            buffer = BytesIO()
            img.save(buffer, format="PNG", quality=85)
            filename = f"{self.username}{self.id}.png"

            self.profile_image.save(
                filename, ContentFile(buffer.getvalue()), save=False
            )

        super().save(*args, **kwargs)


class UserFollowing(models.Model):
    """
    UserFollowing model represents the relationship between users who follow each other.

    Attributes:
        user (ForeignKey): Reference to the User who is following another user.
        following_user (ForeignKey): Reference to the User who is being followed.
        created_at (DateTimeField): Timestamp when the following relationship was created, set automatically.

    Methods:
        __str__(): Returns a string representation of the following relationship.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relationships",
    )
    following_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relationships",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "following_user")

    def __str__(self):
        return f"{self.user.username} follows {self.following_user.username}"


class Chirp(models.Model):
    """
    Chirp model represents a post in the Chirper application.

    Attributes:
        id (UUIDField): Primary key for the Chirp, generated automatically.
        title (CharField): The title of the chirp, limited to 50 characters.
        content (TextField): The content of the chirp, limited to 255 characters.
        created_at (DateTimeField): Timestamp when the chirp was created, set automatically.
        like_count (IntegerField): The number of likes the chirp has received, default is 0.
        author (ForeignKey): Reference to the User who authored the chirp, can be null.
        likes (ManyToManyField): Users who have liked the chirp, can be blank.

    Methods:
        __str__(): Returns a string representation of the chirp, limited to the first 50 characters of the content.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="chirps"
    )
    likes = models.ManyToManyField(User, related_name="liked_chirps", blank=True)

    def __str__(self):
        return self.content[:50]


class Reply(models.Model):
    """
    Reply model represents a reply to a Chirp or another Reply in the Chirper application.

    Attributes:
        id (UUIDField): Primary key for the Reply, generated automatically.
        content (TextField): The content of the reply, limited to 255 characters.
        created_at (DateTimeField): Timestamp when the reply was created, set automatically.
        like_count (IntegerField): The number of likes the reply has received, default is 0.
        is_chirp_reply (BooleanField): Indicates if the reply is to a Chirp, default is True.
        author (ForeignKey): Reference to the User who authored the reply, can be null.
        likes (ManyToManyField): Users who have liked the reply, can be blank.
        chirp (ForeignKey): Reference to the Chirp this reply is connected to, can be null or blank.
        parent_reply (ForeignKey): Reference to another Reply this reply is connected to, can be null or blank.

    Methods:
        clean(): Validates that the reply is connected to either a Chirp or another Reply.
        save(*args, **kwargs): Validates and saves the reply.
        __str__(): Returns a string representation of the reply, limited to the first 50 characters of the content.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField(default=0)
    is_chirp_reply = models.BooleanField(default=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="replies"
    )
    likes = models.ManyToManyField(User, related_name="liked_replies", blank=True)

    chirp = models.ForeignKey(
        Chirp, on_delete=models.SET_NULL, related_name="replies", null=True, blank=True
    )
    parent_reply = models.ForeignKey(
        "self", on_delete=models.SET_NULL, related_name="replies", null=True, blank=True
    )

    def clean(self):
        # Ensure that a reply is connected to either a Chirp or another Reply
        if (self.chirp is None and self.parent_reply is None) or (
            self.chirp and self.parent_reply
        ):
            raise ValidationError(
                "A reply must be connected to either a 'Chirp' or another 'Reply'"
            )

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content[0:50]
