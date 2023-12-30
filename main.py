from googleapiclient.discovery import build
from pprintpp import pprint as pp
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

youtube = build('youtube', 'v3', developerKey=google_api_key)

f = open('telugu_songs.txt')
w = open('telugu_songs_youtube.txt', 'w')
while True:
    song_name = f.readline()
    if not song_name:
        break
    song_name += ' lyrical telugu song'
    request = youtube.search().list(
        part='snippet',
        q=song_name,
        maxResults=1,
    )

    response = request.execute()

    video_url = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId']
    video_title = response['items'][0]['snippet']['title']
    w.write(video_title + ": " + video_url + '\n')

# pp(response)
# video_url = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId']
# video_title = response['items'][0]['snippet']['title']
# pp(video_title + ": " + video_url)