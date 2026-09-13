from django.contrib import admin

from game.models import Character, Enemy, Item, Inventory
# Register your models here.

admin.site.register(Character)
admin.site.register(Enemy)
admin.site.register(Item)
admin.site.register(Inventory)