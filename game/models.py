from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.

class Enemy(models.Model):
    name = models.CharField(max_length=100, verbose_name='Enemy Name')
    hp = models.PositiveIntegerField(default=30, verbose_name='Enemy Current HP')
    max_hp = models.PositiveIntegerField(default=30, verbose_name="Enemy MAX HP")
    damage = models.FloatField(default=5.0, verbose_name='Enemy Damage')
    reward_exp = models.PositiveIntegerField(default=5, verbose_name='Enemy Reward EXP')
    reward_gold = models.PositiveIntegerField(default=10, verbose_name='Enemy Reward Gold')

    def __str__(self):
        return f'{self.name} (HP: {self.hp})'

class Character(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100, verbose_name='Character Name')
    level = models.IntegerField(default=1, verbose_name='Character Level')
    exp = models.PositiveIntegerField(default=0, verbose_name='Character EXP')
    exp_to_new_level = models.IntegerField(default=100, verbose_name='Character XP To New Level')
    hp = models.PositiveIntegerField(default=100, verbose_name='Character Current HP')
    max_hp = models.PositiveIntegerField(default=100, verbose_name='Character Max HP')
    base_click_damage = models.FloatField(default=10.0, verbose_name='Character Damage')
    base_dps_damage = models.FloatField(default=0.0, verbose_name='Character DPS Damage')
    gold = models.PositiveIntegerField(default=0, verbose_name='Character Gold')
    store_refresh_cost = models.IntegerField(default=10, verbose_name='Character Store Refresh Cost')

    current_enemy = models.ForeignKey(Enemy, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Name of Current Enemy')
    enemy_hp = models.IntegerField(default=5, verbose_name='Current Enemy HP')

    def __str__(self):
        return self.name

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_new_level:
            self.exp -= self.exp_to_new_level
            self.level += 1
            self.exp_to_new_level *= 1.5
            self.max_hp += int(self.max_hp * 0.1)
            self.hp = self.total_max_hp
            self.store_refresh_cost = self.level * 10

    def add_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if amount > self.gold:
            raise ValueError("Not enough gold")
        self.gold -= amount

    @property
    def sum_hp_bonus(self):
        result = self.inventory_set.aggregate(total_hp=Sum('item__hp_bonus'))['total_hp']
        return result or 0

    @property
    def total_max_hp(self):
        return self.max_hp + self.sum_hp_bonus

    @property
    def sum_click_damage_bonus(self):
        result = self.inventory_set.aggregate(total_dmg=Sum('item__click_damage_bonus'))['total_dmg']
        return result or 0

    @property
    def total_click_damage(self):
        return self.base_click_damage + self.sum_click_damage_bonus

    @property
    def sum_dps_bonus(self):
        result = self.inventory_set.aggregate(total_dps=Sum('item__dps_bonus'))['total_dps']
        return result or 0

    @property
    def total_dps_damage(self):
        return self.base_dps_damage + self.sum_dps_bonus

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Item Name')
    cost = models.PositiveIntegerField(default=100, verbose_name='Item Cost')

    click_damage_bonus = models.IntegerField(default=0, verbose_name='Item CLICK Damage Bonus')
    dps_bonus = models.IntegerField(default=0, verbose_name="Item DPS Damage Bonus")
    hp_bonus = models.IntegerField(default=0, verbose_name="Item HP Damage Bonus")

    def __str__(self):
        return f'{self.name} (Cost: {self.cost}) - UP: {self.stat_display}'

    @property
    def stat_display(self):
        parts = []
        if self.click_damage_bonus != 0:
            sign = "+" if self.click_damage_bonus > 0 else ""
            parts.append(f"Click Damage {sign}{self.click_damage_bonus}")
        if self.dps_bonus != 0:
            sign = "+" if self.dps_bonus > 0 else ""
            parts.append(f"DPS {sign}{self.dps_bonus}")
        if self.hp_bonus != 0:
            sign = "+" if self.hp_bonus > 0 else ""
            parts.append(f"HP {sign}{self.hp_bonus}")

        return " / ".join(parts) if parts else "NO STAT UP"

class Inventory(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='Item Owner')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Item Name')
    purchased_at = models.DateTimeField(auto_now_add=True, verbose_name='Purchased at')

    def __str__(self):
        return f'{self.character.name} owned {self.item}'

class ShopOffer(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE, verbose_name='Store offer for')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Item Name')

    def __str__(self):
        return f'{self.character.name} see in store  -> {self.item}'
