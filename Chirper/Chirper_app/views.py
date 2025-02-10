from django.shortcuts import render, HttpResponseRedirect, redirect, HttpResponse
from django.db.models import Q
from .models import Chirp, Reply, User
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm, EmailAuthenticationForm

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

def create_chirp_reply(request, chirp_id):
    if request.method == "POST":
        chirp = Chirp.objects.get(id=chirp_id)
        reply = Reply.objects.create(
            chirp=chirp,
            content=request.POST.get('content'),
            is_chirp_reply=True
        )
        return render(request, 'reply_list.html', {'chirp': chirp})
    return HttpResponseRedirect('/')

def create_reply_reply(request, reply_id):
    if request.method == "POST":
        parent_reply = Reply.objects.get(id=reply_id)
        chirp = parent_reply.chirp if parent_reply.chirp else parent_reply.parent_reply.chirp
        reply = Reply.objects.create(
            parent_reply=parent_reply,
            content=request.POST.get('content'),
            is_chirp_reply=False
        )
        # Get all nested replies, not just the new one
        all_nested_replies = parent_reply.replies.all().order_by('created_at')
        return render(request, 'nested_reply.html', {
            'nested_replies': all_nested_replies
        })
    return HttpResponseRedirect('/')

def like_chirp(request, chirp_id):
    chirp = Chirp.objects.get(id=chirp_id)
    chirp.like_count += 1
    chirp.save()
    return HttpResponse(chirp.like_count)


def like_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    reply.like_count += 1
    reply.save()
    return HttpResponse(reply.like_count)

def search(request):
    q = request.GET.get('q', '')
    
    if q:
        chirp_results = Chirp.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).order_by('-created_at', '-like_count')[:20]
        reply_results = Reply.objects.filter(Q(content__icontains=q)).order_by('-created_at', '-like_count')[:10]
    else:
        chirp_results = []
        reply_results = []

    if request.headers.get('HX-Request'):
        return render(request, 'results_partial.html', {'chirp_results': chirp_results, 'reply_results' : reply_results})

    return render(request, 'results.html', {'chirp_results': chirp_results, 'reply_results' : reply_results})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')  # Redirect to the login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib import messages

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
