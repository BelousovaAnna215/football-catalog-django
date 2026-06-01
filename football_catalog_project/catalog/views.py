from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Player, Club, Country
from .forms import PlayerForm


def home(request):
    player_count = Player.objects.count()
    club_count = Club.objects.count()
    country_count = Country.objects.count()

    context = {
        'players_count': player_count,
        'clubs_count': club_count,
        'countries_count': country_count,
    }

    return render(request, 'catalog/home.html', context)


def catalog(request):
    players = Player.objects.all()
    context = {
        'players': players,
    }
    return render(request, 'catalog/catalog.html', context)


def player_detail(request, id):
    player = get_object_or_404(Player, id=id)
    context = {
        'player': player,
    }
    return render(request, 'catalog/player_detail.html', context)


def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Игрок успешно добавлен!')
            return redirect('catalog:catalog')
        else:
            for error in form.errors.values():
                messages.error(request, str(error))
    else:
        form = PlayerForm()

    clubs = Club.objects.all()
    return render(request, 'catalog/add_player.html', {'form': form, 'clubs': clubs})
