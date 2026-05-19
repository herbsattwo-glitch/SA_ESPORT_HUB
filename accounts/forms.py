from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile


class XboxRegistrationForm(UserCreationForm):
    """
    Custom registration form with Xbox Gamertag and profile fields.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control xbox-input',
            'placeholder': 'your@email.com'
        })
    )
    gamertag = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control xbox-input',
            'placeholder': 'Your Xbox Gamertag'
        })
    )
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select xbox-input'})
    )
    province = forms.ChoiceField(
        choices=[('', 'Select Province')] + UserProfile.PROVINCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select xbox-input'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control xbox-input',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control xbox-input',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control xbox-input',
            'placeholder': 'Confirm Password'
        })

    def clean_gamertag(self):
        gamertag = self.cleaned_data.get('gamertag')
        if UserProfile.objects.filter(gamertag__iexact=gamertag).exists():
            raise forms.ValidationError('This Gamertag is already taken. Choose another.')
        return gamertag

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                gamertag=self.cleaned_data['gamertag'],
                role=self.cleaned_data['role'],
                province=self.cleaned_data.get('province', ''),
            )
        return user


class XboxLoginForm(AuthenticationForm):
    """
    Styled login form matching Xbox theme.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control xbox-input',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control xbox-input',
            'placeholder': 'Password'
        })


class UserProfileUpdateForm(forms.ModelForm):
    """
    Allows users to update their profile information.
    """
    class Meta:
        model = UserProfile
        fields = ['gamertag', 'avatar', 'role', 'province', 'bio', 'xbox_profile_url']
        widgets = {
            'gamertag': forms.TextInput(attrs={'class': 'form-control xbox-input'}),
            'bio': forms.Textarea(attrs={'class': 'form-control xbox-input', 'rows': 4}),
            'role': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'province': forms.Select(attrs={'class': 'form-select xbox-input'}),
            'xbox_profile_url': forms.URLInput(attrs={'class': 'form-control xbox-input'}),
        }


class UserUpdateForm(forms.ModelForm):
    """
    Allows users to update core User model fields.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control xbox-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control xbox-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control xbox-input'}),
        }