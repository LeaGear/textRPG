from django.urls import path
from game.views import game_home, attack_action

urlpatterns = [
    path('', game_home, name='game_home'),
    path('attack/', attack_action, name='attack_action')
]