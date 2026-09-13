import random


def get_new_enemy(character, all_enemies):
    if all_enemies:
        random_enemy = random.choice(all_enemies)
        character.enemy_name = random_enemy.name
        character.enemy_hp = random_enemy.hp * character.level
        character.save()
