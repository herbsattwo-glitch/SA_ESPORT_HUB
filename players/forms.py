from django import forms
from .models import Player, ScoutingReport


class PlayerProfileForm(forms.ModelForm):
    """
    Form for creating/editing a competitive player profile.
    """
    class Meta:
        model = Player
        fields = [
            'primary_game', 'skill_tier', 'ranking_points',
            'wins', 'losses', 'draws', 'tournament_wins',
            'is_available_for_scouting', 'looking_for_team', 'highlights_url'
        ]
        widgets = {
            'primary_game': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'skill_tier': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'ranking_points': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'wins': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'losses': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'draws': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'tournament_wins': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'highlights_url': forms.URLInput(attrs={'class': 'form-control xbox-input'}),
        }


class ScoutingReportForm(forms.ModelForm):
    """
    Form for scouts to submit player evaluations.
    """
    class Meta:
        model = ScoutingReport
        fields = [
            'overall_rating', 'mechanics_rating',
            'game_sense_rating', 'consistency_rating',
            'notes', 'is_recommended'
        ]
        widgets = {
            'overall_rating': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'mechanics_rating': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'game_sense_rating': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'consistency_rating': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control xbox-input', 'rows': 5,
                'placeholder': 'Detailed evaluation notes...'
            }),
        }


class PlayerSearchForm(forms.Form):
    """
    Search and filter form for the player directory.
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control xbox-input',
            'placeholder': 'Search by Gamertag...'
        })
    )
    game = forms.ChoiceField(
        required=False,
        choices=[('', 'All Games')] + Player.GAME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select xbox-input'})
    )
    skill_tier = forms.ChoiceField(
        required=False,
        choices=[('', 'All Tiers')] + Player.SKILL_TIER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select xbox-input'})
    )
    available_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input xbox-check'})
    )