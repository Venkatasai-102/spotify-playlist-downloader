from pytube import YouTube
import os

url = 'https://www.youtube.com/watch?v=RSYHtpVRSjU'
yt = YouTube(url)

print(yt.title)

# dowloading audio
out_path = yt.streams.filter(only_audio=True).first().download(output_path='./telugu_songs')
new_name = os.path.splitext(out_path)
# save to a folder named 'telgu_songs'
# new_path = os.path.join(os.path.dirname(out_path), 'telgu_songs')
os.rename(out_path, f"{new_name[0]}.mp3")