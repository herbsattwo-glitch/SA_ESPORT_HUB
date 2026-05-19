from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    """
    Extended competitive profile for a registered user.
    Tracks game-specific stats and SA regional ranking.
    """

    GAME_CHOICES = [
        ('FIFA', 'EA FC (FIFA)'),
        ('COD', 'Call of Duty'),
        ('TEKKEN', 'Tekken 8'),
        ('SF6', 'Street Fighter 6'),
        ('KI', 'Killer Instinct'),
        ('FH6', 'Forza Horizon 6'),
    ]

    SKILL_TIER_CHOICES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
        ('master', 'Master'),
        ('grandmaster', 'Grand Master'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    primary_game = models.CharField(max_length=20, choices=GAME_CHOICES)
    secondary_games = models.JSONField(default=list, blank=True)
    skill_tier = models.CharField(max_length=20, choices=SKILL_TIER_CHOICES, default='bronze')
    ranking_points = models.PositiveIntegerField(default=0)
    national_rank = models.PositiveIntegerField(null=True, blank=True)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    draws = models.PositiveIntegerField(default=0)
    tournament_wins = models.PositiveIntegerField(default=0)
    is_available_for_scouting = models.BooleanField(default=True)
    looking_for_team = models.BooleanField(default=False)
    highlights_url = models.URLField(blank=True, help_text='YouTube/Twitch highlight reel')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-ranking_points']
        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __str__(self):
        gamertag = getattr(self.user, 'profile', None)
        tag = gamertag.gamertag if gamertag else self.user.username
        return f'{tag} | {self.get_primary_game_display()} | {self.get_skill_tier_display()}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('player_detail', kwargs={'pk': self.pk})

    @property
    def total_matches(self):
        return self.wins + self.losses + self.draws

    @property
    def win_rate(self):
        if self.total_matches == 0:
            return 0
        return round((self.wins / self.total_matches) * 100, 1)


class ScoutingReport(models.Model):
    """
    A scout's evaluation of a player.
    """

    RATING_CHOICES = [(i, str(i)) for i in range(1, 11)]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='scouting_reports')
    scout = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_reports')
    overall_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    mechanics_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    game_sense_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    consistency_rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    notes = models.TextField()
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['player', 'scout']
        verbose_name = 'Scouting Report'
        verbose_name_plural = 'Scouting Reports'

    def __str__(self):
        return f'Report on {self.player} by {self.scout.username}'

    @property
    def average_rating(self):
        total = (
            self.overall_rating +
            self.mechanics_rating +
            self.game_sense_rating +
            self.consistency_rating
        )
        return round(total / 4, 1)