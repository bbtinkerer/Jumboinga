# Jumboinga - The jumping boinging game.
# Copyright (c) 2018 bbtinkerer
#
# Simple roulette/wheel type game with a spring doort stop. Uses the 
# Adafruit Circuit Playground Express (CPX) with a piezoelectric sensor 
# and a spring door stop. User pulls back on the door stop spring  and 
# lets go (or knocks the game board really hard) to start the cursor
# moving around the NeoPixel ring of the CPX. Distance travelled by the
# cursor determined by how strong the spring vibrates.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import audioio
import analogio
import board
import neopixel
import time
import digitalio

# default values are arbitrary
# you should calibrate to your setup
# The values indicate at what strength
# to trigger on.
VIBRATION_READ_TIME_SHORT_THRESHOLD = 2800
VIBRATION_READ_TIME_MEDIUM_THRESHOLD = 4500
VIBRATION_READ_TIME_LONG_THRESHOLD = 6000

# I found these times work good for me
# The values are how long to read the sensor
# after triggering.
VIBRATION_READ_TIME_SHORT = 0.5
VIBRATION_READ_TIME_MEDIUM = 1.0
VIBRATION_READ_TIME_LONG = 1.5

# Amount to increase the read time of the piezo
# if the sensor goes above the threshold.
VIBRATION_READ_TIME_INCREMENT = 0.1
VIBRATION_READ_TIME_THRESHOLD = 800

# Number of Win spaces when the game starts.
START_WIN_COUNT = 6

# Number of Win spaces left to consider
# winning the game.
MIN_WIN_COUNT = 2

# Speed of cursor around the neopixel circle.
MAX_SPEED = 0.01
MIN_SPEED = 1.00

# Amount of times to flash the NeoPixel between rounds.
ROUND_ANIMATION_FLASH_COUNT = 5

# Amount of time to alternate between colors
ROUND_ANIMATION_FLASH_DELAY = 0.25

# How fast the cursor ticks between colors
# when stationary.
CURSOR_TICK_SPEED = 0.5

# How much seconds before applying deceleration factor on the cursor
CURSOR_DECELERATE_TIME = 0.5

# Factor to decelerate the cursor
CURSOR_DECELERATE_FACTOR = 1.5

# Sounds to play. These sounds were downloaded from freesound.org
# See README.md for sound file information.
LOSE_ROUND_SOUND_FILE = "362204__taranp__horn-fail-wahwah-3.wav"
START_ROUND_SOUND_FILE = "234565__foolboymedia__announcement-begin.wav"
WIN_GAME_SOUND_FILE = "110317__timbre__remix-of-62176-fanfare-before-after.wav"
WIN_ROUND_SOUND_FILE = "320883__rhodesmas__action-03.wav"

# Some colors to choose from.
RED = (0x10, 0, 0) 
YELLOW = (0x10, 0x10, 0)
GREEN = (0, 0x10, 0)
AQUA = (0, 0x10, 0x10)
BLUE = (0, 0, 0x10)
PURPLE = (0x10, 0, 0x10)
BLACK = (0, 0, 0)

# Setup of the cursor and space colors.
winColor = GREEN
loseColor = RED
cursorColor = PURPLE
cursorWin = YELLOW

# Initalization of variables and stuff from here on out, 
# you don't really need to adjust these

# Setup to read the piezo from A3.
piezoInput = analogio.AnalogIn(board.A3)

# Initial setup the neopixels.
pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=.2)
pixels.fill(BLACK)
pixels.show()

# Holds the game state
gameState = "ReadInput"

# Holds how strong the vibrations are
vibrationStrength = 0

# Speed at which the cursor moves around the NeoPixel ring.
currentSpeed = MAX_SPEED

# Number of neopixels in the ring.
pixelsLength = len(pixels)

# Store the time, used to compare time so we don't
# use time.sleep() to delay in the animations
previousPixelElapsedTime = time.monotonic()
previousRuntime = previousPixelElapsedTime
pixelElapsedTime = 0

