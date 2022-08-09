from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('artists/', view_artists, name='view_artists'),
    path('albums/', view_albums, name='view_albums'),
    path('test/', testing_forms, name='form'),
    path('tracks/', view_tracks, name='tracks'),
    path('profile/', view_profile, name='profile'),
    path('construction/', under_construction, name='under_construction')

]
