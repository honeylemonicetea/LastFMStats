import base64
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth, AuthBase

WEB_API_SPOT = 'https://api.spotify.com/v1/search'

# spotify authorization todo: HIDE THIS STUFFF
CLIENT_ID = '9d2f324bb97448f49098149ce32f793e'
CLIENT_SECRET = '85877416e6264ca39ed4f55fb4e8fe3d'
REDIRECT_URI = 'http://localhost/'
TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'

bytes_id = CLIENT_ID.encode('ascii')
base_id = base64.urlsafe_b64encode(bytes_id)
bytes_secret = CLIENT_SECRET.encode('ascii')
base_secret = base64.urlsafe_b64encode(bytes_secret)
auth_header = {
    'Content-Type':'application/x-www-form-urlencoded'
}


def client_cred():
    resp = requests.post(TOKEN_ENDPOINT, params={'grant_type':'client_credentials','client_id':CLIENT_ID, 'client_secret':CLIENT_SECRET}, headers=auth_header)
    response = resp.json()
    token = response['access_token']
    return token



def get_artist_image(name):  #SPOTIFY
    token = client_cred()
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    get_art = requests.get(WEB_API_SPOT, params={'q':name, 'type':'artist'}, headers=headers)
    artist_info = get_art.json()
    return artist_info['artists']['items'][0]['images'][0]['url']


# print(get_artist_image('blaqk audio'))


