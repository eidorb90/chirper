from django.shortcuts import render
from .models import Chirp

# Create your views here.
def home(request):
    chirps = Chirp.objects.all().order_by('-created_at') 

    return render(request, 'home.html', {
        "message" : 'Welcome to the Chirper Home Page!!',
        'chirps' : chirps
    })