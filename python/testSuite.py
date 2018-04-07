import serial
import time
import Tkinter
#from tkinter import *
from functools import partial
from random import shuffle
from Tkinter import *

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
class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("HESM Test Suite")

        self.label = Label(master, text="Subject Name:")
        self.label.pack()

        self.greet_button = Button(master, text="Output File: ", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")
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

#open serial
ser = serial.Serial(SERIAL_PORT, BAUD)
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
    #get users name

    #open save file

    #build gui

    #instructions && user inputs ready key

    #practice mode

    #run through test cases (can do random or in order)

    # keys = hapticTestCases.keys()
    # shuffle(keys)
    # print keys
    # for key in keys:
    #     hapticTestCases[key]()
    root = Tk()
    my_gui = MyFirstGUI(root)
    root.mainloop()

    #blank window or brief reset before next test

    #upon finishing, close serial
    #summary && output file presented

if __name__ == "__main__":
    main()