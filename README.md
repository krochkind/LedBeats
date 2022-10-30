# Changing LED lights to Music with a RaspberryPi
For the holidys, I wanted to decorate my house with LED lights that change color to music.  Rather than purchase something pre-built, I decided to take the long (and more fun) way of building my own.  I used a RaspberryPi because it is portable and draws very little power and some LED lights that I got off Amazon.  I used this to flash Orange lights to scary music for Halloween and Red/Green lights on my Christmas tree to holiday music.
<br /><br />
The way this works, is you upload your MP3s to a designated directory on the RaspberryPi.  The program then analyzes each audio file to create a beatmap of every time it detects a beat.  You select a pattern of colors you want the LED lights to flash in.  The program then connects to your LED strip and plays each MP3 (external speaker required), changing the color of the LED strip each time a new beat is detected.
<br /><br />

## Hardware Requirements

* RaspberyPi with Bluetooth and Python (I used a RaspberryPi 4)
* LED strip with Bluetooth connectivity (I used [this one](https://amzn.to/3WfXyqx))
* External speaker to play music<br />
<br />

## Installation Instructions
### Python Libraries
* pip install bleak
* pip install bledom
* pip install python-vlc
* pip install webcolors
* pip install librosa
<br />
Note: I ran into an issue of being unable to install the librosa library because of a failed dependency on numba.  After installing numba via Conda, I was able to install librosa:
<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;https://github.com/jjhelmus/berryconda<br /> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;chmod +x Berryconda3-2.0.0-Linux-armv6l.sh <br /> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;./Berryconda3-2.0.0-Linux-armv6l.sh<br /> 
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;conda install numba<br /> 
<br /> 

Run *find_device.py* to get the MAC Address and Name of the BlueTooth devices that your RaspberryPi can connect to.  My LED strip looked like this:<br />
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;XX:XX:XX:XX:XX:XX: ELK-BLEDOM   
### config.ini settings
Update the *[BluetoothConnections]* section with your LED strip's information<br />
Choose a folder for your MP3s <br />
Choose a color theme.  Color themes are defined in *themes.py*.  Feel free to make your own<br />
<br />
## Running the application
Upload MP3s to the folder that you designated in *config.ini*<br />
Connect your RaspberryPi to your external speaker<br />
Run *LED-Beats.py* and enjoy!
