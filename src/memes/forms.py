from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from memes.models import MemePost

User = get_user_model()


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)


class MemeUploadForm(forms.ModelForm):
    class Meta:
        model = MemePost
        fields = ('image', 'description')
