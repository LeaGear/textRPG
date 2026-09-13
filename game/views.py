
from django.http import HttpResponse
from django.shortcuts import render, redirect


from game.models import Character, Enemy
from game.services import get_new_enemy

# Create your views here.

def game_home(view_request):
    character = Character.objects.filter(id=1).first()
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
        character = Character.objects.filter(id=1).first()
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


