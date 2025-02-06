from django.contrib import admin
from .models import Chirp

@admin.register(Chirp)
class ChirpAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'created_at')
    search_fields = ('title',) 
    list_filter = ('created_at',)