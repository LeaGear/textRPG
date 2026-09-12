import random

from django.http import HttpResponse
from django.shortcuts import render, redirect


from game.models import Character, Enemy
# Create your views here.

def game_home(view_request):
    character = Character.objects.filter(id=1).first()
    if not character.enemy_name:
        get_new_enemy(character)

    enemy_name = character.enemy_name

    enemy = Enemy.objects.filter(name=enemy_name).first()
    context = {
        'character' : character,
        'enemy': enemy
    }
    return render(view_request, 'game/game_home.html', context)

def attack_action(view_request):
    if view_request.method == 'POST':
        character = Character.objects.filter(id=1).first()

        if character and character.enemy_name:
            enemy = Enemy.objects.filter(name=character.enemy_name).first()

            if enemy:
                character.enemy_hp -= character.damage

                if character.enemy_hp <= 0:
                    character.exp += enemy.reward_exp
                    character.gold += enemy.reward_gold
                    get_new_enemy(character)

                character.save()

    return redirect('game_home')


def get_new_enemy(character):
    all_enemies = list(Enemy.objects.all())
    print(all_enemies)
    if all_enemies:
        random_enemy = random.choice(all_enemies)
        print(f"Now random -> {random_enemy}")
        character.enemy_name = random_enemy.name
        character.enemy_hp = random_enemy.hp * character.level
        character.save()
