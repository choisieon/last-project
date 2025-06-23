from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.apps import apps

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', )

class CustomAuthenticationForm(AuthenticationForm):
    pass

class UserProfileForm(forms.ModelForm):
    concerns = forms.ModelMultipleChoiceField(
        queryset=None,  # 초기엔 비워두고
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            'nickname',
            'role',
            'interests',
            'keywords',
            'profile_image',
            'concerns',
            'age',
            'job',
            'points',
            'tagline',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Concern = apps.get_model('mentor', 'Concern')
        self.fields['concerns'].queryset = Concern.objects.all()