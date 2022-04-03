import time

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
    params = {'owner_id': id, 'album_id': album, 'access_token': token, 'v': '5.131'}
    res = requests.get(url, params=params)
    photos = res.json()['response']['items']
    photo_big = []
    for photo in photos:
        # print(photo['sizes'])
        for p in photo['sizes']:
            if p['type'] == 'x':
                photo_big.append(p['url'])
    return photo_big

photos = get_photos(get_user_id(screen_name))

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
        for p in photos:
            params2 = {'path': f'{folder}/{file}', 'url': p}
            response = requests.post(upload_url, headers=headers, params=params2)
            pprint(response)
            time.sleep(1)


token = 'AQAAAAAnTSzNAADLW-jve_JHdkqztQk1d2ApBtE'
folder = 'Backup'
photo_name = 'date'

uploader = YaUploader(token)
result = uploader.create_folder(folder)
result2 = uploader.upload(folder, photo_name, photos)