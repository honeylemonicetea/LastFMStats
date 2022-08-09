from django.db import models

# Create your models here.
class LastfmUser(models.Model):
    user_name = models.CharField(max_length=150)
    api_token = models.CharField(max_length=200)
    date = models.DateField()

class Artist(models.Model):
    name = models.CharField(max_length=100)
    photo_url = models.URLField(default='https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png')
    last_fm_link = models.URLField(default='https://www.last.fm/')
    country = models.CharField(max_length=100, default='Unknown')
    country_flag_url = models.URLField(default='')

    def __str__(self):
        return self.name




