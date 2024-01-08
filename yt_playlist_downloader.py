from pytube import Playlist
import os

url = input("Enter playlist url: ")
playlist = Playlist(url)
print(playlist.title)
print("Total Videos in playlist: ", len(playlist.video_urls))

folder_name = input("Enter folder name: ")

for i, video in enumerate(playlist.videos):
	print(f"Downloading video {i}: {video.title}...")
	out_path = video.streams.filter(only_audio=True).first().download(output_path=f"./{folder_name}")
	new_name = os.path.splitext(out_path)
	os.rename(out_path, f"{new_name[0]}.mp3")
	print("Downloaded")
