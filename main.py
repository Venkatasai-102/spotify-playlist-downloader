from googleapiclient.discovery import build
from pprintpp import pprint as pp
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv('GOOGLE_API_KEY')

youtube = build('youtube', 'v3', developerKey=google_api_key)


request = youtube.search().list(
    part='snippet',
    q='Attention song',
    maxResults=1,
)

response = request.execute()

# pp(response)
video_url = 'https://www.youtube.com/watch?v=' + response['items'][0]['id']['videoId']
video_title = response['items'][0]['snippet']['title']
pp(video_title + ": " + video_url)