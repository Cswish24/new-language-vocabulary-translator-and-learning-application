from socket import fromshare
from django import forms
from .models import Words
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

        

class EnWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['spanish_word', 'slug', 'tries', 'wrong_guesses', 'correct_guesses', 'percentage', 'user' ]
        labels = {
            "english_word": "English word"
        }

class EsWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['english_word', 'slug', 'tries', 'wrong_guesses', 'correct_guesses', 'percentage', 'user']
        labels = {
            "spanish_word": "Spanish word"
        }

class ManualWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['slug', 'tries', 'wrong_guesses', 'correct_guesses', 'percentage', 'user']
        labels = {
            "spanish_word": "Spanish word",
            "english_word": "English word"
        }