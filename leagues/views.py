from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import League, LeagueRegistration, Match
from .forms import LeagueForm, MatchResultForm, LeagueSearchForm


def league_list(request):
    """
    Displays all leagues with search and filter support.
    """
    form = LeagueSearchForm(request.GET or None)
    leagues = League.objects.filter(is_active=True)

    if form.is_valid():
        query = form.cleaned_data.get('query')
        game = form.cleaned_data.get('game')
        status = form.cleaned_data.get('status')

        if query:
            leagues = leagues.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        if game:
            leagues = leagues.filter(game=game)
        if status:
            leagues = leagues.filter(status=status)

    return render(request, 'leagues/league_list.html', {
        'leagues': leagues,
        'form': form,
        'page_title': 'Leagues'
    })


def league_detail(request, pk):
    """
    Detailed view of a single league including matches and participants.
    """
    league = get_object_or_404(League, pk=pk)
    registrations = league.registrations.filter(status='approved').select_related('player')
    matches = league.matches.all().select_related('player_one', 'player_two', 'winner')
    user_registered = False

    if request.user.is_authenticated:
        user_registered = LeagueRegistration.objects.filter(
            league=league, player=request.user
        ).exists()

    return render(request, 'leagues/league_detail.html', {
        'league': league,
        'registrations': registrations,
        'matches': matches,
        'user_registered': user_registered,
        'page_title': league.name
    })


@login_required
def league_create(request):
    """
    Creates a new league. Only available to logged-in users.
    """
    if request.method == 'POST':
        form = LeagueForm(request.POST, request.FILES)
        if form.is_valid():
            league = form.save(commit=False)
            league.organizer = request.user
            league.save()
            messages.success(request, f'League "{league.name}" created successfully!')
            return redirect('league_detail', pk=league.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = LeagueForm()

    return render(request, 'leagues/league_form.html', {
        'form': form,
        'page_title': 'Create League',
        'action': 'Create'
    })


@login_required
def league_update(request, pk):
    """
    Updates an existing league. Only the organizer can edit.
    """
    league = get_object_or_404(League, pk=pk)

    if league.organizer != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit this league.')
        return redirect('league_detail', pk=pk)

    if request.method == 'POST':
        form = LeagueForm(request.POST, request.FILES, instance=league)
        if form.is_valid():
            form.save()
            messages.success(request, f'League "{league.name}" updated successfully!')
            return redirect('league_detail', pk=league.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = LeagueForm(instance=league)

    return render(request, 'leagues/league_form.html', {
        'form': form,
        'league': league,
        'page_title': 'Edit League',
        'action': 'Update'
    })


@login_required
def league_delete(request, pk):
    """
    Deletes a league. Only the organizer or staff can delete.
    """
    league = get_object_or_404(League, pk=pk)

    if league.organizer != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this league.')
        return redirect('league_detail', pk=pk)

    if request.method == 'POST':
        league_name = league.name
        league.delete()
        messages.success(request, f'League "{league_name}" has been deleted.')
        return redirect('league_list')

    return render(request, 'leagues/league_confirm_delete.html', {
        'league': league,
        'page_title': 'Delete League'
    })


@login_required
def league_register(request, pk):
    """
    Registers the current user to a league.
    """
    league = get_object_or_404(League, pk=pk)

    if LeagueRegistration.objects.filter(league=league, player=request.user).exists():
        messages.warning(request, 'You are already registered for this league.')
        return redirect('league_detail', pk=pk)

    if league.spots_remaining <= 0:
        messages.error(request, 'This league is full.')
        return redirect('league_detail', pk=pk)

    LeagueRegistration.objects.create(league=league, player=request.user)
    messages.success(request, f'You have registered for {league.name}. Awaiting approval.')
    return redirect('league_detail', pk=pk)


@login_required
def record_match(request, league_pk):
    """
    Records a match result within a league.
    """
    league = get_object_or_404(League, pk=league_pk)

    if league.organizer != request.user and not request.user.is_staff:
        messages.error(request, 'Only the league organizer can record matches.')
        return redirect('league_detail', pk=league_pk)

    if request.method == 'POST':
        form = MatchResultForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.league = league
            match.save()
            messages.success(request, 'Match result recorded!')
            return redirect('league_detail', pk=league_pk)
    else:
        form = MatchResultForm()

    return render(request, 'leagues/match_form.html', {
        'form': form,
        'league': league,
        'page_title': 'Record Match'
    })