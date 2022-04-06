from django.db import models

# Create your models here.
class LastfmUser(models.Model):
    user_name = models.CharField(max_length=150)
    api_token = models.CharField(max_length=200)
