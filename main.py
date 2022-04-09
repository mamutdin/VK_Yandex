import time
import json
from tqdm import tqdm
import requests
from pprint import pprint



screen_name = 'begemot_korovin'
def get_user_id(name=str):
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    url = 'https://api.vk.com/method/users.get'
    params = {'user_ids': name, 'access_token': token, 'v': '5.131'}
    res = requests.get(url, params=params)
    return res.json()['response'][0]['id']

def get_photos(id):
    token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    album = 'profile'
    url = 'https://api.vk.com/method/photos.get'
    params = {'owner_id': id, 'album_id': album, 'access_token': token, 'extended': 1, 'v': '5.131'}
    res = requests.get(url, params=params)
    photos = res.json()['response']['items']

    # pprint(photos)
    big_photos =[]
    photo_big = []
    for photo in photos:
        # print(photo['sizes'])
        sorted_photos = sorted(photo['sizes'], key=lambda x: x['height'])
        sorted_photos.reverse()
        sorted_photos[0]['likes'] = photo['likes']['count']
        big_photos.append(sorted_photos[0])

        photo_big.append(sorted_photos[0]['url'])

    with open('data.txt', 'w') as outfile:
        json.dump(big_photos, outfile, indent=4)

    return photo_big

photos = get_photos(get_user_id(screen_name))
pprint(photos)

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def create_folder(self, folder:str):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
        params = {'path': folder}
        r = requests.put(url, headers=headers, params=params).json()

    def upload(self, folder: str, file: str, photos:list):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                   'Authorization': f'OAuth {self.token}'}

        for p in tqdm(photos):
            params2 = {'path': f'{folder}/{file}', 'url': p}
            response = requests.post(upload_url, headers=headers, params=params2)
            time.sleep(0.5)

token = 'AQAAAAAnTSzNAADLW-jve_JHdkqztQk1d2ApBtE'
folder = 'Backup'
photo_name = 'date'

uploader = YaUploader(token)
result = uploader.create_folder(folder)
result2 = uploader.upload(folder, photo_name, photos)
