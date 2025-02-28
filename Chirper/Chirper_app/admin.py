"""
Brodie Rogers
admin.py
<brodie.rogers@cune.students.edu>

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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "created_at", "id")
    search_fields = ("username", "created_at", "id")
    list_filter = ("created_at", "id")


@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "created_at", "id")
    search_fields = ("title", "created_at", "id")
    list_filter = ("created_at", "id")


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("content", "created_at")
    search_fields = ("content", "created_at")
    list_filter = ("content", "created_at")
