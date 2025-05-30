#
# Brandon Stevens
# 01/03/2020
# Main program for seniorRadio project. Reads IO and plays internet radio streams using VLC
#
# changes by Tmra 9-dec-2022
# left out the Led, added a shutdown button instead and 
# also added LCD 16x02 for text output

from gpiozero import LED, Button  # for rpi IO
import json
import urllib.request  # grabbing github json page
import time  # for delays
import subprocess  # for calling bash commands
import sys

# adjust to your python version and user
sys.path.append("/home/radiohead/.local/lib/python3.9/site-packages/")  # PYTHONPATH fix to make sure it sees VLC package

import vlc  # python-vlc package, and VLC need to be installed

#extra shutdown button & LCD 16x2 
from signal import signal, SIGTERM, SIGHUP, pause
from  rpi_lcd import LCD

lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

# list with radiostreams 
url = "https://raw.githubusercontent.com/rspbrrypi/seniorRadio/master/internetStations.json"

# list with stationNames
url2 = "https://raw.githubusercontent.com/rspbrrypi/seniorRadio/master/stationNames.json"

def buttonPress():
    player.pause()  # stops stream, resumes the stream on another press

def shutdown():
    lcd.text("Power off", 1)
    player.stop()
    lcd.clear()
    subprocess.check_call(['sudo','poweroff']) # shutdown the pi

def show_text(): 
    current = radioState.get('stationSelected')
    radiostation = str(stationNames[current])
    lcd.text("Je luistert naar", 1) # change this as you like, it's the first line of your LCD screen
    lcd.text(radiostation, 2) 

def changeStation():
    player.stop()
    lcd.clear()
    player.set_media(mediaList[stationSelected])
    saveState()
    player.play() 
    show_text()

def incrementStation(currentStation):
    if currentStation == (len(streamURLs) - 1):  # if last entry
        newStation = 0
    else:
        newStation = currentStation + 1  # increment
    return newStation


def decrementStation(currentStation):
    if currentStation == 0:  # if first entry
        newStation = (len(streamURLs) - 1)
    else:
        newStation = currentStation - 1  # decrement
    return newStation


def increaseAudio(audioLevel):
    if audioLevel == 100:  # if max
        newAudio = 100
    else:
        newAudio = audioLevel + 10  # increase
    return newAudio


def decreaseAudio(audioLevel):
    if audioLevel == 0:  # if min
        newAudio = 0
    else:
        newAudio = audioLevel - 10  # decrease
    return newAudio


def pinARising():  # Pin A station event handler
    if pinB.is_pressed:  # pin A rising while A is active is a clockwise turn
        global stationDialCountCW, stationDialCountCCW
        if stationDialCountCCW > 0:  # reset, debouncer
            stationDialCountCW = 0
            stationDialCountCCW = 0
        else:
            stationDialCountCW = stationDialCountCW + 1


def pinBRising():  # Pin B station event handler
    if pinA.is_pressed:  # pin B rising while A is active is a counter-clockwise turn
        global stationDialCountCW, stationDialCountCCW
        if stationDialCountCW > 0:  # reset, debouncer
            stationDialCountCW = 0
            stationDialCountCCW = 0
        else:
            stationDialCountCCW = stationDialCountCCW + 1


def pinCRising():  # Pin C audio level event handler
    if pinD.is_pressed:  # pin C rising while C is active is a clockwise turn
        global audioDialCountCW, audioDialCountCCW
        if audioDialCountCCW > 0:  # reset, debouncer
            audioDialCountCW = 0
            audioDialCountCCW = 0
        else:
            audioDialCountCW = audioDialCountCW + 1


def pinDRising():  # Pin D audio level event handler
    if pinC.is_pressed:  # pin D rising while C is active is a counter-clockwise turn
        global audioDialCountCW, audioDialCountCCW
        if audioDialCountCW > 0:  # reset, debouncer
            audioDialCountCW = 0
            audioDialCountCCW = 0
        else:
            audioDialCountCCW = audioDialCountCCW + 1


