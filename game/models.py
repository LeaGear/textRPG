from django.db import models

# Create your models here.

class Character(models.Model):
    name = models.CharField(max_length=100, verbose_name='Character Name', unique=True)
    level = models.IntegerField(default=1, verbose_name='Character Level')
    exp = models.IntegerField(default=0, verbose_name='Character EXP')
    hp = models.IntegerField(default=100, verbose_name='Character Current HP')
    max_hp = models.IntegerField(default=100, verbose_name='Character Max HP')
    damage = models.FloatField(default=10.0, verbose_name='Character Damage')
    gold = models.IntegerField(default=0, verbose_name='Character Gold')

    enemy_name = models.CharField(default ='Zombie', max_length=100, verbose_name='Name of Current Enemy')
    enemy_hp = models.IntegerField(default=5, verbose_name='Current Enemy HP')

    def __str__(self):
        return self.name

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level += 1
            self.max_hp += self.max_hp * 0.1
            self.hp = self.max_hp

    def add_gold(self, amount):
        self.gold += amount

class Enemy(models.Model):
    name = models.CharField(max_length=100, verbose_name='Enemy Name')
    hp = models.IntegerField(default=30, verbose_name='Enemy Current HP')
    max_hp = models.IntegerField(default=30, verbose_name="Enemy MAX HP")
    damage = models.FloatField(default=5.0, verbose_name='Enemy Damage')
    reward_exp = models.IntegerField(default=5, verbose_name='Enemy Reward EXP')
    reward_gold = models.IntegerField(default=10, verbose_name='Enemy Reward Gold')

    def __str__(self):
        return f'{self.name} (HP: {self.hp})'