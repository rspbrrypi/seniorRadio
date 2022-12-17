# seniorRadio
Project to make an accessible device for internet radio

<img src="https://i.imgur.com/R6uO1aB.jpg" width="200px" >>

The Senior Radio project is an accessible designed internet radio device with both hardware and software components. It is intended to be used for users familiar with controlling a pocket radio where dials controls volume and the selected radio station. The project is made with a user-centered design, focused on a user who want a similar size and controls as a standard handheld radio.

It was built to satisfy the needs of allowing impaired individuals be able to listen to the thousands of different internet streaming content that is usually only normally available through an internet browser. Many people do not have the ability to use such a device easily, so this design aims to make a familiar interface for a modern technology.

The python program is meant to be self-documenting. It reads IO and calls VLC as an audio player to play whatever is selected. It reads and writes to a local json file to store the state of the radio and reads an online json file to load into the list of radio station URLs.

Instructions for setting up the Rpi into headless mode, loading the software, and creating the physical IO is online at <b>https://www.instructables.com/id/Senior-Radio-Raspberry-Pi</b>

Inspired by these other awesome creations:

https://opensource.com/article/19/11/pyradio

https://projects-raspberry.com/fireside-internet-radio-player-for-elderly-users-built-with-raspberry-pi

Newly added 17-12-2022  
I left out the LED. Instead I used that pin (17) for a shutdown button on my Raspberry Pi to completely turn of the radio and the Pi.
Also I added a LCD Screen so you can see which station you're listening to. I used a 16x02 LCD screen with I2C backpack. 
This video explains very simple how to connect it: https://youtu.be/DHbLBTRpTWM
Finally I added another file: stationNames.json. This list contains exactly the same radiostations as InternetStations.json only with a prettier output for the LCD. 
Each station can contain a max of 16 chars or it won't fit the screen. So if you change the InternetStations.json you must also change stationNames.json in the same order.
I mainly used Dutch streams, most of them I found here: https://hendrikjansen.nl/henk/streaming.html  
