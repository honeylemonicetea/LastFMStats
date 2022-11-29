from django.shortcuts import render
from .tools.lastfm import  get_artists, get_albums, get_top_tracks, get_user

PERIOD_DICT = {
    '7day': "7 days",
    "1month":"1 month",
    "3month":"3 months",
    "6month":"6 months",
    "12month":"12 months",
    "overall":"Overall"
}

def home(request):

    return render(request, 'home.html')

def view_artists(request):
    if request.method == 'GET':
        return render(request, 'artists.html')
    elif request.method == 'POST':
        print(request.POST)
        try:
            username = request.POST['username']
            grid_size = int(request.POST['grid'])
            period = request.POST['period']
            period_verbose = PERIOD_DICT.get(period)
            size_verbose = f'{grid_size}x{grid_size}'
            try:
                overlay = request.POST['overlay']
            except Exception:
                overlay = 'off'
            artists =   get_artists(username, grid_size, period)
            print(artists)
            if artists:
                greeting = f'Hi, {username}, here is your Top {grid_size**2} artists grid'
            else:
                greeting = "Couldn't find the user"
            return  render(request, 'artists.html', {'artists':artists, 'greeting':greeting, 'overlay':overlay,
                                                 'size': grid_size, 'period': period,
                                                 'period_verbose':period_verbose,"size_verbose":size_verbose,
                                                 "username": username})
        except Exception:
            greeting = "The information you have entered is incorrect. Please, try again"
            return render(request, "artists.html", {"greeting":greeting})



def view_albums(request):
    if request.method == 'GET':
        return render(request, 'albums.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            grid_size = int(request.POST['grid'])
            period = request.POST['period']
            period_verbose = PERIOD_DICT.get(period)
            size_verbose = f'{grid_size}x{grid_size}'
            try:
                overlay = request.POST['overlay']
            except Exception:
                overlay = 'off'
            albums = get_albums(username, grid_size, period)
            if albums:
                greeting = f'Hi, {username}, here is your Top {grid_size**2} albums grid'
            else:
                greeting = "Couldn't find the user"
            return render(request, 'albums.html', {'albums': albums, "username":username, 'greeting': greeting,
                                                   'overlay':overlay, "period": period,
                                                   'size': grid_size, "period_verbose":period_verbose, "size_verbose":
                                                       size_verbose})
        except Exception:
            greeting = "The information you have entered is incorrect. Please, try again"
            return render(request, 'albums.html', { 'greeting': greeting})

def view_tracks(request):
    if request.method == 'GET':
        return render(request, 'tracks.html')
    elif request.method == 'POST':
        try:
            username = request.POST['username']
            quantity = int(request.POST['quantity'])
            period = request.POST['period']
            period_verbose = PERIOD_DICT.get(period)
            track_list = get_top_tracks(username, quantity, period)
            if track_list:
                greeting = f'Hi, {username}, here is your Top {quantity} tracks chart'
            else:
                greeting = "Couldn't find the user"
            return render(request, 'tracks.html', {'tracks': track_list, 'greeting': greeting, 'quantity':quantity,
                                                   "username": username, "period":period, "period_verbose": period_verbose})
        except Exception:
            greeting = "The information you have entered is incorrect. Please, try again"
            return render(request, 'tracks.html', {'greeting': greeting})



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
        return render(request, 'profile.html', {'user_info':user_info, "message": message, "username":username})


def under_construction(request):

    return render(request, 'UnderConstr.html')