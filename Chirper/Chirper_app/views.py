from django.shortcuts import render
from .models import Chirp

# Create your views here.
def home(request):
    chirps = Chirp.objects.all().order_by('-created_at') 

    return render(request, 'home.html', {
        'chirps' : chirps
    })

def account(request):
    return render(request, 'account.html')

def create_chirp(request):
    if request == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        # date = request.POST.get('date')
        Chirp.objects.create(title=title, content=content)
#, date=date
        chirps = Chirp.objects.all().order_by('-created_at')
        print("Chirp Created")
        return render(request, 'chirp_list.html', {'chirps': chirps})

