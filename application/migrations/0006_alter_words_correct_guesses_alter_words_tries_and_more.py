# Generated by Django 4.0.4 on 2022-09-12 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_words_correct_guesses_words_tries_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='correct_guesses',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='words',
            name='tries',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='words',
            name='wrong_guesses',
            field=models.FloatField(default=0),
        ),
    ]
