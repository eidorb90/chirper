from django.shortcuts import (
    render,
    HttpResponseRedirect,
    redirect,
    HttpResponse,
    get_object_or_404,
)
from django.db.models import Q, Count, Exists, OuterRef
from django.contrib.auth.decorators import login_required
from .models import Chirp, Reply, User, UserFollowing
from django.contrib.auth import authenticate, login, logout as auth_logout
from .forms import CustomUserCreationForm, EmailAuthenticationForm


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        chirps = Chirp.objects.all().order_by("-created_at")

        return render(request, "home.html", {"chirps": chirps})
    else:
        return redirect("login_view")
    
def settings(request):
    """
    Render the settings view for the authenticated user.
    """
    return render(request, "settings.html", {"user": request.user})


@login_required
def account(request):
    return render(request, "account.html", {"user": request.user})


@login_required
def delete_account(request):
    if request.user.is_authenticated:
        account_id = request.user.id
        account = get_object_or_404(User, id=account_id)
        account.delete()
        return redirect("register")


@login_required
def create_chirp(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        author = request.user
        Chirp.objects.create(title=title, content=content, author=author)
        chirps = Chirp.objects.all().order_by("-created_at")
        return render(request, "chirp_list.html", {"chirps": chirps})
    return HttpResponseRedirect("/")


@login_required
def delete_chirp(request, chirp_id):
    chirp = get_object_or_404(Chirp, id=chirp_id)
    chirp.delete()
    return HttpResponse("")


@login_required
def create_chirp_reply(request, chirp_id):
    if request.method == "POST":
        chirp = Chirp.objects.get(id=chirp_id)
        author = request.user
        reply = Reply.objects.create(
            chirp=chirp,
            content=request.POST.get("content"),
            is_chirp_reply=True,
            author=author,
        )
        return render(request, "reply_list.html", {"chirp": chirp})
    return HttpResponseRedirect("/")


@login_required
def create_reply_reply(request, reply_id):
    if request.method == "POST":
        parent_reply = Reply.objects.get(id=reply_id)
        chirp = (
            parent_reply.chirp
            if parent_reply.chirp
            else parent_reply.parent_reply.chirp
        )
        author = request.user
        reply = Reply.objects.create(
            parent_reply=parent_reply,
            content=request.POST.get("content"),
            is_chirp_reply=False,
            author=author,
        )
        # Get all nested replies, not just the new one
        all_nested_replies = parent_reply.replies.all().order_by("created_at")
        return render(
            request, "nested_reply.html", {"nested_replies": all_nested_replies}
        )
    return HttpResponseRedirect("/")


@login_required
def like_chirp(request, chirp_id):
    chirp = Chirp.objects.get(id=chirp_id)
    user = request.user
    if user in chirp.likes.all():
        chirp.likes.remove(user)
        chirp.like_count -= 1

    else:
        chirp.likes.add(user)
        chirp.like_count += 1

    chirp.save()
    return HttpResponse(chirp.like_count)


@login_required
def like_reply(request, reply_id):
    reply = Reply.objects.get(id=reply_id)
    user = request.user
    if user in reply.likes.all():
        reply.likes.remove(user)
        reply.like_count -= 1

    else:
        reply.likes.add(user)
        reply.like_count += 1

    reply.save()
    return HttpResponse(reply.like_count)


@login_required
def search(request):
    q = request.GET.get("q", "")

    if q:
        chirp_results = Chirp.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q)
        ).order_by("-created_at", "-like_count")[:20]

        reply_results = Reply.objects.filter(Q(content__icontains=q)).order_by(
            "-created_at", "-like_count"
        )[:10]

        # Subquery to check if the current user follows each account
        following_subquery = UserFollowing.objects.filter(
            user=request.user, following_user=OuterRef("pk")
        )

        account_results = (
            User.objects.filter(Q(username__contains=q))
            .annotate(
                follower_count=Count("follower_relationships"),
                following_status=Exists(following_subquery),
            )
            .order_by("-follower_count", "-created_at")
        )
    else:
        chirp_results = []
        reply_results = []
        account_results = []

    if request.headers.get("HX-Request"):
        return render(
            request,
            "results_partial.html",
            {
                "chirp_results": chirp_results,
                "reply_results": reply_results,
                "account_results": account_results,
            },
        )

    return render(
        request,
        "results.html",
        {
            "chirp_results": chirp_results,
            "reply_results": reply_results,
            "account_results": account_results,
        },
    )


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login_view")
    else:
        form = CustomUserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(
                request,
                username=User.objects.get(email=email).username,
                password=password,
            )
            if user is not None:
                login(request, user)
                return redirect("home")
    else:
        form = EmailAuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def change_username(request):
    if request.method == "POST":
        new_name = request.POST.get("new_username", "").strip()
        if new_name:
            taken_username_list = User.objects.all().values_list("username", flat=True)
            if new_name not in taken_username_list:
                request.user.username = new_name
                request.user.save()
                return render(
                    request,
                    "username_display.html",
                    {
                        "username": new_name,
                        "message": "Username Updated Successfully",
                        "status": "success",
                    },
                )
            return render(
                request,
                "username_display.html",
                {
                    "username": request.user.username,
                    "message": "Username Already Taken",
                    "status": "error",
                },
            )
        return render(
            request,
            "username_display.html",
            {
                "username": request.user.username,
                "message": "Username cannot be empty",
                "status": "error",
            },
        )
    return render(request, "username_display.html", {"username": request.user.username})


