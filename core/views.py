from django.shortcuts import render
from .tools.lastfm import authenticate, get_artists

def home(request):
    login_link = authenticate()
    token = request.GET.get('token')
    if token is not None:
        print(token)

    return render(request, 'home.html', {'last_login':login_link})

def view_artists(request):
    artists = get_artists()

    return render(request, 'artists.html', {'artists':artists})