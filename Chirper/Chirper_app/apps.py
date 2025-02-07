from django.apps import AppConfig
from django.contrib import admin

class ChirperAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Chirper_app'


class RegisterUser(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.set_password(obj.password)
        obj.save()