@login_required
def change_pfp(request):
    if request.method == "POST":
        print("Got post Request")
        if "profile_image" in request.FILES:
            print("Got profile_image")
            request.user.profile_image = request.FILES["profile_image"]
            request.user.save()

    return render(request, "pfp_container.html", {"user": request.user})


@login_required
def logout(request):
    auth_logout(request)
    return redirect("login_view")


@login_required
def user_chirps(request):
    return render(request, "user_chirps.html", {"chirps": request.user.chirps.all()})


@login_required
def user_replies(request):
    return render(request, "user_replies.html", {"replies": request.user.replies.all()})



@login_required
def view_other_account(request, username):
    try:
        account = User.objects.get(username=username)
        following_status = UserFollowing.objects.filter(
            user=request.user, following_user=account
        ).exists()
        return render(
            request,
            "other_account.html",
            {"user": account, "following_status": following_status},
        )
    except User.DoesNotExist:
        return redirect("home")


@login_required
def other_chirps(request, username):
    try:
        user = User.objects.get(username=username)
        chirps = Chirp.objects.filter(author=user).order_by("-created_at")
        return render(request, "user_chirps.html", {"chirps": chirps, "user": user})
    except User.DoesNotExist:
        return redirect("home")


@login_required
def other_replies(request, username):
    try:
        user = User.objects.get(username=username)
        replies = Reply.objects.filter(author=user).order_by("-created_at")
        return render(request, "user_replies.html", {"replies": replies, "user": user})
    except User.DoesNotExist:
        return redirect("home")


@login_required
def follow_user(request, username):
    try:
        user_to_follow = User.objects.get(username=username)
        following_status = UserFollowing.objects.filter(
            user=request.user, following_user=user_to_follow
        ).exists()

        if following_status:
            UserFollowing.objects.filter(
                user=request.user, following_user=user_to_follow
            ).delete()
            following_status = False
        else:
            UserFollowing.objects.create(
                user=request.user, following_user=user_to_follow
            )
            following_status = True

        return render(
            request,
            "profile_stats.html",
            {
                "user": user_to_follow,
                "following_status": following_status,
            },
        )

    except User.DoesNotExist:
        return HttpResponse(status=404)


@login_required
def change_privacy(request):
    if request.method == "POST":
        user = request.user
        user.private = not user.private
        user.save()

        return render(request, "privacy_button.html", {"user": user})

    return HttpResponse(status=400)
