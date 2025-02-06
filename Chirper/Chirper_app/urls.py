from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account', views.account, name="account"),
    path('create_chirp/', views.create_chirp, name="create_chirp")
]
