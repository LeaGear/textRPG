import random

from game.models import Character, Enemy, ShopOffer, Item, Inventory, GameLog, LogCategory
from django.db import transaction
from django.utils.timezone import now

def get_user_character(user):
    return Character.objects.filter(user = user).select_related('current_enemy').first()

def get_new_enemy(character):
    all_enemies = Enemy.objects.all()
    if all_enemies:
        random_enemy = random.choice(all_enemies)
        character.set_new_enemy(random_enemy, random_enemy.hp)

def add_log(person, info, category):
    GameLog.objects.create(
        character = person,
        text = info,
        category = category
    )

def get_last_logs(character):
    raw_logs = GameLog.objects.filter(character = character).order_by('-created_at')[:30]
    logs = list(raw_logs)[::-1]
    return logs

@transaction.atomic
def buy_item_from_store(offer_id, char):
    offer = ShopOffer.objects.filter(id = offer_id, character = char).first()
    if not offer:
        return
    character = offer.character
    item = offer.item
    if character and item:
        if character.gold >= item.cost:
            character.spend_gold(item.cost)
            Inventory.objects.create(character = character, item = item)
            add_log(
                character,
                f"Player {character.name} bought {item.name} for {item.cost} golds",
                LogCategory.ECONOMY
            )
            offer.delete()
        else:
            print("Not enough gold! ")

@transaction.atomic
def sell_item_from_inventory(record_id, char):
    inv_record = Inventory.objects.filter(id = record_id, character = char).first()
    if not inv_record:
        return
    item_cost = inv_record.item.cost
    character = inv_record.character
    if item_cost and character:
        add_log(
            character,
            f"Player {character.name} sold {inv_record.item.name} for {inv_record.item.cost // 2} golds",
            LogCategory.ECONOMY
        )
        inv_record.delete()
        character.add_gold(item_cost // 2)


@transaction.atomic
def refresh_char_store_offer(character):
    if character.gold >= character.store_refresh_cost:
        ShopOffer.objects.filter(character = character).delete()
        items = list(Item.objects.all())
        if items:
            count = min(len(items), 5)
            selected_items = random.sample(items, count)
            ShopOffer.objects.bulk_create([
                ShopOffer(character=character, item=item) for item in selected_items
            ])
        character.spend_gold(character.store_refresh_cost)
    else:
        print("Not enough gold! ")

@transaction.atomic
def resolve_enemy_death(character):
    if character.enemy_hp <= 0:
        add_log(
            character,
            f"Enemy {character.current_enemy.name} is defeated! Reward: {character.current_enemy.reward_exp} EXP, {character.current_enemy.reward_gold} gold",
            LogCategory.COMBAT
        )
        character.add_exp(character.current_enemy.reward_exp)
        character.add_gold(character.current_enemy.reward_gold)
        get_new_enemy(character)

def apply_dps_damage(character):
    if character.total_dps_damage <= 0:
        return
    time_diff = now() - character.last_dps_tick_time
    elapsed_seconds = int(time_diff.total_seconds())
    dps_damage = character.total_dps_damage * elapsed_seconds
    character.attack_enemy(dps_damage)
    resolve_enemy_death(character)
#    add_log(
#        character,
#        f"Player {character.name} DPS {character.current_enemy.name} by {character.total_dps_damage} damage",
#        LogCategory.COMBAT
#    )

    if elapsed_seconds >= 1:
        character.change_last_dps_tick_time()

def attack_action(character):
    character.attack_enemy(character.total_click_damage)
    add_log(
        character,
        f"Player {character.name} attacks {character.current_enemy.name} by {character.total_click_damage} damage",
        LogCategory.COMBAT
    )

    resolve_enemy_death(character)

