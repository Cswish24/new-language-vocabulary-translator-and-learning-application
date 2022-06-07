from socket import fromshare
from django import forms
from .models import Words

class EnWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['spanish_word', 'slug']
        labels = {
            "english_word": "English word"
        }

class EsWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['english_word', 'slug']
        labels = {
            "spanish_word": "Spanish word"
        }

class ManualWordForm(forms.ModelForm):
    class Meta:
        model = Words
        exclude = ['slug']
        labels = {
            "spanish_word": "Spanish word",
            "english_word": "English word"
        }