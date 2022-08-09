import requests
import environ
import time
from datetime import datetime
from core.models import Artist

# todo: UNCOMMENT
try:
    from .spotifyapi import get_artist_image, get_track_info
    from .lastfm_images import get_image
except Exception:
    pass

env = environ.Env()
environ.Env.read_env('D:/Coding/PycharmProjects/NEW OWN PROJECTS/LASTFMKITTY/lastfmkitty/.env')

API_ROOT = 'http://ws.audioscrobbler.com/2.0/'
CALLBACK_URL = 'http://127.0.0.1:8000/'
AUTH_ROOT = 'http://www.last.fm/api/auth/'
MB_ROOT = 'https://musicbrainz.org/ws/2/'
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}


"""
    ARTISTS 
"""
def get_artists(username):
    artists = []
    start_req = time.time()  #TODO: remove
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'user': username, 'format': 'json',
                                       'method': 'library.getartists', 'limit': '100'})
    print(f'Time spend making a request to LFM {time.time() - start_req}')
    content = r.json()
    start_req = time.time()
    for i in range(100):
        try:
            artist_info = dict()
            artist_name = content['artists']['artist'][i]['name']
            artist_playcount = content['artists']['artist'][i]['playcount']
            artist_url = content['artists']['artist'][i]['url']

            # TODO: ENABLE IN DEV, GIVES TIMEOUT ERROR ON PROD
            # flag_url = get_country_flag(artist_country)

            # if the artists is in the db, get the info from there
            try:
                st = time.time()
                artist_db = Artist.objects.get(name=artist_name)
                artist_image = artist_db.photo_url
                flag = artist_db.country_flag_url
            except Exception:
                artist_image = get_artist_image(artist_name)  # gets the image from spotify
                country, flag = get_more_inf_ART(artist_name)
                print(f'Time spent on getting one artist pic from spotify {time.time() - st}')

                new_artist = Artist.objects.create(name=artist_name, photo_url=artist_image, last_fm_link=artist_url,
                                                   country = country, country_flag_url = flag)
                new_artist.save()

            artist_info['id'] = i + 1
            artist_info['artist_name'] = artist_name
            artist_info['playcount'] = artist_playcount
            artist_info['artist_url'] = artist_url
            artist_info['artist_image'] = artist_image
            artist_info['flag'] = flag
            artists.append(artist_info)
        except IndexError:
            print('index error')
    print(f'Time spent compiling the dictionary {time.time() - start_req}')
    return artists

def get_top3_ART(username='BellaLeto'):
    top_3_artists = []
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'user': username, 'format': 'json',
                                       'method': 'user.gettopartists', 'period': 'overall', 'limit': '3'})
    content = r.json()
    number_one = ''
    image_one = ''
    for i in range(3):
        artist_info = dict()
        artist_name = content['topartists']['artist'][i]['name']
        artist_playcount = content['topartists']['artist'][i]['playcount']
        artist_url = content['topartists']['artist'][i]['url']
        try:
            # artist_image, code = get_image(artist_name)
            # if code != 200:

            artist_db = Artist.objects.get(name=artist_name)
            artist_image = artist_db.photo_url
            artist_country = artist_db.country


        except Exception:
            # artist_image = get_artist_image(artist_name)
            artist_image = 'https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png'
            artist_country = 'Unknown'

        artst_more = time.time()
        # artist_country, artist_city, artist_begin, artist_end, inactive = get_mb_info(artist_name)
        # flag_url = get_country_flag(artist_country)

        artist_info['id'] = i + 1
        artist_info['artist_name'] = artist_name
        artist_info['playcount'] = artist_playcount
        artist_info['artist_url'] = artist_url
        artist_info['artist_image'] = artist_image
        artist_info['country'] = artist_country
        # artist_info['flag_url'] = flag_url


        top_3_artists.append(artist_info)
        print(f"GETTING more info artist {time.time() - artst_more}")

    return top_3_artists

def get_more_inf_ART(artist_name):
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'artist': artist_name, 'format': 'json',
                                       'method': 'artist.getInfo', 'autocorrect': '1'})
    info = r.json()

    # listeners = int(info['artist']['stats']['listeners'])
    # playcount = int(info['artist']['stats']['playcount'])
    # ratio = playcount // listeners

    time.sleep(0.1)  # 50 reqs per second limit
    r = requests.get(f"{MB_ROOT}artist?", headers=headers, params={'query': artist_name, 'fmt': 'json'})
    json_data = r.json()['artists'][0]
    artist_id = json_data['id']
    try:
        artist_country = json_data['area']['name']
    except Exception:
        artist_country = 'Unknown'
    if artist_country != 'Unknown':
        country_names = requests.get('https://flagcdn.com/en/codes.json')
        country_names = country_names.json()
        flag_url = 'None'
        for code, country in country_names.items():
            if country == artist_country:
                flag_url = f'https://flagcdn.com/w40/{code}.png'
                break
    else:
        flag_url = ''

    return artist_country, flag_url





def get_albums(username):
    albums = []
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'user': username, 'format': 'json',
                                       'method': 'user.gettopalbums', 'period': 'overall', 'limit': '100'})
    content = r.json()
    for i in range(100):
        album_info = dict()
        album_title = content['topalbums']['album'][i]['name']
        album_playcount = content['topalbums']['album'][i]['playcount']
        album_url = content['topalbums']['album'][i]['url']
        album_image = content['topalbums']['album'][i]['image'][3]['#text']
        artist_name = content['topalbums']['album'][i]['artist']['name']
        album_info['id'] = i + 1
        album_info['album_name'] = album_title
        album_info['playcount'] = album_playcount
        album_info['album_url'] = album_url
        album_info['album_image'] = album_image
        album_info['artist'] = artist_name
        albums.append(album_info)
    # TODO: FOR TESTING
    # with open("ALBUMS.json", 'w', encoding='utf-8') as file:
    #     file.write(str(albums))

    return albums


