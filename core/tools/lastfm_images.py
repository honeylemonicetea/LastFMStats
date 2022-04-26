import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://www.last.fm/music/'
IMAGE_BASE = 'https://lastfm.freetls.fastly.net/i/u/770x0/'

def get_image(artist_name):
    if " " in artist_name:
        artist_name = artist_name.replace(" ", "+")
    response = requests.get(f"{BASE_URL}{artist_name}")
    soup = BeautifulSoup(response.text, 'lxml')
#         header-new-gallery--link    class
    element = soup.find(class_ = 'header-new-gallery--link')
    pattern = f'/music/{artist_name}/+images/'
    element_url = element['href']
    image_token = element_url.replace(pattern, '')
    final_url = f'{IMAGE_BASE}{image_token}.jpg'
    check_im = requests.get(final_url)
    image_status = check_im.status_code
    return final_url, image_status
