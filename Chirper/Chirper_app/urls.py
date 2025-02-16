from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("account", views.account, name="account"),
    path("login/", views.login_view, name="login_view"),
    path("register/", views.register, name="register"),
    path("create_chirp/", views.create_chirp, name="create_chirp"),
    path(
        "chirp/<uuid:chirp_id>/reply/",
        views.create_chirp_reply,
        name="create_chirp_reply",
    ),
    path(
        "reply/<uuid:reply_id>/reply/",
        views.create_reply_reply,
        name="create_reply_reply",
    ),
    path("like_chirp/<uuid:chirp_id>/", views.like_chirp, name="like_chirp"),
    path("like_reply/<uuid:reply_id>/", views.like_reply, name="like_reply"),
    path("search/", views.search, name="search"),
    path("logout/", views.logout, name="logout"),
    path("profile/chirps/", views.user_chirps, name="user_chirps"),
    path("profile/replies/", views.user_replies, name="user_replies"),
    path("profile/username/", views.change_username, name="change_username"),
    path("profile/profile_pic/", views.change_pfp, name="change_pfp"),
    path("view/<str:username>/", views.view_other_account, name="view_other_account"),
    path("view/<str:username>/chirps", views.other_chirps, name="other_chirps"),
    path("view/<str:username>/replies", views.other_replies, name="other_replies"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
    path("profile/privacy/", views.change_privacy, name="change_privacy"),
    # TODO work on likes in the future
    # path('profile/likes/', views.user_likes, name='user_likes'),
]
