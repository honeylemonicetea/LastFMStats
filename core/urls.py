from django.urls import path
from .views import home, view_artists

urlpatterns = [
    path('', home, name='home'),
    path('artists/', view_artists, name='view_artists')
]