# Stores which spaces are win/lose spaces, True are win spaces.
gameWheel = [False] * pixelsLength

# Hold the current count of wins spaces left.
winCount = START_WIN_COUNT

# Use to hold extra vibration reading time after the initial
# spring boinginging
vibrationReadTime = 0

# Hold the location of the cursor.
currentIndex = pixelsLength-1

# Sets the colors on the NeoPixel ring. StartIndex is what neopixel
# is the first win space. Length is the amount of neopixels. WinCount
# is the number of spaces to mark as win spaces clockwise starting
# with startIndex.
def setLinearGameWheel(startIndex, length, winCount):
    loseCount = length - winCount
    while winCount:
        gameWheel[startIndex] = True
        # subtracting so that the direction goes clockwise
        startIndex -= 1
        if startIndex < 0:
            startIndex = length - 1
        winCount -= 1
    while loseCount:
        gameWheel[startIndex] = False
        startIndex -= 1
        if startIndex < 0:
            startIndex = length - 1
        loseCount -= 1

# Moves the cursor around the NeoPixel ring if enough
# time has passed.
def tickWheel():
    global currentIndex
    global pixelElapsedTime
    global previousPixelElapsedTime
    now = time.monotonic()
    pixelElapsedTime = now - previousPixelElapsedTime
    if pixelElapsedTime > currentSpeed:
        pixels[currentIndex] = winColor if gameWheel[currentIndex] else loseColor
        currentIndex -= 1
        if currentIndex < 0:
            currentIndex = pixelsLength - 1
        pixels[currentIndex] = cursorWin if gameWheel[currentIndex] else cursorColor
        pixels.show()
        previousPixelElapsedTime = now

# Flashes the cursor in place if enough time has passed.
def tickCursor():
    global pixelElapsedTime
    global previousPixelElapsedTime
    now = time.monotonic()
    pixelElapsedTime = now - previousPixelElapsedTime
    if pixelElapsedTime > CURSOR_TICK_SPEED:
        pixels[currentIndex] = winColor if pixels[currentIndex] == cursorWin else cursorWin
        pixels.show()
        previousPixelElapsedTime = now

# Flashes the NeoPixel ring alternating colors between first and second and plays
# the sound file.
def roundAnimation(first, second, soundfile):
    # Required for CircuitPlayground Express
    speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
    speaker_enable.switch_to_output(value=True)
    data = open(soundfile, "rb")
    wav = audioio.WaveFile(data)
    a = audioio.AudioOut(board.A0)
    a.play(wav)
    
    for i in range(ROUND_ANIMATION_FLASH_COUNT):
        for j in range(pixelsLength):
            pixels[j] = first
        pixels.show()
        time.sleep(ROUND_ANIMATION_FLASH_DELAY)
        for k in range(pixelsLength):
            pixels[k] = second
        pixels.show()
        time.sleep(ROUND_ANIMATION_FLASH_DELAY)
    while a.playing:
        pass
    # release the resources so they can be used else where
    a.deinit()
    speaker_enable.switch_to_output(value=False)
    speaker_enable.deinit() 

# Calls roundAnimation() with the colors considered a win.
def winRoundAnimation():
    roundAnimation(cursorWin, winColor, WIN_ROUND_SOUND_FILE)

# Calls roundAnimation() with the colors considered a lost.
def loseRoundAnimation():
    roundAnimation(cursorColor, loseColor, LOSE_ROUND_SOUND_FILE)

# Lightup the NeoPixel ring.
def showWheel():
    for i in range(pixelsLength):
        pixels[i] = winColor if gameWheel[i] else loseColor
    pixels.show()

# Just play the sound file.
def playSound(soundfile):
    # Required for CircuitPlayground Express
    speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
    speaker_enable.switch_to_output(value=True)
    data = open(soundfile, "rb")
    wav = audioio.WaveFile(data)
    a = audioio.AudioOut(board.A0)
    a.play(wav)
    while a.playing:
        pass
    a.deinit()
    speaker_enable.switch_to_output(value=False)
    speaker_enable.deinit()
    # need to sleep because reading from A3 will have a high value right after deinit
    time.sleep(0.5) 

