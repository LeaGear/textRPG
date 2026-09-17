from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Character(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(max_length=100, verbose_name='Character Name', unique=True)
    level = models.IntegerField(default=1, verbose_name='Character Level')
    exp = models.IntegerField(default=0, verbose_name='Character EXP')
    exp_to_new_level = models.IntegerField(default=100, verbose_name='Character XP To New Level')
    hp = models.IntegerField(default=100, verbose_name='Character Current HP')
    max_hp = models.IntegerField(default=100, verbose_name='Character Max HP')
    damage = models.FloatField(default=10.0, verbose_name='Character Damage')
    gold = models.IntegerField(default=0, verbose_name='Character Gold')
    store_refresh_cost = models.IntegerField(default=10, verbose_name='Character Store Refresh Cost')

    enemy_name = models.CharField(default ='Zombie', max_length=100, verbose_name='Name of Current Enemy')
    enemy_hp = models.IntegerField(default=5, verbose_name='Current Enemy HP')

    def __str__(self):
        return self.name

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_new_level:
            self.exp -= self.exp_to_new_level
            self.level += 1
            self.exp_to_new_level *= 1.5
            self.max_hp += self.max_hp * 0.1
            self.hp = self.max_hp
            self.store_refresh_cost = self.level * 10

    def add_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if amount > self.gold:
            raise ValueError("Not enough gold")
        self.gold -= amount

class Enemy(models.Model):
    name = models.CharField(max_length=100, verbose_name='Enemy Name')
    hp = models.IntegerField(default=30, verbose_name='Enemy Current HP')
    max_hp = models.IntegerField(default=30, verbose_name="Enemy MAX HP")
    damage = models.FloatField(default=5.0, verbose_name='Enemy Damage')
    reward_exp = models.IntegerField(default=5, verbose_name='Enemy Reward EXP')
    reward_gold = models.IntegerField(default=10, verbose_name='Enemy Reward Gold')

    def __str__(self):
        return f'{self.name} (HP: {self.hp})'

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Item Name')
    cost = models.IntegerField(default=100, verbose_name='Item Cost')
    stat_up = models.CharField(max_length=100, verbose_name='Item Stat Up')

    def __str__(self):
        return f'{self.name} (Cost: {self.cost}) - UP: {self.stat_up}'

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
