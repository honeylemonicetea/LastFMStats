from django.shortcuts import render
from .tools.lastfm import  get_artists, get_albums, get_top3_ART, get_more_inf_ART, top_three_albums, get_top_tracks, get_user
from .forms import LFMUser
from .models import LastfmUser


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
        username = request.POST['username']
        artists = get_artists(username)
        top_three, number_one, image_one, playcount_one = get_top3_ART(username)
        # info about the number one artist
        top_one_dict= get_more_inf_ART(number_one)
        greeting = f'Hi, {username}, here is your Top 100 artists grid'


        return render(request, 'artists.html', {'artists':artists, 'greeting':greeting,  'top_two':top_three, 'one_name':number_one, 'top_one_dict':top_one_dict, 'one_pic':image_one, 'playcount_one':playcount_one})

def view_albums(request):
    if request.method == 'GET':
        return render(request, 'albums.html')
    elif request.method == 'POST':
        username = request.POST['username']
        albums = get_albums(username)
        greeting = f'Hi, {username}, here is your Top 100 albums grid'
        two_albs, top_one = top_three_albums(username)


        return render(request, 'albums.html', {'albums': albums, 'greeting': greeting, 'two_albs': two_albs, 'top_one':top_one })


def view_tracks(request):
    if request.method == 'GET':
        return render(request, 'tracks.html')
    elif request.method == 'POST':
        username = request.POST['username']
        greeting = f'Hi, {username}, here is your Top 100 tracks chart'
        track_list = get_top_tracks(username)


        return render(request, 'tracks.html', {'tracks': track_list, 'greeting': greeting})



def view_profile(request):
    if request.method == 'GET':
        return render(request, 'profile.html')
    elif request.method == 'POST':
        username = request.POST['username']
        user_info = get_user(username)
        return render(request, 'profile.html', {'user_info':user_info})