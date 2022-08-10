# Generated by Django 4.0.3 on 2022-08-09 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_artist_biography_remove_artist_birth_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='country',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='artist',
            name='country_flag_url',
            field=models.URLField(default=''),
        ),
    ]