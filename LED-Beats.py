import asyncio
import configparser
import os
from random import randint
import time
import webcolors

# bleak imports
from bleak import BleakScanner, BleakClient

# project imports
from device import BleLedDevice
import music_helper as audio
from themes import themes

if os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    try:
        MP3_LOCATION = config['Directories']['mp3Location']
        BLUETOOTH_CONNECTION_MAC = config['BluetoothConnections']['bluetoothConnectionMac']
        BLUETOOTH_CONNECTION_NAME = config['BluetoothConnections']['bluetoothConnectionName']
        THEME = config['Themes']['theme']
    except:
        print("Invalid config.ini file")         
        os.sys.exit()

async def timer(file_name: str, stop_at: float, beatmap: list, device: BleLedDevice):
    start_time = time.time()
    beat_num = 0
    while True:
        time_elapsed = time.time() - start_time
        await asyncio.sleep(.01)
        if round(time_elapsed, 2) in beatmap:
            beat_num += 1
            await beatfound(time_elapsed, beat_num, len(beatmap), device)
        if time_elapsed > stop_at:
            print(f"{file_name} Beats Finished in {time_elapsed:.3f} seconds")
            break


async def beatfound(beat: float, beat_num: int, total_beats: int, device: BleLedDevice):
    print(f"Beat {beat_num} of {total_beats} - {beat:.2f} seconds : ", end="", flush=True)
    if THEME == 'Random' or THEME not in themes:
        await color_changer('random', device)
        return
    
    num_colors_in_theme = len(themes[THEME])
    if num_colors_in_theme == 1:
        if beat_num % 2 == 1:
            await color_changer(themes[THEME][0], device)
        else:
            await color_changer('off', device)
        return
    # Cycle through array of theme's colors.  -1 because arrays start at 0
    await color_changer(themes[THEME][(beat_num-1) % num_colors_in_theme], device)
    return


def getplaylist():
    return [f for f in os.listdir('./' + MP3_LOCATION) if os.path.isfile(os.path.join('./' + MP3_LOCATION, f))]


async def connect_bt_device(device) -> BleakClient:
    print(f"Connecting to {device.name} ({device.address})...")
    client = BleakClient(device)
    await client.connect()
    return client


async def color_changer(color: str, device: BleLedDevice, output=True):
    if output:
        print(color)
    if color.lower() == 'random':
        await device.set_color(randint(0, 255), randint(0, 255), randint(0, 255))
        return
    if color.lower() == 'off':
        color = 'black'
    rgb = webcolors.html5_parse_legacy_color(color)
    await device.set_color(rgb[0], rgb[1], rgb[2])
    return


async def main():
    if not os.path.exists('config.ini'):
        print("Missing config.ini file")
        os.sys.exit()
    if not os.path.exists(f"./{MP3_LOCATION}"):
        os.makedirs(f"./{MP3_LOCATION}")
        os.makedirs(f"./{MP3_LOCATION}/beatmaps")
    if not os.path.exists(f"./{MP3_LOCATION}/beatmaps"):
        os.makedirs(f"./{MP3_LOCATION}/beatmaps")
    if not getplaylist():
        print("Please add some MP3 files to your mp3Location directory (specified in config.ini)")
        os.sys.exit()
    await connect_to_bluetooth_device()

   
async def connect_to_bluetooth_device():
    if len(BLUETOOTH_CONNECTION_MAC) > 0:
        bt_device = [device for device in await BleakScanner.discover() if device.name is not None and device.address == BLUETOOTH_CONNECTION_MAC][0]
    elif len(BLUETOOTH_CONNECTION_NAME) > 0:
        bt_device = [device for device in await BleakScanner.discover() if device.name is not None and device.name.strip() == BLUETOOTH_CONNECTION_NAME][0]
    
    try:
        bt_client = await connect_bt_device(bt_device)
        device = await BleLedDevice.new(bt_client)
        await device.set_color(0, 0, 0)
        await playlist(device)
    except Exception as e:
        print(e)
    finally:
        await bt_client.disconnect()
        print("Disconnected")


async def playlist(device: BleLedDevice):
    for file_name in getplaylist():
        file_name_no_extension, _ = os.path.splitext(file_name)
        beatmap_file = MP3_LOCATION + '/beatmaps/' + file_name_no_extension + '.beatmap.txt'
        if not os.path.exists(beatmap_file):
            beatmap_file = audio.create_beatmap(file_name)
    
    for file_name in getplaylist():
        file_name_no_extension, _ = os.path.splitext(file_name)
        beatmap_file = MP3_LOCATION + '/beatmaps/' + file_name_no_extension + '.beatmap.txt'
        beatmap = []
        with open(beatmap_file) as f:
            beatmap = [round(float(line), 2) for line in f]
        last_beat = beatmap[-1]    
        await color_changer('off', device, False)
        start = time.time()
        asyncio.get_event_loop().create_task(timer(file_name, last_beat, beatmap, device))
        await audio.play_audio(file_name)
        print(f"{file_name} Finished in {time.time()-start:.3f} seconds")
        await color_changer('off', device, False)
        
        time.sleep(4) # Pause between songs
        print()


if __name__ == "__main__":
    asyncio.run(main())
