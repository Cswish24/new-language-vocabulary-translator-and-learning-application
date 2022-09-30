from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Words(models.Model):
    id = models.BigAutoField(db_index=True, primary_key=True)
    english_word = models.CharField(max_length=40)
    spanish_word = models.CharField(max_length=40)
    category = models.CharField(max_length=40, null=True)
    tries = models.FloatField(default=0)
    wrong_guesses = models.FloatField(default=0)
    correct_guesses = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
    user = models.ManyToManyField(User, through='UsersWords')
    

class UsersWords(models.Model):
    words_id = models.ForeignKey(Words, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tries = models.FloatField(default=0)
    wrong_guesses = models.FloatField(default=0)
    correct_guesses = models.FloatField(default=0)
    percentage = models.FloatField(default=0)
