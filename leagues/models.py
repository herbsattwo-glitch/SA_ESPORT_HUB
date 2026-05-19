from django.db import models
from django.contrib.auth.models import User


class League(models.Model):
    """
    Represents an SA Esports league for a specific game title.
    """

    GAME_CHOICES = [
        ('FIFA', 'EA FC (FIFA)'),
        ('COD', 'Call of Duty'),
        ('TEKKEN', 'Tekken 8'),
        ('SF6', 'Street Fighter 6'),
        ('KI', 'Killer Instinct'),
        ('FH6', 'Forza Horizon 6'),
    ]

    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    FORMAT_CHOICES = [
        ('single_elimination', 'Single Elimination'),
        ('double_elimination', 'Double Elimination'),
        ('round_robin', 'Round Robin'),
        ('swiss', 'Swiss System'),
        ('group_stage', 'Group Stage + Playoffs'),
    ]

    name = models.CharField(max_length=150)
    game = models.CharField(max_length=20, choices=GAME_CHOICES)
    description = models.TextField()
    organizer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='organized_leagues'
    )
    format = models.CharField(max_length=30, choices=FORMAT_CHOICES, default='single_elimination')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    max_participants = models.PositiveIntegerField(default=16)
    prize_pool = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    registration_deadline = models.DateField(null=True, blank=True)
    banner = models.ImageField(upload_to='league_banners/', blank=True, null=True)
    rules = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'League'
        verbose_name_plural = 'Leagues'

    def __str__(self):
        return f'{self.name} ({self.get_game_display()})'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('league_detail', kwargs={'pk': self.pk})

    @property
    def participant_count(self):
        return self.registrations.filter(status='approved').count()

    @property
    def spots_remaining(self):
        return self.max_participants - self.participant_count


class LeagueRegistration(models.Model):
    """
    Tracks a player's registration to a specific league.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='registrations')
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='league_registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    registered_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['league', 'player']
        verbose_name = 'League Registration'
        verbose_name_plural = 'League Registrations'

    def __str__(self):
        return f'{self.player.username} -> {self.league.name} ({self.status})'


class Match(models.Model):
    """
    Stores individual match results within a league.
    """

    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='matches')
    player_one = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='matches_as_p1'
    )
    player_two = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='matches_as_p2'
    )
    winner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_matches'
    )
    score_p1 = models.PositiveIntegerField(default=0)
    score_p2 = models.PositiveIntegerField(default=0)
    round_number = models.PositiveIntegerField(default=1)
    played_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'
        ordering = ['round_number', 'played_at']

    def __str__(self):
        return f'{self.player_one.username} vs {self.player_two.username} | {self.league.name}'