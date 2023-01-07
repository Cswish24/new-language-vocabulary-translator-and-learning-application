from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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

class UserExtended(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    word_count = models.SmallIntegerField(default=0)

@receiver(post_save, sender=User)
def create_user_extended(sender, instance, created, **kwargs):
    if created:
        UserExtended.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_extended(sender, instance, **kwargs):
#     instance.profile.save()