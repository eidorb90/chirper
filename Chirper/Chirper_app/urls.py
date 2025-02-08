from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account', views.account, name="account"),
    path('create_chirp/', views.create_chirp, name="create_chirp"),
    path('chirp/<uuid:chirp_id>/reply/', views.create_reply, name="create_reply"),
    path('like_chirp/<uuid:chirp_id>/', views.like_chirp, name="like_chirp"),
]
