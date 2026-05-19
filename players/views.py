from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Player, ScoutingReport
from .forms import PlayerProfileForm, ScoutingReportForm, PlayerSearchForm


def player_list(request):
    """
    Displays ranked player directory with search and filter.
    """
    form = PlayerSearchForm(request.GET or None)
    players = Player.objects.select_related('user', 'user__profile').order_by('-ranking_points')

    if form.is_valid():
        query = form.cleaned_data.get('query')
        game = form.cleaned_data.get('game')
        skill_tier = form.cleaned_data.get('skill_tier')
        available_only = form.cleaned_data.get('available_only')

        if query:
            players = players.filter(
                Q(user__username__icontains=query) |
                Q(user__profile__gamertag__icontains=query)
            )
        if game:
            players = players.filter(primary_game=game)
        if skill_tier:
            players = players.filter(skill_tier=skill_tier)
        if available_only:
            players = players.filter(is_available_for_scouting=True)

    return render(request, 'players/player_list.html', {
        'players': players,
        'form': form,
        'page_title': 'Player Rankings'
    })


def player_detail(request, pk):
    """
    Detailed view of a player's competitive profile and scouting reports.
    """
    player = get_object_or_404(Player, pk=pk)
    reports = player.scouting_reports.all().select_related('scout')
    user_has_reported = False

    if request.user.is_authenticated:
        user_has_reported = ScoutingReport.objects.filter(
            player=player, scout=request.user
        ).exists()

    return render(request, 'players/player_detail.html', {
        'player': player,
        'reports': reports,
        'user_has_reported': user_has_reported,
        'page_title': str(player)
    })


@login_required
def player_create(request):
    """
    Creates a competitive player profile for the logged-in user.
    """
    if hasattr(request.user, 'player_profile'):
        messages.warning(request, 'You already have a player profile.')
        return redirect('player_detail', pk=request.user.player_profile.pk)

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            messages.success(request, 'Player profile created! Welcome to the rankings.')
            return redirect('player_detail', pk=player.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PlayerProfileForm()

    return render(request, 'players/player_form.html', {
        'form': form,
        'page_title': 'Create Player Profile',
        'action': 'Create'
    })


@login_required
def player_update(request, pk):
    """
    Updates an existing player profile.
    """
    player = get_object_or_404(Player, pk=pk)

    if player.user != request.user and not request.user.is_staff:
        messages.error(request, 'You can only edit your own profile.')
        return redirect('player_detail', pk=pk)

    if request.method == 'POST':
        form = PlayerProfileForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, 'Player profile updated!')
            return redirect('player_detail', pk=player.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PlayerProfileForm(instance=player)

    return render(request, 'players/player_form.html', {
        'form': form,
        'player': player,
        'page_title': 'Edit Player Profile',
        'action': 'Update'
    })


@login_required
def player_delete(request, pk):
    """
    Deletes a player profile.
    """
    player = get_object_or_404(Player, pk=pk)

    if player.user != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own profile.')
        return redirect('player_detail', pk=pk)

    if request.method == 'POST':
        player.delete()
        messages.success(request, 'Player profile deleted.')
        return redirect('player_list')

    return render(request, 'players/player_confirm_delete.html', {
        'player': player,
        'page_title': 'Delete Player Profile'
    })


@login_required
def submit_scouting_report(request, player_pk):
    """
    Allows a scout to submit a report on a player.
    """
    player = get_object_or_404(Player, pk=player_pk)

    if player.user == request.user:
        messages.error(request, 'You cannot scout yourself.')
        return redirect('player_detail', pk=player_pk)

    if ScoutingReport.objects.filter(player=player, scout=request.user).exists():
        messages.warning(request, 'You have already submitted a report for this player.')
        return redirect('player_detail', pk=player_pk)

    if request.method == 'POST':
        form = ScoutingReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.player = player
            report.scout = request.user
            report.save()
            messages.success(request, 'Scouting report submitted!')
            return redirect('player_detail', pk=player_pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ScoutingReportForm()

    return render(request, 'players/scouting_report_form.html', {
        'form': form,
        'player': player,
        'page_title': 'Scout Report'
    })