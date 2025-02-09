from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from .models import Chirp, Reply


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

def create_reply(request, chirp_id):
    if request.method == "POST":
        chirp = Chirp.objects.get(id=chirp_id)
        reply = Reply.objects.create(
            chirp=chirp,
            content=request.POST.get('content')
        )
        return render(request, 'reply_list.html', {'chirp': chirp})
    return HttpResponseRedirect('/')

def like_chirp(request, chirp_id):
    chirp = Chirp.objects.get(id=chirp_id)
    chirp.like_count += 1
    chirp.save()
    return HttpResponse(chirp.like_count)
