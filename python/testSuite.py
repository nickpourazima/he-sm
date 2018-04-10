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
# from multiprocessing import Process
from threading import Thread
# import os.path
# from tkinter import filedialog,messagebox
# import platform
# import sys


#TO-DO Tomorrow
# finish building audio, music, and dynamic tests
# interface to FSR SW
# integrate intermediary gui page


#SERIAL VARS
TAP_SERIAL_PORT = '/dev/tty.usbmodem1421'
TAP_BAUD = 9600
TIMEOUT = 0.25

HAPTIC_SERIAL_PORT = '/dev/tty.usbserial-A907CAHB'
HAPTIC_BAUD = 115200

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
closeFile = False
fileNumber = 0

PACKET_LENGTH = 8

audioFile =[
    '/Users/nickpourazima/GitHub/he-sm/click_44.1_16bit_20sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/click_44.1_16bit_20sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/click_44.1_16bit_20sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/click_44.1_16bit_20sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/beep-11.wav'
]
userName = ""
instructions = "You will first do this and then this. Then there will be a break where you put this on so you can do that. Got it?"
LARGE_FONT= ("Verdana", 12)

#open serial
if(os.path.exists(HAPTIC_SERIAL_PORT)):
    hapticSerial = serial.Serial(HAPTIC_SERIAL_PORT, HAPTIC_BAUD)
if(os.path.exists(TAP_SERIAL_PORT)):
    tapSerial = serial.Serial(TAP_SERIAL_PORT,TAP_BAUD,timeout=TIMEOUT)
else:
    print ("No serial connected...")


class mainGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, InstructionPage, TestPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Please enter your name:", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        self.name = tk.Entry(self) # add the text entry box for the value
        self.name.pack(padx=5)
        self.myController = controller
        button = tk.Button(self, text="Instructions",
                            command = self.advance)
        button.pack()

    def advance(self):
        print("Working so far")
        self.name.focus_set()
        self.name.selection_range(0, tk.END)
        global userName
        userName = (self.name.get())
        self.myController.show_frame(InstructionPage)

class InstructionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text=instructions, font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        self.myController = controller
        button1 =   tk.Button(self, text="Accept",
                            command=self.advance)
        button1.pack()
        button2 =   tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()

    def advance(self):
        global startFlag 
        startFlag = True
        self.myController.show_frame(TestPage)

class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Setup output file", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        # self.flash()
        button1 = tk.Button(self,text="Okay",command=self.quit)
        button1.pack()

    def flash(self):
        bg = self.label.cget("background")
        fg = self.label.cget("foreground")
        self.label.configure(background=fg, foreground=bg)
        self.after(500, self.flash)

        # os.system("python2.7 python/captureGui.py")

def steady_haptic(mode,tempo,timer):
    playBeep()
    # time.sleep(5)
    hapticSerial.write((mode + CRLF).encode())
    hapticSerial.write((tempo + CRLF).encode())
    start = time.time()
    while True:
        reading = hapticSerial.readline().decode('utf-8')
        print(reading)
        end = time.time()
        elapsed = end - start
        hapticSerial.flush()
        print(elapsed)
        if(end-start >= timer):
            hapticSerial.write((OFF+CRLF).encode())
            global closeFile 
            closeFile = True
            break
    print(closeFile)
    playBeep()

def playback(audio_file):
    playBeep()
    # mixer.pre_init(44100, -16, 2, 2048)
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.set_volume(0.3)
    mixer.music.play()
    mixer.music.fadeout(20500)
    while mixer.music.get_busy():
        pass
    playBeep()

def playBeep():
    print ("Prepare for next test in 3 seconds")
    mixer.pre_init(44100, -16, 2, 2048)
    mixer.init()
    mixer.music.load(audioFile[4])
    mixer.music.set_volume(0.1)
    mixer.music.play()
    mixer.music.fadeout(3000)
    while mixer.music.get_busy():
        pass
    print ("Starting...")

