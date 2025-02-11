from django.contrib import admin
from .models import Chirp, Reply, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at', 'id')
    search_fields = ('username', 'created_at', 'id') 
    list_filter = ('created_at', 'id')

@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at', 'id')
    search_fields = ('title', 'created_at', 'id') 
    list_filter = ('created_at', 'id')

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at')
    search_fields = ('content', 'created_at')
    list_filter = ('content', 'created_at')     

