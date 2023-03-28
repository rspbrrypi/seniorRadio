# seniorRadio
Project to make an simple internet radio for Raspberry Pi; I used a Pi Zero W. Easy to use, and cheap in electrical costs.
<img src="https://github.com/rspbrrypi/seniorRadio/blob/master/Pizero-internetradio.jpg?raw=true" width="200px" >
It has 3 rotating knobs for volume, change channel and brightness for LCD-screen. 
It also has a pause button and a shutdown button to safely turn of the Pi.

This project is mainly based on this seniorRadio Project: https://github.com/Bunborn/seniorRadio
Difference is that I left out the LED. Instead I used that pin (17) for a *shutdown button* on my Raspberry Pi to completely turn of the radio and the Pi.
Also I added a *LCD Screen* so you can see which station you're listening to.

Finally I added another file: stationNames.json. This list contains exactly the same radiostations as InternetStations.json only with a prettier output for the LCD. 
Each station can contain a max of 16 chars or it won't fit the screen. So if you change the InternetStations.json you must also change stationNames.json in the same order.---
I mainly used Dutch streams, most of them I found here: https://hendrikjansen.nl/henk/streaming.html  But you can change them to your own favourite streaming radio channels.
    
## Roughly setup (for details, check the urls): 
1. Install an OS on your Raspberry Pi, connect to internet & setup SSH connection
    You can start off with the instructions for the wiring etc on the original seniorRadio here:  
    https://github.com/Bunborn/seniorRadio 
    Instructions for setting up the Rpi into headless mode etc
    * https://www.instructables.com/id/Senior-Radio-Raspberry-Pi
    * https://opensource.com/article/19/11/pyradio
    * https://projects-raspberry.com/fireside-internet-radio-player-for-elderly-users-built-with-raspberry-pi

2. Install GIT 
    Open a terminal and clone this repo by typing: git clone https://github.com/rspbrrypi/seniorRadio.git

3. Install VLC
   See: https://pimylifeup.com/raspberry-pi-vlc/

4. (optional) Install a SOUNDCARD if you use a Pi Zero (I used a guitar interface adapter)
    Instructions you'll find here: https://circuitdigest.com/microcontroller-projects/how-to-use-usb-audio-device-and-microphone-on-raspberry-pi-zero-w
 
5. LCD
  Connect your LCD-screen.  I used a 16x02 LCD screen with I2C backpack. 
  This video explains very simple how to connect it: https://youtu.be/DHbLBTRpTWM
 
6. Setup to start your radio at boot with CRONTAB
   https://www.cyberciti.biz/faq/linux-execute-cron-job-after-system-reboot/
    Open a terminal and type crontab -e to open up the crontab.
    Add the following line:
     @reboot sleep 180 && python3 /home/radio/seniorRadio/seniorRadio.py
    Save and exit. Reboot your pi. Change the time (180 seconds) to whatever time your OS needs to load before starting the radio.

NB
If you pause the radio, and start playing the radio again, it will take on from the song from where you paused and then stops. 
Just rotate the channel knob forwards and back to the channel you want to listen to.


