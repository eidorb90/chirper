"""
Brodie Rogers
Marcus Sweet
<brodie.rogers@cune.students.edu>

admin.py
Last Edited : 3/20/25

Description:
    In this file we create the specify the differnt
    database tables that we want to see in the admin pannel.
    With each of these pannels we can sepecify what
    information from each model that we want.

Help:
    The classes defined below are somewhat self explanatory,
    we specify what we want to be able to have the model to be
    listed by, able to search with, and what we want to be able to filter by.

"""

from django.contrib import admin
from .models import Chirp, Reply, User


# Register the User model with the admin site
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ("username", "created_at", "id")
    # Specify the fields to search by
    search_fields = ("username", "created_at", "id")
    # Specify the fields to filter by
    list_filter = ("created_at", "id")


# Register the Chirp model with the admin site
@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ("title", "content", "created_at", "id")
    # Specify the fields to search by
    search_fields = ("title", "created_at", "id")
    # Specify the fields to filter by
    list_filter = ("created_at", "id")


# Register the Reply model with the admin site
@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ("content", "created_at")
    # Specify the fields to search by
    search_fields = ("content", "created_at")
    # Specify the fields to filter by
    list_filter = ("content", "created_at")
