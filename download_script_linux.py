import requests
import os
import subprocess
from subprocess import Popen
import shutil
import time
import download_config

req = requests.Session()

def get_selection():
	print('''
	Select what you want to do \n

	1. Download and convert stream video only.\n
	2. Download and convert stream audio only.\n
	3. Download and convert stream video and audio with separate links.\n
	4. Download and convert stream video and audio with sigle link.\n\n
	''')

	selection = int(input("Enter your selection number(1, 2, 3, 4 only):\n"))

	if not 0 < selection < 5 :
		raise ValueError("Invalid input!!!")
		exit()
	elif selection == 1:
		download_video()
	elif selection == 2:
		download_audio()
	elif selection == 3:
		convert_video_audio()
	else:
		convert_video()


def download_video():
	i = 0
	headers = download_config.headers
	global url_video
	url_video = input('Input Video URL (Replace "{}" with segment number)\n')
	check_video_start = req.get(url_video.format(i), headers=headers, allow_redirects=True)

	if check_video_start.status_code != 200:
		print('Video segments start with 1')
		i = 1
	else:
		print('Video segments start with 0')

	while True:
		url = url_video.format(i)
		filetype = url.split('.')[-1]

		video = req.get(url, headers=headers, allow_redirects=True)
		if video.status_code != 200:
			print('No more video segments to download...')
			break
		else:
			video_f = os.path.dirname('Downloads/Video/')
			temp_dir = os.path.dirname('Downloads/temp/Video/')
			if not os.path.exists(temp_dir):
				os.makedirs(temp_dir)
			elif not os.path.exists(video_f):
				os.makedirs(video_f)

			open(temp_dir + '/' + f'part_{i}.' + filetype, 'wb').write(video.content)
			print(f'Successfully Downloaded part {i}')
			i+=1
	concat_video()
	return url_video


def download_audio():
	i = 0
	headers = download_config.headers
	global url_audio
	url_audio = input('Input Audio URL (Replace "{}" with segment number)\n')
	check_audio_start = req.get(url_audio.format(i), headers=headers, allow_redirects=True)
	if check_audio_start.status_code != 200:
		print('Audio segments start with 1')
		i = 1
	else:
		print('Audio segments start with 0')
	while True:
		url = url_audio.format(i)
		filetype = url.split('.')[-1]

		audio = req.get(url, headers=headers, allow_redirects=True)
		if audio.status_code != 200:
			print('No more audio segments to download...')
			break
		else:
			audio_f = os.path.dirname('Downloads/Audio/')
			temp_dir = os.path.dirname('Downloads/temp/Audio/')
			if not os.path.exists(temp_dir):
				os.makedirs(temp_dir)
			elif not os.path.exists(audio_f):
				os.makedirs(audio_f)

			open(temp_dir + '/' + f'part_{i}.' + filetype, 'wb').write(audio.content)
			print(f'Successfully Downloaded part {i}')
			i+=1
	concat_audio()
	return url_audio


def concat_video():
	temp_dir = os.path.dirname('Downloads/temp/Video/')
	filetype = url_video.split('.')[-1]
	code = f"cat *.{filetype} > ../../Video/merged.{filetype}"

	open(temp_dir + '/concat_video.sh', 'w').write(code)
	print('Concatenating video files...')
	os.chdir(temp_dir)
	open_sh = Popen(['concat_video.sh'])
	open_sh.wait()
	if open_sh.returncode == 0:
		os.chdir('../../../')
		shutil.rmtree('Downloads/temp')	


def concat_audio():
	temp_dir = os.path.dirname('Downloads/temp/Audio/')
	filetype = url_audio.split('.')[-1]
	code = f"cat *.{filetype} > ../../Audio/merged.{filetype}"

	open(temp_dir + '/' + 'concat_audio.sh', 'w').write(code)
	print('Concatenating audio files...')
	os.chdir(temp_dir)
	open_sh = Popen(['concat_audio.sh'])
	open_sh.wait()
	if open_sh.returncode == 0:
		os.chdir('../../../')
		shutil.rmtree('Downloads/temp')


def convert_video_audio():
	url_video = download_video()
	url_audio = download_audio()
	os.chdir('Downloads')
	folder_video = os.path.dirname('Video/')
	folder_audio = os.path.dirname('Audio/')
	filetype_video = url_video.split('.')[-1]
	filetype_audio = url_audio.split('.')[-1]
	code = f"ffmpeg -i {folder_video}/merged.{filetype_video} -i {folder_audio}/merged.{filetype_audio} -c:v copy -c:a copy {folder_video}/final.mp4"
	open('ffmpeg_convert.sh', 'w').write(code)
	print('Starting to convert...')
	subprocess.run('ffmpeg_convert.sh')
	os.remove('ffmpeg_convert.sh')
	os.remove(f'Video/merged.{filetype_video}')
	os.remove(f'Audio/merged.{filetype_audio}')


def convert_video():
	url_video = download_video()
	os.chdir('Downloads')
	folder_video = os.path.dirname('Video/')
	filetype_video = url_video.split('.')[-1]
	print(os.getcwd())
	code = f"ffmpeg -i {folder_video}/merged.{filetype_video} -c:v copy -c:a copy {folder_video}/final.mp4"
	open('ffmpeg_convert.sh', 'w').write(code)
	print(os.getcwd())
	subprocess.run('ffmpeg_convert.sh')
	os.remove('ffmpeg_convert.sh')
	os.remove(f'Video/merged.{filetype_video}')
	cat

get_selection()


