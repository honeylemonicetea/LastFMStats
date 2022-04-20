import pylast

import time
import datetime


# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = 'ba40191a93dd7dafa6b5e626a13b378c'  # this is a sample key
API_SECRET = '6a760750f4a64d9a9ad69db0f04e75d3'

# In order to perform a write operation you need to authenticate yourself
username = "arinna_2012"
pw = 'HeyThereDelilah$2008'


password_hash = pylast.md5(pw)

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

# Now you can use that object everywhere


user = network.get_user(username)
# top_week = user.get_top_artists(limit=100, period=pylast.PERIOD_OVERALL)
# artists = []
# for top in top_week:
#     artists.append(top.item.name)
#     print(type(top))
# print(artists)
# songs_week = user.get_top_tracks(period=pylast.PERIOD_7DAYS, limit=6)
# for top in songs_week:
#     print(top.item, top.weight)



def scrobble(artist, track, times, album=''):
    for i in range(times):
        time.sleep(0.5)
        arts = network.scrobble(artist, track, timestamp=time.time(), album=album)
        print(arts)

# Type help(pylast.LastFMNetwork) or help(pylast) in a Python interpreter
# to get more help about anything and see examples of how it works



scrobble('Ed Sheeran', 'Bad Habits',1000, album='=')

