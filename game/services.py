import random

from game.models import Character, Enemy, ShopOffer, Item, Inventory


def get_user_character(user):
    return Character.objects.filter(user = user).first()

def get_new_enemy(character, all_enemies):
    if all_enemies:
        random_enemy = random.choice(all_enemies)
        character.enemy_name = random_enemy.name
        character.enemy_hp = random_enemy.hp * character.level
        character.save()

def buy_item_from_store(offer_id):
    offer = ShopOffer.objects.get(id = offer_id)
    character = Character.objects.get(id = offer.character.id)
    item = Item.objects.get(id = offer.item.id)
    if character and item:
        if character.gold >= item.cost:
            character.spend_gold(item.cost)
            Inventory.objects.create(character = character, item = item)
            ShopOffer.objects.filter(id=offer_id).delete()
            character.save()
        else:
            print("Not enough gold! ")

def refresh_char_store_offer(character):
    if character.gold >= character.store_refresh_cost:
        offer = []
        ShopOffer.objects.filter(character = character).delete()
        items = list(Item.objects.all())
        while len(offer) < min(len(items), 5):
            random_item = random.choice(items)
            if random_item not in offer:
                offer.append(random_item)
        for item in offer:
            ShopOffer.objects.create(character = character, item = item)
        character.spend_gold(character.store_refresh_cost)
        character.save()
    else:
        print("Not enough gold! ")

def attack_action(character, enemy):
    character.enemy_hp -= character.damage

    if character.enemy_hp <= 0:
        character.add_exp(enemy.reward_exp)
        character.add_gold(enemy.reward_gold)
        all_enemies = list(Enemy.objects.all())
        get_new_enemy(character, all_enemies)

    character.save()