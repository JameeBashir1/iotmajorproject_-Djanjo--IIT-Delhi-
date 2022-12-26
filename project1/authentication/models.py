from django.db import models

# Create your models here.
class Database(models.Model):
    entry=models.FloatField(max_length=100)
