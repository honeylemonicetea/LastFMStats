# write some instruction here dumbass


# LIBRARY IMPORTS ARE HERE
import requests
import environ
import time
import base64
from .spotify_authorization import get_artist_image
env = environ.Env()
environ.Env.read_env('D:/Coding/PycharmProjects/NEW OWN PROJECTS/LASTFMKITTY/lastfmkitty/.env')

# CONsTANTS
API_ROOT='http://ws.audioscrobbler.com/2.0/'
CALLBACK_URL='http://127.0.0.1:8000/'
AUTH_ROOT='http://www.last.fm/api/auth/'


# HEY BELLA! The apps you've created on last fm are here: https://www.last.fm/api/accounts


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}

def authenticate():  #for last fm
    r = requests.get(AUTH_ROOT, params={'api_key':env('API_KEY')})
    return r.url

def get_artists():
    artists = []
    r = requests.get(API_ROOT, params={'api_key':env('API_KEY'), 'user':'BellaLeto', 'format':'json', 'method':'library.getartists', 'limit':'100'})
    content = r.json()
    for i in range(100):
        artist_info = dict()
        artist_name = content['artists']['artist'][i]['name']
        artist_playcount = content['artists']['artist'][i]['playcount']
        artist_url = content['artists']['artist'][i]['url']
        try:
            artist_image = get_artist_image(artist_name)
        except Exception:
            artist_image = 'https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png'
        # print(artist_name, artist_playcount, artist_url, artist_image)
        artist_info['id'] = i+1
        artist_info['artist_name'] = artist_name
        artist_info['playcount'] = artist_playcount
        artist_info['artist_url'] = artist_url
        artist_info['artist_image'] = artist_image
        artists.append(artist_info)
    return artists



# LAST FM RESTRICTED ACCESS TO ARTIST IMAGES!! TRY USING SPOTIFY

# getting artist images from spotify
