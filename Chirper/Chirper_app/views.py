from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Chirp, User
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, EmailAuthenticationForm
from django.contrib import messages
from .forms import ProfileForm, EditProfileForm

# Create your views here.
def home(request):
    chirps = Chirp.objects.all().order_by('-created_at') 

    return render(request, 'home.html', {
        'chirps' : chirps
    })

def account(request):
    user_account = request.user
    return render(request, 'account.html', {'user' : user_account   })

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
            return redirect('login_view')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        print("Form valid:", form.is_valid())
        if not form.is_valid():
            print("Form errors:", form.errors)
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=User.objects.get(email=email).username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = EmailAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def profile(request):
    user = request.user
    profile = user.profile
    return render(request, 'profile.html', {'profile': profile})

def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})