from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Chirp
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, EmailAuthenticationForm

# Create your views here.
def home(request):
    chirps = Chirp.objects.all().order_by('-created_at') 

    return render(request, 'home.html', {
        'chirps' : chirps
    })

def account(request):
    return render(request, 'account.html')

def create_chirp(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        Chirp.objects.create(title=title, content=content)
        chirps = Chirp.objects.all().order_by('-created_at')
        return render(request, 'chirp_list.html', {'chirps': chirps})
    return HttpResponseRedirect('/')




def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})