def saveState():
    radioState["stationSelected"] = stationSelected
    radioState["audioLevel"] = audioLevel
    with open("radioState.json", "w") as f:
        json.dump(radioState, f, indent=4)


# SETUP

# quick fix to give time for connection with bluetooth speaker on startup
# may not need depending on how you are booting it up
# time.sleep(30)

# first, restart pulseaudio. Need to do this on almost every boot on my and many machines so just do it every time
# subprocess.call(["pulseaudio", "--kill"])
# time.sleep(0.5)
# subprocess.call(["pulseaudio", "--start"])
time.sleep(0.5)


# setup pins (https://pinout.xyz/ for reference)
# Pause button
button = Button(pin=17, bounce_time=0.04, hold_time=0.2)  # BCM pin 17, push button
button.when_pressed = buttonPress  # calls buttonPress function

# Shutdown button 
shutdownbutton = Button(pin=27, bounce_time=0.04, hold_time=0.2)
shutdownbutton.when_held = shutdown # calls shutdown function

pinA = Button(21, pull_up=True)  # Station rotary encoder dt pin connected to BCM pin 21
pinB = Button(20, pull_up=True)  # Station rotary encoder clk pin connected to BCM pin 20
pinC = Button(19, pull_up=True)  # Audio level rotary encoder dt pin connected to BCM pin 19
pinD = Button(16, pull_up=True)  # Audio level rotary encoder clk pin connected to BCM pin 16

#  global variables, track dial movement
stationDialCountCW = 0
stationDialCountCCW = 0
audioDialCountCW = 0
audioDialCountCCW = 0

# read json file and load data
with open("/home/radiohead/seniorRadio/radioState.json", "r") as f:
    radioState = json.load(f)
with urllib.request.urlopen(url) as f:  # change your url for json file at top of this file
    internetStations = json.loads(f.read().decode())
stationSelected = radioState["stationSelected"]
audioLevel = radioState["audioLevel"]
streamURLs = internetStations["stationLinks"]
if stationSelected > len(streamURLs):  # not valid station anymore, outside range
    stationSelected = 0

# List with radiostations voor LCD output
with urllib.request.urlopen(url2) as g: 
    stationNames = json.loads(g.read())

# setup VLC
instance = vlc.Instance('--input-repeat=-1', '--fullscreen')
player = instance.media_player_new()
mediaList = []  # list for each stream
for i in range(len(streamURLs)):
    mediaList.append(instance.media_new(streamURLs[i]))

# begin playing
player.audio_set_volume(audioLevel)
player.set_media(mediaList[stationSelected])
player.play()
show_text()

# rotary encoder handlers
pinA.when_pressed = pinARising  # Register the station event handler for pin A
pinB.when_pressed = pinBRising  # Register the station event handler for pin B
pinC.when_pressed = pinCRising  # Register the audio level event handler for pin C
pinD.when_pressed = pinDRising  # Register the audio level event handler for pin D

while True:
    # main loop, poll to see dials change with debouncing
    if stationDialCountCW >= 5:  # valid turn
        stationSelected = incrementStation(stationSelected)
        changeStation()
        stationDialCountCW = 0
    elif stationDialCountCCW >= 5:  # valid turn
        stationSelected = decrementStation(stationSelected)
        changeStation()
        stationDialCountCCW = 0
    if audioDialCountCW >= 2:  # likely valid turn, okay if false positive rarely
        audioLevel = increaseAudio(audioLevel)
        player.audio_set_volume(audioLevel)
        saveState()
        audioDialCountCW = 0
    elif audioDialCountCCW >= 2:  # likely valid turn, okay if false positive rarely
        audioLevel = decreaseAudio(audioLevel)
        player.audio_set_volume(audioLevel)
        saveState()
        audioDialCountCCW = 0
