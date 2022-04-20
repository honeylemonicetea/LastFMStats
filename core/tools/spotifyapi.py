import base64
import requests
import environ

WEB_API_SPOT = 'https://api.spotify.com/v1/search'
REDIRECT_URI = 'http://localhost/'
TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

env = environ.Env()
environ.Env.read_env('D:/Coding/PycharmProjects/NEW OWN PROJECTS/LASTFMKITTY/lastfmkitty/.env')

bytes_id = env('CLIENT_ID').encode('ascii')
base_id = base64.urlsafe_b64encode(bytes_id)
bytes_secret = env('CLIENT_SECRET').encode('ascii')
base_secret = base64.urlsafe_b64encode(bytes_secret)
auth_header = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

def client_cred():
    resp = requests.post(TOKEN_ENDPOINT, params={'grant_type': 'client_credentials', 'client_id':env('CLIENT_ID'),
                                                 'client_secret': env('CLIENT_SECRET')}, headers=auth_header)
    response = resp.json()
    token = response['access_token']
    return token


def get_artist_image(name):  # SPOTIFY
    token = client_cred()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    get_art = requests.get(WEB_API_SPOT, params={'q': name, 'type': 'artist'}, headers=headers)
    artist_info = get_art.json()
    return artist_info['artists']['items'][0]['images'][0]['url']


def get_track_info(track_name, artist):
    token = client_cred()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    get_art = requests.get(WEB_API_SPOT, params={'q': f"{track_name} {artist}", 'type': 'track', 'limit': 1},
                           headers=headers)
    track_info = get_art.json()

    album_name = track_info['tracks']['items'][0]['album']['name']
    album_cover = track_info['tracks']['items'][0]['album']['images'][0]['url']
    return album_name, album_cover
