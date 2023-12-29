from dotenv import load_dotenv
import os
import base64
from requests import get, post
import json

load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
user_id = os.getenv('SPOTIFY_USER_ID')

def get_token():
    auth_string = f'{client_id}:{client_secret}'
    auth_string = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_string), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    result = json.loads(result.content)
    return result['access_token']

def get_auth_header(token):
    return {"Authorization": "Bearer "+ token}

def get_user_id(token):
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    result = json.loads(result.content)
    return result

def get_playlists(token):
    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    result = json.loads(result.content)
    return result['items']

def get_playlist_items(token, id):
    url = f"https://api.spotify.com/v1/playlists/{id}/tracks"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    result = json.loads(result.content)
    return result['items']

token = get_token()
playlists = get_playlists(token)

################################################################
playlist_name = input('Enter playlist name: ')
for playlist in playlists:
    if playlist['name'] == playlist_name:
        id = playlist['id']
        break
playlist_items = get_playlist_items(token, id)

file_name = input('Enter file name: ')
f = open(f"{file_name}.txt", "w")
for item in playlist_items:
    if item['track']['name'] != "":
        f.write(f"{item['track']['name']}\n")

f.close()

