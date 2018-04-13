#   Author: Nick Pourazima
#   Contact: npourazima@gmail.com
#   Description:
import serial
import time
import os
import tkinter as tk
import sys
import datetime
from functools import partial
from random import shuffle
from pygame import mixer
from threading import Thread
from tabulate import tabulate
#TO-DO Tomorrow
# re-organize output from haptic such that inter onset interval is acquired
# timestamp of tests
# timestamp of tap info

# think about tempo write time vs. time of full interval to complete, 
# can only change at rate equivalent to rate +1 essentially otherwise jumps in value
# finish building dynamic audio tests
# CRUCIAL: 
# time stamp functions save to output 
# also need IOI data from audio somehow -> onset detection https://musicinformationretrieval.com/onset_detection.html
# can pipe terminal to txt as other reference

#LOW PRIORITY
# instruction verbiage
# comments/clean up code
# integrate intermediary gui page, flashing countdown in sync with audio?
# captureGUI to 3.6 pull request --> not a priority
# data output format

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

#GUI VARS
LARGE_FONT= ("Verdana", 12)

#Get Tap / Write File VARS
PACKET_LENGTH = 8
startFlag = False
closeFile = False
startRead = False
t0 = ''
userName = ""
timestamp = datetime.datetime
hapticData = []
tapData = []


instructions = "You will first do this and then this. Then there will be a break where you put this on so you can do that. Got it?"
audioFile =[
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_30sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_30sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_30sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_30sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_32sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_16sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_11sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_8sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_32sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_16sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_11sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_8sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/beep-11.wav'
]


#open serial
if(os.path.exists(HAPTIC_SERIAL_PORT) and os.path.exists(TAP_SERIAL_PORT)):
    hapticSerial = serial.Serial(HAPTIC_SERIAL_PORT, HAPTIC_BAUD)
    tapSerial = serial.Serial(TAP_SERIAL_PORT,TAP_BAUD,timeout=TIMEOUT)
