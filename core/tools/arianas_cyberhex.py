import requests
import time
import _md5

ARIANA_API = 'ba40191a93dd7dafa6b5e626a13b378c'
ARIANA_SECRET = '6a760750f4a64d9a9ad69db0f04e75d3'
AUTH_ROOT='http://www.last.fm/api/auth/'
API_ROOT='http://ws.audioscrobbler.com/2.0/'

TOKEN = 'cCK5odeEhsX8cK0JG_W2mPV71VOK-Sls'


def authenticate():  #for last fm
    r = requests.get(AUTH_ROOT, params={'api_key':ARIANA_API})
    return r.url

method = 'track.updateNowPlaying'

signature = f'api_key{ARIANA_API}method{method}token{TOKEN}{ARIANA_SECRET}'
signature = signature.encode('utf-8')

hash_sig = _md5.md5(signature)

def scrobble(artist, track, album=''):
    req = requests.post(API_ROOT, params={'artist':artist, 'track':track, 'album':album, 'api_key': ARIANA_API, 'api_sig':hash_sig, 'sk':TOKEN, 'method':method})
    print(req.status_code)
    print(req.content)

scrobble('Ed Sheeran', 'Shivers', '=')


