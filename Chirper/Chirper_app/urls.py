from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account', views.account, name="account"),
    path('create_chirp/', views.create_chirp, name="create_chirp"),
    path('chirp/<uuid:chirp_id>/reply/', views.create_chirp_reply, name="create_chirp_reply"),
    path('reply/<uuid:reply_id>/reply/', views.create_reply_reply, name="create_reply_reply"),
    path('like_chirp/<uuid:chirp_id>/', views.like_chirp, name="like_chirp"),
    path('like_reply/<uuid:reply_id>/', views.like_reply, name="like_reply"),
    path('search/', views.search, name='search')
]