else:
    print ("No serial connected...")
    sys.exit()


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
        self.label = tk.Label(self, text="GET READY", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        # self.flash()
        button1 = tk.Button(self,text="Start",command=self.quit)
        button1.pack()

    def flash(self):
        bg = self.label.cget("background")
        fg = self.label.cget("foreground")
        self.label.configure(background=fg, foreground=bg)
        self.after(500, self.flash)

def steady_haptic(mode,tempo,timer):
    global closeFile, startRead
    readyFlag = False

    # playBeep()
    if startRead:
        hapticSerial.write((mode + CRLF).encode())
        hapticSerial.write((tempo + CRLF).encode())
        hapticSerial.flush()
        readyFlag = True
        start = time.time()
    while readyFlag:
        end = time.time()
        elapsed = end - start
        reading = hapticSerial.readline().decode('utf-8')

        (hapticData.append([timestamp.now(),elapsed,reading,None,None,None,None]))
        if(elapsed >= timer):
            hapticSerial.write((OFF+CRLF).encode())
            closeFile = True
            break
 

    # time.sleep(1)
    # playBeep()

def dynamic_haptic(mode,tempo,timer):
    playBeep()
    hapticSerial.write((mode + CRLF).encode())
    hapticSerial.write((tempo + CRLF).encode())
    newTempo = int(tempo)
    increment = 10
    print(newTempo)
    start = time.time()
    while True:
        time.sleep((60000/newTempo)/1000)
        reading = hapticSerial.readline().decode('utf-8')
        print(reading)
        end = time.time()
        elapsed = end - start
        hapticSerial.flush()
        print(elapsed)
        if(elapsed <= timer/4):
            newTempo = newTempo+increment
            hapticSerial.write((str(newTempo)+ CRLF).encode())
            print('STAGE ONE: ' + str(newTempo))
        elif(elapsed >= timer/4 and elapsed <= timer/2):
            newTempo = newTempo-increment
            hapticSerial.write((str(newTempo)+ CRLF).encode())
            print('STAGE TWO: ' + str(newTempo))
        elif(elapsed >= timer/2 and elapsed <= (timer/2+timer/4)):
            newTempo = newTempo+increment
            hapticSerial.write((str(newTempo)+ CRLF).encode())
            print('STAGE THREE: ' + str(newTempo))
        elif(elapsed >= (timer/2+timer/4) and elapsed <= timer):
            newTempo = newTempo-increment
            hapticSerial.write((str(newTempo)+ CRLF).encode())
            print('STAGE FOUR: ' + str(newTempo))
        else:
            hapticSerial.write((OFF+CRLF).encode())
            break
    global closeFile
    closeFile = True
    time.sleep(1)

def playback(audio_file):
    playBeep()
    mixer.pre_init(44100, -16, 2, 2048)
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.set_volume(0.4)
    mixer.music.play()
    # mixer.music.fadeout(20500)
    while mixer.music.get_busy():
        pass
    global closeFile
    closeFile = True
    time.sleep(1)
    # playBeep()

def playBeep():
    global startRead
    mixer.pre_init(44100, -16, 2, 2048)
    mixer.init()
    mixer.music.load(audioFile[16])
    mixer.music.set_volume(0.1)
    mixer.music.play()
    mixer.music.fadeout(5000)
    while mixer.music.get_busy():
        pass
    time.sleep(1)
    startRead = True
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
    # output = "%i %i %i"%(tap_onset,tap_offset,maxforce)
    # print (output)

    return tap_onset,tap_offset,maxforce

def getTap():
    global closeFile,startRead
    readyFlag = False
    # if not (os.path.isdir('/Users/nickpourazima/GitHub/he-sm/TestOutput/'+userName)):
    #     os.makedirs('/Users/nickpourazima/GitHub/he-sm/TestOutput/'+userName)
    # currentPath = '/Users/nickpourazima/GitHub/he-sm/TestOutput/'+str(userName)
    # filename = (userName+' '+t0+' '+time.asctime()) # get the filename we are supposed to output to
    # completeName = os.path.join(currentPath,filename)
    # print (completeName)
    # dumpfile = open(completeName,'w')
    # output_header = "onset offset maxforce"
    # dumpfile.write(output_header+"\n")
    print("before startRead")
    print(startRead)
    if startRead:
        print("after startRead")
        tapSerial.reset_input_buffer()
        readyFlag = True
        start = time.time()
    while readyFlag:
        end = time.time()
        elapsed = end - start
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
                onset,offset,maxforce = interpret_output_discrete(s)
                tapData.append([timestamp.now(),None,None,elapsed,onset,offset,maxforce])
                # dumpfile.write(output+"\n")
                # dumpfile.flush()
        if closeFile:
            closeFile = False
            startRead = False
            break


hapticTestCases = {
    'H1a1': (DISCRETE,BPM1,20),
    'H1a2': (DISCRETE,BPM2,20),
    'H1a3': (DISCRETE,BPM3,20),
    'H1a4': (DISCRETE,BPM4,20),
    'H1b1': (CONTINOUS,BPM1,20),
    'H1b2': (CONTINOUS,BPM2,20),
    'H1b3': (CONTINOUS,BPM3,20),
    'H1b4': (CONTINOUS,BPM4,20),
    'H2a1': (DISCRETE,BPM1,20),
    'H2a2': (DISCRETE,BPM2,20),
    'H2a3': (DISCRETE,BPM3,20),
    'H2a4': (DISCRETE,BPM4,20),
    'H2b1': (CONTINOUS,BPM1,20),
    'H2b2': (CONTINOUS,BPM2,20),
    'H2b3': (CONTINOUS,BPM3,20),
    'H2b4': (CONTINOUS,BPM4,20)
}
audioTestCases = {
    'A1a1': audioFile[0],
    'A1a2': audioFile[1],
    'A1a3': audioFile[2],
    'A1a4': audioFile[3],
    'A1b1': audioFile[4],
    'A1b2': audioFile[5],
    'A1b3': audioFile[6],
    'A1b4': audioFile[7],
    'A2a1': audioFile[8],
    'A2a2': audioFile[9],
    'A2a3': audioFile[10],
    'A2a4': audioFile[11],
    'A2b1': audioFile[12],
    'A2b2': audioFile[13],
    'A2b3': audioFile[14],
    'A2b4': audioFile[15]
}

def main():
    #practice mode
    global t0
    #run through test cases (randomly)
    hapticKeys = list(hapticTestCases.keys())
    shuffle(hapticKeys)

    audioKeys = list(audioTestCases.keys())
    shuffle(audioKeys)

    allKeys = hapticKeys + audioKeys
    shuffle(allKeys)
    # print(allKeys)
    # for key in allKeys:
    #     t0 = key
    #     if(t0[:2]=='H1'):
    #         t1 = Thread(target = steady_haptic, args = hapticTestCases.get(key))
    #     elif(t0[:2]=='H2'):
    #         t1 = Thread(target = dynamic_haptic, args = hapticTestCases.get(key))
    #     elif(t0[0]=='A'):
    #         t1 = Thread(target = playback, args = [audioTestCases.get(key)])
    #     t2 = Thread(target= getTap)
    #     t1.start()
    #     t2.start()
    #     t1.join()
    #     t2.join()

    t0 = Thread(target=playBeep)
    t0.start()
    t0.join()
    t1 = Thread(target=steady_haptic, args = (CONTINOUS,'60',10))
    t2 = Thread(target=getTap)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    combo = hapticData+tapData
    print (tabulate(combo,headers=['Timestamp','Haptic Elapsed Time','Haptic Onset','Tap Elapsed Time','Tap Onset','Tap Offset','Tap Maxforce']))
    
    # dynamic_haptic(CONTINOUS,'60',20)

    print("FINISHED")
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
    
