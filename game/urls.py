from django.urls import path
from game.views import game_home

urlpatterns = [
    path('', game_home, name='game_home')
]