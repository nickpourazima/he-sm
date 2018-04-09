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

#TO-DO Tomorrow
# finish building audio, music, and dynamic tests
# interface to FSR SW
# integrate intermediary gui page


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
        button1 =   tk.Button(self, text="Agree.",
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
        self.label = tk.Label(self, text="GET READY!!!", font=LARGE_FONT)
        self.label.pack(pady=10,padx=10)
        self.flash()

        button1 = tk.Button(self,text="START",command=self.end)
        button1.pack()

    def flash(self):
        bg = self.label.cget("background")
        fg = self.label.cget("foreground")
        self.label.configure(background=fg, foreground=bg)
        self.after(500, self.flash)

    def end(self):
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
    playBeep()

def playback(audio_file):
    mixer.pre_init(44100, -16, 2, 2048)
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
    mixer.init()
    mixer.music.load(audioFile[4])
    mixer.music.set_volume(0.1)
    mixer.music.play()
    mixer.music.fadeout(3000)
    while mixer.music.get_busy():
        pass
    print ("Starting...")

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

audioTestCases = {
    'A1a1': partial(playback,audioFile[0]),
    'A1a2': partial(playback,audioFile[1]),
    'A1a3': partial(playback,audioFile[2]),
    'A1a4': partial(playback,audioFile[3]),
    'A1b1': partial(playback,audioFile[0]),
    'A1b2': partial(playback,audioFile[1]),
    'A1b3': partial(playback,audioFile[2]),
    'A1b4': partial(playback,audioFile[3]),
}
def main():
    #practice mode

    #run through test cases (can do random or in order)

    hapticKeys = list(hapticTestCases.keys())
    shuffle(hapticKeys)
    print (hapticKeys)
    # for key in hapticKeys:
    #     hapticTestCases[key]()
    
    audioKeys = list(audioTestCases.keys())
    shuffle(audioKeys)
    print (audioKeys)
    # for key in audioKeys:
    #     audioTestCases[key]()

    print (userName)
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
        print ("Didn't run main()")