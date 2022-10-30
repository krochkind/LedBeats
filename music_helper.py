import asyncio
import configparser
import os
from os.path import exists
import sys
import time
import vlc
import warnings

if exists('config.ini'):
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    
    try:
        MP3_LOCATION = config['Directories']['mp3Location']
    except:
        pass


def create_beatmap(file_path):
    start_time = time.time()
    if 'librosa' not in sys.modules:
        print("Loading music analysis libraries.  This can take a moment...")
    import librosa
    warnings.filterwarnings('ignore')
    print(f"Start Analyzing Beats: {file_path}")
    file_name_no_extension, _ = os.path.splitext(file_path)
    x, sr = librosa.load(MP3_LOCATION + '/' + file_path)
    onset_frames = librosa.onset.onset_detect(y=x, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
    onset_times = librosa.frames_to_time(onset_frames)
    output_name = file_name_no_extension + '.beatmap.txt'
    with open(MP3_LOCATION + '/beatmaps/' + output_name, 'wt') as f:
        f.write('\n'.join(['%.2f' % onset_time for onset_time in onset_times]))
    print(f"Done Analyzing Beats: {output_name} in {round((time.time() - start_time), 2)} seconds")
    return MP3_LOCATION + '/beatmaps/' + output_name

 
async def play_audio(source):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(MP3_LOCATION + '/' + source)
    player.set_media(media)
    player.play()
    time.sleep(0.1)
    duration = player.get_length()
    print(f"{source} duration: {str(duration/1000)} seconds")
    await asyncio.sleep(duration/1000)


def getplaylist():
    return os.listdir('./' + MP3_LOCATION)
