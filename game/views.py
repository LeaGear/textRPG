from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render, redirect


from game.models import Character, Enemy, ShopOffer, Inventory
from game.services import refresh_char_store_offer, buy_item_from_store, sell_item_from_inventory, attack_action, get_user_character

# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            Character.objects.create(
                user=user,
                name=user.username
            )
            return redirect('game_home')
    else:
        form =  UserCreationForm()
    context = {"form" : form}
    return render(request, 'game/register.html', context=context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('game_home')
    else:
        form = AuthenticationForm()
    context = {"form" : form}
    return render(request, "game/login.html", context)

@login_required
def logout_view(request):
    if request.method == "POST":
        auth_logout(request)
    return redirect('game_home')

def game_home(view_request):
    character = None
    shop_offer = []
    char_inventory = []

    if view_request.user.is_authenticated:
        character = get_user_character(view_request.user)
    if character:
        enemy = character.current_enemy
        shop_offer = list(ShopOffer.objects.filter(character=character))
        char_inventory = list(Inventory.objects.filter(character=character))

    else:
        enemy = Enemy.objects.first()



    context = {
        'character' : character,
        'enemy': enemy,
        'offers': shop_offer,
        'inventory': char_inventory
    }
    return render(view_request, 'game/main_screen.html', context)

@login_required
def refresh_store(request):
    if request.method == 'POST':
        character = get_user_character(request.user)
        if character:
            refresh_char_store_offer(character)
    return redirect('game_home')

@login_required
def buy_item_view(request):
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        buy_item_from_store(offer_id)
    return redirect('game_home')

@login_required
def sell_item_view(request):
    if request.method == 'POST':
        inventory_slot_id = request.POST.get('inventory_record_id')
        print("LOOOOOL", inventory_slot_id)
        sell_item_from_inventory(inventory_slot_id)
    return redirect('game_home')

@login_required
def attack_action_view(view_request):
    if view_request.method == 'POST':
        character = get_user_character(view_request.user)
        if character and character.current_enemy:
            attack_action(character, character.current_enemy)
    return redirect('game_home')


