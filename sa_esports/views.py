from django.shortcuts import render
from leagues.models import League
from players.models import Player


def home(request):
    """
    Landing page showing featured leagues and top-ranked players.
    """
    featured_leagues = League.objects.filter(is_active=True).order_by('-created_at')[:4]
    top_players = Player.objects.all().order_by('-ranking_points')[:6]

    context = {
        'featured_leagues': featured_leagues,
        'top_players': top_players,
        'page_title': 'SA Esports Hub',
    }
    return render(request, 'home.html', context)