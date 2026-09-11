from django.http import HttpResponse

from django.shortcuts import render

from game.models import Character
# Create your views here.

def game_home(view_request):
    character = Character.objects.filter(id=1).first()
    context = {
        'character' : character
    }
    return render(view_request, 'game/game_home.html', context)