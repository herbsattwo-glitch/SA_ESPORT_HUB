from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Extended profile for every registered user.
    Stores Xbox Gamertag and role information.
    """

    ROLE_CHOICES = [
        ('player', 'Player'),
        ('scout', 'Scout'),
        ('organizer', 'League Organizer'),
        ('spectator', 'Spectator'),
    ]

    PROVINCE_CHOICES = [
        ('GP', 'Gauteng'),
        ('WC', 'Western Cape'),
        ('KZN', 'KwaZulu-Natal'),
        ('EC', 'Eastern Cape'),
        ('FS', 'Free State'),
        ('LP', 'Limpopo'),
        ('MP', 'Mpumalanga'),
        ('NC', 'Northern Cape'),
        ('NW', 'North West'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    gamertag = models.CharField(max_length=50, unique=True, help_text='Your Xbox Gamertag')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='spectator')
    province = models.CharField(max_length=3, choices=PROVINCE_CHOICES, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    xbox_profile_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f'{self.gamertag} ({self.user.username})'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('profile', kwargs={'pk': self.pk})