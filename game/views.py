from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from django.http import HttpResponse
from django.shortcuts import render, redirect


from game.models import Character, Enemy
from game.services import get_new_enemy

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Character.objects.create(
                user=user,
                name=user.username
            )
            return redirect('game_home')
    else:
        form =  UserCreationForm()
    context = {"form" : form}
    return render(request, 'game/register.html', context=context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('game_home')
    else:
        form = AuthenticationForm()
    context = {"form" : form}
    return render(request, "game/login.html", context)

def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect('game_home')

def game_home(view_request):
    character = None
    if view_request.user.is_authenticated:
        character = Character.objects.filter(user=view_request.user).first()
    if character:
        enemy_name = character.enemy_name
        enemy = Enemy.objects.filter(name=enemy_name).first()
    else:
        enemy = Enemy.objects.first()

    context = {
        'character' : character,
        'enemy': enemy
    }
    return render(view_request, 'game/main_screen.html', context)

def attack_action(view_request):
    if view_request.method == 'POST':
        character = Character.objects.filter(user=view_request.user).first()
        if character and character.enemy_name:
            enemy = Enemy.objects.filter(name=character.enemy_name).first()

            if enemy:
                character.enemy_hp -= character.damage

                if character.enemy_hp <= 0:
                    character.add_exp(enemy.reward_exp)
                    character.add_gold(enemy.reward_gold)
                    all_enemies = list(Enemy.objects.all())
                    get_new_enemy(character, all_enemies)

                character.save()

    return redirect('game_home')


