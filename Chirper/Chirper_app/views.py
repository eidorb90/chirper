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