def interpret_output_discrete(r):

    # Interpret the raw (binary) output that we got from Arduino.

    #Packet
    #|---------+---+---------+----------+-------------+---|
    #| Byte    | 1 | 2,3     | 4,5      | 6,7         | 8 |
    #| Content | B | [onset] | [offset] | [max force] | E |
    #|---------+---+---------+----------+-------------+---|
    
    #Where [t] = N for oNset, F for oFfset
    #and [time] is the timestamp (in msec)


    # Here we interpret the packet that we received from Arduino.
    # Note that the first element of the packet (B in our case) has been omitted here.
    tap_onset  = ord(r[0])+256*ord(r[1])
    tap_offset = ord(r[2])+256*ord(r[3])
    maxforce   = ord(r[4])+256*ord(r[5])
    
    # Make a formatted output
    output = "%i %i %i"%(tap_onset,tap_offset,maxforce)
    print (output)

    return output

def getTap():
    global closeFile
    global fileNumber
    filename = (userName+' '+str(fileNumber)+' '+time.asctime()) # get the filename we are supposed to output to
    dumpfile = open(filename,'w')
    output_header = "onset offset maxforce"
    dumpfile.write(output_header+"\n")
    while True:
        # Ok, let's read one byte
        r = tapSerial.read(1)
        # print(r)
        if bytes.decode(r)=="B": # This could be the beginning of a packet from arduino
            avail=0 # how many bytes are available
            while avail<PACKET_LENGTH-1: # read to fill up the packet
                avail=tapSerial.inWaiting()

            # all right, now we can read
            r = tapSerial.read(PACKET_LENGTH-1) # read the whole packet straight away
            s = str(r,'latin-1')
            # print(s)
            # Now continue to work with this
            if len(s)==(PACKET_LENGTH-1) and s[-1]=="E": # if we have the correct ending also
                output = interpret_output_discrete(s)
                dumpfile.write(output+"\n")
                dumpfile.flush()
        if closeFile:
            closeFile = False
            fileNumber+=1
            break


hapticTestCases = {
    'H1a1': (DISCRETE,BPM1,15),
    'H1a2': (DISCRETE,BPM2,15),
    'H1a3': (DISCRETE,BPM3,15),
    'H1a4': (DISCRETE,BPM4,15),
    'H1b1': (CONTINOUS,BPM1,15),
    'H1b2': (CONTINOUS,BPM2,15),
    'H1b3': (CONTINOUS,BPM3,15),
    'H1b4': (CONTINOUS,BPM4,15)
}
audioTestCases = {
    'A1a1': (audioFile[0]),
    'A1a2': (audioFile[1]),
    'A1a3': (audioFile[2]),
    'A1a4': (audioFile[3]),
    'A1b1': (audioFile[0]),
    'A1b2': (audioFile[1]),
    'A1b3': (audioFile[2]),
    'A1b4': (audioFile[3])
}

def main():
    #practice mode

    #run through test cases (randomly)

    hapticKeys = list(hapticTestCases.keys())
    shuffle(hapticKeys)
    print (hapticKeys)

    for key in hapticKeys:
        t1 = Thread(target = steady_haptic, args = hapticTestCases.get(key))
        t2 = Thread(target= getTap)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    audioKeys = list(audioTestCases.keys())
    shuffle(audioKeys)
    print (audioKeys)

    for key in audioKeys:
        t1 = Thread(target = playback, args = audioTestCases.get(key))
        t2 = Thread(target= getTap)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    print("FIN")
    #blank window or brief reset before next test

    #upon finishing, close serial

    #summary && output file presented

if __name__ == "__main__":
    app = mainGUI()
    app.title("Audible & Haptic Test Suite (Author: Nick Pourazima - CMU 18')")
    app.mainloop()
    if(startFlag):
        main()
    else:
        "Main was not run, please debug"
    
