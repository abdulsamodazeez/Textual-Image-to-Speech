from django.urls import path, include
from . import views

urlpatterns = [
    path('text/', views.ManageSpeechView.as_view(), name='text'),
]