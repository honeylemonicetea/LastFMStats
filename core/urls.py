from django.urls import path
from .views import home, view_artists, view_albums, testing_forms, view_tracks, view_profile

urlpatterns = [
    path('', home, name='home'),
    path('artists/', view_artists, name='view_artists'),
    path('albums/', view_albums, name='view_albums'),
    path('test/', testing_forms, name='form'),
    path('tracks/', view_tracks, name='tracks'),
    path('profile/', view_profile, name='profile')

]
