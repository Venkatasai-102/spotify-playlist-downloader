from pytube import YouTube
import os

urls = []
num_videos = int(input("Enter number of videos you want to download: "))

for i in range(num_videos):
	url = input("Enter url: ")
	urls.append(url)

is_folder = input("Do you want to save in a folder? (y/n)")

folder_name = ""

if is_folder == "y":
	folder_name = input("Enter folder name: ")

for url in urls:
	video = YouTube(url)
	print(f"Downloading {video.title}...")
	out_path = ""
	if is_folder == "n":
		out_path = video.streams.filter(only_audio=True).first().download()
	else:
		out_path = video.streams.filter(only_audio=True).first().download(output_path=f"./{folder_name}")
	new_name = os.path.splitext(out_path)
	os.rename(out_path, f"{new_name[0]}.mp3")
	print("Downloaded")