def album_more_info(album_name, artist_name):
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'artist': artist_name, 'format': 'json',
                                       'method': 'album.getInfo', 'album': album_name})
    content = r.json()
    listener_count = content['album']['listeners']
    playcount = content['album']['playcount']
    ratio = int(playcount) // int(listener_count)
    description = content['album']['wiki']['content']

    return playcount, listener_count, ratio, description


def top_three_albums(username):
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'user': username, 'format': 'json',
                                       'method': 'user.gettopalbums', 'period': 'overall', 'limit': '3'})
    content = r.json()
    two_albs = []
    top_one = dict()
    for i in range(3):
        album_info = dict()
        album_title = content['topalbums']['album'][i]['name']
        album_playcount = content['topalbums']['album'][i]['playcount']
        album_url = content['topalbums']['album'][i]['url']
        album_image = content['topalbums']['album'][i]['image'][3]['#text']
        artist_name = content['topalbums']['album'][i]['artist']['name']
        if i == 0:
            top_one['id'] = i + 1
            top_one['album_name'] = album_title
            top_one['your_playcount'] = album_playcount  # user's playcount
            top_one['album_url'] = album_url
            top_one['album_image'] = album_image
            playcount, listener_count, ratio, description = album_more_info(album_title, artist_name)
            top_one['playcount'] = playcount  # total playcount
            top_one['ratio'] = ratio
            top_one['listener_count'] = listener_count
            top_one['description'] = description
            top_one['artist'] = artist_name
        else:
            album_info['id'] = i + 1
            album_info['album_name'] = album_title
            album_info['playcount'] = album_playcount
            album_info['album_url'] = album_url
            album_info['album_image'] = album_image
            album_info['artist'] = artist_name
            two_albs.append(album_info)
    # TODO: FOR TESTING
    # with open("TWO_AL.json", 'w', encoding='utf-8') as file:
    #     file.write(str(two_albs))
    # with open("one_AL.json", 'w',  encoding='utf-8') as file:
    #     file.write(str(top_one))

    return two_albs, top_one

# gets more info on the artist




def get_top_tracks(username):
    r = requests.get(API_ROOT, params={'api_key': env('API_KEY'), 'user': username, 'format': 'json',
                                       'method': 'user.getTopTracks', 'period': 'overall', 'limit': '100'})
    content = r.json()['toptracks']['track']
    tracks = []
    for i in range(100):
        try:
            track = dict()
            your_playcount = content[i]['playcount']
            track_name = content[i]['name']
            artist_name = content[i]['artist']['name']
            try:
                album_name, album_cover = get_track_info(track_name, artist_name)
            except Exception:
                album_name = 'Unknown'
                album_cover = 'https://lastfm.freetls.fastly.net/i/u/300x300/2a96cbd8b46e442fc41c2b86b821562f.png'
            track['num'] = i + 1
            track['name'] = track_name
            track['playcount'] = your_playcount
            track['artist'] = artist_name
            track['album_name'] = album_name
            track['album_cover'] = album_cover
            tracks.append(track)
        except IndexError:
            print('index error')

    return tracks



def get_user(username):
    r = requests.post(API_ROOT, params={'api_key': env('API_KEY'), 'user': username, 'format': 'json',
                                        'method': 'user.getInfo'})
    user_data = r.json()['user']
    user_country = user_data['country']
    # country_flag = get_country_flag(user_country)
    user_age = user_data['age']
    user_playcount = user_data['playcount']
    user_name = user_data['realname']
    user_image = user_data['image'][3]['#text']
    registered = float(user_data['registered']['unixtime'])

    string_date = datetime.utcfromtimestamp(registered).strftime('%m/%d/%Y')

    user_url = user_data['url']
    user_gender = user_data['gender']
    user_type = user_data['type']
    user_dict = {
        'username': username,
        'country': user_country,
        'age': user_age,
        'playcount': user_playcount,
        'realName': user_name,
        'image': user_image,
        'registered': string_date,
        'user_url': user_url,
        'user_gender': user_gender,
        'user_type': user_type
    }
    return user_dict


# musicbrainz     fmt=json

# entity types:  area, artist, event, genre, instrument, label, place, recording, release, release - group, series, work, url
#  lookup:   /<ENTITY_TYPE>/<MBID>?inc=<INC>
#  browse:   /<RESULT_ENTITY_TYPE>?<BROWSING_ENTITY_TYPE>=<MBID>&limit=<LIMIT>&offset=<OFFSET>&inc=<INC>
#  search:   /<ENTITY_TYPE>?query=<QUERY>&limit=<LIMIT>&offset=<OFFSET>


# def get_country(artist_name):
#     time.sleep(0.1)  # 50 reqs per second limit
#     r = requests.get(f"{MB_ROOT}artist?", headers=headers, params={'query': artist_name, 'fmt': 'json'})
#     json_data = r.json()['artists'][0]
#     artist_id = json_data['id']
#     # try:
#     #     artist_city = json_data['begin-area']['name']
#     # except Exception:
#     #     artist_city = 'Unknown'
#     # try:
#     #     artist_begin = json_data['life-span']['begin']
#     # except Exception:
#     #     artist_begin = 'Unknown'
#     # try:
#     #     artist_end = json_data['life-span']['end']
#     #     inactive = json_data['life-span']['ended']
#     # except Exception:
#     #     artist_end = False
#     #     inactive = False
#     try:
#         artist_country = json_data['area']['name']
#     except Exception:
#         artist_country = 'Unknown'
#
#     return artist_country