# initialize the game starting colors, 9 is the neopixel to the right of the USB
setLinearGameWheel(9, pixelsLength, winCount)
showWheel()

# The game loop.
while True:
    if gameState == "ReadInput":
        # waiting state for user to boing the spring
        playSound(START_ROUND_SOUND_FILE)
        
        # need to reset since this is start of a round
        vibrationStrength = 0
        
        # loop till there is a strong enough vibration that signals the
        # user boing'd the spring, or knocked the game hard enough
        while vibrationStrength < VIBRATION_READ_TIME_SHORT_THRESHOLD:
            vibrationStrength = piezoInput.value
            tickCursor()
            
        # depending on how strong the vibration was, setting the amount
        # of time to keep reading vibrations, stronger the vibration,
        # the longer we read the sensor
        if vibrationStrength < VIBRATION_READ_TIME_MEDIUM_THRESHOLD:
            vibrationReadTime = VIBRATION_READ_TIME_SHORT
            vibrationReadTime = VIBRATION_READ_TIME_SHORT
        elif vibrationStrength < VIBRATION_READ_TIME_LONG_THRESHOLD:
            vibrationReadTime = VIBRATION_READ_TIME_MEDIUM
        else:
            vibrationReadTime = VIBRATION_READ_TIME_LONG
        
        # set the state to WheelSpin where we let the cursor spin
        # for a while and read the sensor
        gameState = "WheelSpin"
        
        # get the time so we know how long we have been reading the
        # sensor in the WheelSpin state.
        startTime = time.monotonic()
        
    elif gameState == "WheelSpin":
        # state that letting the cursor go round and round while 
        # reading the sensor to add more time going round and round
        now = time.monotonic()
        elapsedTime = now - startTime
        if elapsedTime < vibrationReadTime:
            vibrationStrength = piezoInput.value
            # adding a bit more time reading if the vibrations are strong enough
            if vibrationStrength > VIBRATION_READ_TIME_THRESHOLD:
                vibrationReadTime += VIBRATION_READ_TIME_INCREMENT
            tickWheel()
        else:
            # time for reading the sensor ended so need to go to the WindDown state
            gameState = "WindDown"
            
            # need to reset this so that we know how long has elapsed
            previousRuntime = now
            
    elif gameState == "WindDown":
        # state where the cursor slows down going around the NeoPixel ring
        now = time.monotonic()
        runElapsedTime = now - previousRuntime
        
        # time before decelerating the speed of the cursor
        if runElapsedTime > CURSOR_DECELERATE_TIME:
            previousRuntime = now
            
            # how much to decelerate the cursor
            currentSpeed *= CURSOR_DECELERATE_FACTOR
            
            # check that the cursor is to slow to move on
            if currentSpeed > MIN_SPEED: 
 
                # check if a win
                if gameWheel[currentIndex]:
                    # do the win stuff
                    winRoundAnimation()
                    # decrease the amount of win spaces on the ring
                    winCount -= 1
                else:
                    # loser
                    loseRoundAnimation()
                    # start over with the starting amount of win spaces
                    winCount = START_WIN_COUNT
                
                # check to see if the user got down the minimum win spaces
                # and play the Winning game sound
                if winCount == MIN_WIN_COUNT:
                    playSound(WIN_GAME_SOUND_FILE)
                    winCount = START_WIN_COUNT
                    
                # reset the ring accordingly to how much win spaces as deteremined
                # earlier by the win/lose round or win game
                currentSpeed = MAX_SPEED
                setLinearGameWheel(currentIndex, pixelsLength, winCount)
                showWheel()
                
                # go back to reading the sensor
                gameState = "ReadInput"
        else:
            tickWheel()
    