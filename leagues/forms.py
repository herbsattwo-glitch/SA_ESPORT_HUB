from django import forms
from .models import League, Match, LeagueRegistration


class LeagueForm(forms.ModelForm):
    """
    Form for creating and editing leagues.
    """
    class Meta:
        model = League
        fields = [
            'name', 'game', 'description', 'format',
            'max_participants', 'prize_pool',
            'start_date', 'end_date', 'registration_deadline',
            'banner', 'rules', 'status'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control xbox-input',
                'placeholder': 'League Name'
            }),
            'game': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control xbox-input', 'rows': 4
            }),
            'format': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'prize_pool': forms.NumberInput(attrs={
                'class': 'form-control xbox-input',
                'step': '0.01'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'form-control xbox-input', 'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control xbox-input', 'type': 'date'
            }),
            'registration_deadline': forms.DateInput(attrs={
                'class': 'form-control xbox-input', 'type': 'date'
            }),
            'rules': forms.Textarea(attrs={
                'class': 'form-control xbox-input', 'rows': 5
            }),
            'status': forms.Select(attrs={'class': 'form-select xbox-input'}),
        }


class MatchResultForm(forms.ModelForm):
    """
    Form for recording match results.
    """
    class Meta:
        model = Match
        fields = ['score_p1', 'score_p2', 'winner', 'notes', 'is_completed']
        widgets = {
            'score_p1': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'score_p2': forms.NumberInput(attrs={'class': 'form-control xbox-input'}),
            'winner': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control xbox-input', 'rows': 3
            }),
        }


class LeagueSearchForm(forms.Form):
    """
    Search and filter form for the league listing page.
    """
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control xbox-input',
            'placeholder': 'Search leagues...'
        })
    )
    game = forms.ChoiceField(
        required=False,
        choices=[('', 'All Games')] + League.GAME_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select xbox-input'})
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All Statuses')] + League.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select xbox-input'})
    )