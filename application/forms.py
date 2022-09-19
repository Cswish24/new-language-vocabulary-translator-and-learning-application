from socket import fromshare
from django import forms
from .models import Words

class EnWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['spanish_word', 'slug', 'tries', 'wrong_guesses', 'correct_guesses', 'percentage' ]
        labels = {
            "english_word": "English word"
        }

class EsWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['english_word', 'slug', 'tries', 'wrong_guesses', 'correct_guesses', 'percentage']
        labels = {
            "spanish_word": "Spanish word"
        }

class ManualWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['slug', 'tries', 'wrong_guesses', 'correct_guesses', 'percentage']
        labels = {
            "spanish_word": "Spanish word",
            "english_word": "English word"
        }