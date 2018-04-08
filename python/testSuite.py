#   Author: Nick Pourazima
#   Contact: npourazima@gmail.com
#   Description:
import serial
import time
import os
import tkinter as tk
from functools import partial
from random import shuffle
from pygame import mixer

#SERIAL VARS
SERIAL_PORT = '/dev/tty.usbserial-A907CAHB'
BAUD = 115200

#TEMPO INFO
BPM1 = '45'
BPM2 = '90'
BPM3 = '135'
BPM4 = '180'

#HAPTIC VARS
OFF = '0'
DISCRETE = '1'
CONTINOUS = '2'
CRLF = '\r\n'
startFlag = False
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.userNameEntryLabel = tk.Label(self,text="Username: ")
        self.userNameEntry = tk.Entry(self)
        self.startButton = tk.Button(self, text="Start", command=self.on_button)
        self.userNameEntryLabel.pack(side = "left")
        self.userNameEntry.pack(side = "right")
        self.startButton.pack(side = "bottom")

    def on_button(self):
        userName = (self.userNameEntry.get())
        global startFlag 
        startFlag = True
        self.quit()

def steady_haptic(mode,tempo,timer):
    time.sleep(5)
    ser.write(mode + CRLF)
    ser.write(tempo + CRLF)
    start = time.time()
    while True:
        reading = ser.readline().decode('utf-8')
        print(reading)
        end = time.time()
        elapsed = end - start
        ser.flush()
        print(elapsed)
        if(end-start >= timer):
            ser.write(OFF+CRLF)
            break

def playback():
    mixer.pre_init(44100, -16, 2, 2048)
    mixer.init()
    mixer.music.load('/Users/nickpourazima/GitHub/he-sm/click_16bit_20sec_45bpm.wav')
    mixer.music.play()
    time.sleep(20)
    # mixer.music.fadeout(10)
#open serial
if(os.path.exists(SERIAL_PORT)):
    ser = serial.Serial(SERIAL_PORT, BAUD)
else:
    print ("No serial connected...")
hapticTestCases = {
    'H1a1': partial(steady_haptic,DISCRETE,BPM1,15),
    'H1a2': partial(steady_haptic,DISCRETE,BPM2,15),
    'H1a3': partial(steady_haptic,DISCRETE,BPM3,15),
    'H1a4': partial(steady_haptic,DISCRETE,BPM4,15),
    'H1b1': partial(steady_haptic,CONTINOUS,BPM1,15),
    'H1b2': partial(steady_haptic,CONTINOUS,BPM2,15),
    'H1b3': partial(steady_haptic,CONTINOUS,BPM3,15),
    'H1b4': partial(steady_haptic,CONTINOUS,BPM4,15)
}

def main():
    #open save file

    #build test gui

    #instructions && user inputs ready key

    #practice mode

    #run through test cases (can do random or in order)

    keys = list(hapticTestCases.keys())
    shuffle(keys)
    print (keys)
    playback()
    # for key in keys:
    #     hapticTestCases[key]()

    #blank window or brief reset before next test

    #upon finishing, close serial

    #summary && output file presented

if __name__ == "__main__":
    app = App()
    app.mainloop()
    if(startFlag):
        main()
    else:
        print ("EXECUTION ERROR")