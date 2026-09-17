from django.urls import path
from game.views import game_home, attack_action_view, register_view, login_view, logout_view, refresh_store, buy_item_view

urlpatterns = [
    path('', game_home, name='game_home'),
    path('attack/', attack_action_view, name='attack_action'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('refresh_store/', refresh_store, name='refresh_store'),
    path('buy_item/', buy_item_view, name='buy_item'),
]