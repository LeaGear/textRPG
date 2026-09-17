import random

from game.models import Character, Enemy, ShopOffer, Item, Inventory


def get_user_character(user):
    return Character.objects.filter(user = user).first()

def get_new_enemy(character):
    all_enemies = Enemy.objects.all()
    if all_enemies:
        random_enemy = random.choice(all_enemies)
        character.current_enemy = random_enemy
        character.enemy_hp = random_enemy.hp * character.level
        character.save()

def buy_item_from_store(offer_id):
    offer = ShopOffer.objects.get(id = offer_id)
    character = offer.character
    item = offer.item
    if character and item:
        if character.gold >= item.cost:
            character.spend_gold(item.cost)
            Inventory.objects.create(character = character, item = item)
            ShopOffer.objects.filter(id = offer_id).delete()
            character.save()
        else:
            print("Not enough gold! ")

def sell_item_from_inventory(record_id):
    inv_record = Inventory.objects.get(id = record_id)
    item_cost = inv_record.item.cost
    character = inv_record.character
    Inventory.objects.filter(id = record_id).delete()
    character.add_gold(item_cost/2)
    character.save()

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
    character.enemy_hp -= character.total_click_damage

    if character.enemy_hp <= 0:
        character.add_exp(enemy.reward_exp)
        character.add_gold(enemy.reward_gold)
        get_new_enemy(character)

    character.save()