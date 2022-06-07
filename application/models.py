from django.db import models
# Create your models here.

class Words(models.Model):
    id = models.BigAutoField(db_index=True, primary_key=True)
    english_word=models.CharField(max_length=40)
    spanish_word=models.CharField(max_length=40)
    category=models.CharField(max_length=40, null=True)

