from django.shortcuts import render
from .tools.lastfm import  get_artists, get_albums, get_top_tracks, get_user
from .forms import LFMUser
from .models import LastfmUser
import asyncio


def home(request):
    # login_link = authenticate()
    token = request.GET.get('token')
    if token is not None:
        print(token)

    return render(request, 'home.html')

def testing_forms(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        api_token = request.POST['api_token']
        date = request.POST['date']
        LastfmUser.objects.create(user_name=user_name, api_token=api_token, date=date)

    form = LFMUser()
    return render(request, 'form_test.html', {'form': form})

def view_artists(request):
    if request.method == 'GET':
        return render(request, 'artists.html')
    elif request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        grid_size = int(request.POST['grid'])
        period = request.POST['period']
        try:
            overlay = request.POST['overlay']
        except Exception:
            overlay = 'off'
        artists =   get_artists(username, grid_size, period)
        if artists:
            greeting = f'Hi, {username}, here is your Top {grid_size**2} artists grid'
        else:
            greeting = "Couldn't find the user"

        return  render(request, 'artists.html', {'artists':artists, 'greeting':greeting, 'overlay':overlay,'size': grid_size})

def view_albums(request):
    if request.method == 'GET':
        return render(request, 'albums.html')
    elif request.method == 'POST':
        username = request.POST['username']
        grid_size = int(request.POST['grid'])
        period = request.POST['period']
        try:
            overlay = request.POST['overlay']
        except Exception:
            overlay = 'off'
        albums = get_albums(username, grid_size, period)
        if albums:
            greeting = f'Hi, {username}, here is your Top {grid_size**2} albums grid'
        else:
            greeting = "Couldn't find the user"
        return render(request, 'albums.html', {'albums': albums, 'greeting': greeting, 'overlay':overlay, 'size': grid_size })


def view_tracks(request):
    if request.method == 'GET':
        return render(request, 'tracks.html')
    elif request.method == 'POST':
        username = request.POST['username']
        quantity = int(request.POST['quantity'])
        period = request.POST['period']

        track_list = get_top_tracks(username, quantity, period)
        if track_list:
            greeting = f'Hi, {username}, here is your Top {quantity} tracks chart'
        else:
            greeting = "Couldn't find the user"
        return render(request, 'tracks.html', {'tracks': track_list, 'greeting': greeting, 'quantity':quantity})



def view_profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')
    elif request.method == 'POST':
        username = request.POST['username']
        user_info = get_user(username)
        if user_info:
            message = ''
        else:
            message = "Couldn't find the user"
        return render(request, 'profile.html', {'user_info':user_info, "message": message})


def under_construction(request):

    return render(request, 'UnderConstr.html')