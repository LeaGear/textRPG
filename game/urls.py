from django.urls import path
from game.views import game_home, attack_action, register_view, login_view, logout_view

urlpatterns = [
    path('', game_home, name='game_home'),
    path('attack/', attack_action, name='attack_action'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]