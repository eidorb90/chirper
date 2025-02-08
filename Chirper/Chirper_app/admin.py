from django.contrib import admin
from .models import Chirp, User

@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title',) 
    list_filter = ('created_at',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'created_at')
    search_fields = ('username', 'created_at')
    list_filter = ('username', 'created_at')