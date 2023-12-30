# imports
from dotenv import load_dotenv
import os
import base64
from requests import get, post
import json
from googleapiclient.discovery import build
from pytube import YouTube

load_dotenv()

################################################################
# ids and keys
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
user_id = os.getenv('SPOTIFY_USER_ID')
google_api_key = os.getenv('GOOGLE_API_KEY')

################################################################
# helper functions
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
# getting the playlist items from spotify
playlist_name = input('Enter playlist name: ')
for playlist in playlists:
    if playlist['name'] == playlist_name:
        id = playlist['id']
        break
playlist_items = get_playlist_items(token, id)

song_names = []

for item in playlist_items:
    if item['track']['name'] != "":
        artists = ""
        for i, artist in enumerate(item['track']['artists']):
            if i == len(item['track']['artists']) - 1:
                artists += artist['name']
            else:
                artists += artist['name'] + ", "
        song_names.append(f"{item['track']['name']} - {artists}")

################################################################
# getting urls from youtube
youtube = build('youtube', 'v3', developerKey=google_api_key)
urls = []
for song_name in song_names:
    if not song_name:
        break
    song_name += ' lyrical song'
    request = youtube.search().list(
        part='snippet',
        q=song_name,
        maxResults=1,
    )

    response = request.execute()

    video_url = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId']
    # video_title = response['items'][0]['snippet']['title']
    urls.append(video_url)

################################################################
# saving as audio file in the given folder
folder_name = input('Enter folder name: ')
for url in urls:
    yt = YouTube(url)
    out_path = yt.streams.filter(only_audio=True).first().download(output_path=f'./{folder_name}')
    new_name = os.path.splitext(out_path)
    os.rename(out_path, f"{new_name[0]}.mp3")