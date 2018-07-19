#   Author: Nick Pourazima
#   School: Carnegie Mellon University
#   Department: Music Technology
#   Contact: npourazima@gmail.com
#   Date: ~Spring 2018
#   Description:
#       Master test suite contol for haptic (Pro Trinket 5V 16MHz) and FSR tap hardware (Arduino Uno).
#       Synchronizes timing via multi-threaded operations. Outputs test cases for analysis.

# TODO
# comments/clean up code

import openpyxl
import webbrowser
import serial
import plotly
from plotly.graph_objs import Scatter, Layout
import plotly.tools as tls
import plotly.plotly as py
import plotly.graph_objs as go
import time
import os
import glob
import random
import tkinter as tk
import sys
import datetime as dt
from datetime import timedelta
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.dates as md
mpl.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from matplotlib.ticker import FormatStrFormatter
import seaborn as sns
from functools import partial
from random import shuffle
from pygame import mixer
from collections import defaultdict
from threading import Thread
from tabulate import tabulate

# SERIAL VARS
TAP_SERIAL_PORT = '/dev/tty.usbmodem14131'
TAP_BAUD = 115200
TIMEOUT = 0.25

HAPTIC_SERIAL_PORT = '/dev/tty.usbserial-A907CAHB'
HAPTIC_BAUD = 115200

# TEMPO INFO
BPM1 = '45'
BPM2 = '90'
BPM3 = '135'
BPM4 = '180'

# HAPTIC VARS
OFF = '0'
DISCRETE = '1'
CONTINOUS = '2'
CRLF = '\r\n'

# GUI VARS
LARGE_FONT = ("Verdana", 18)

# Get Tap / Write File VARS
PACKET_LENGTH = 8
startFlag = False
closeFile = False
startRead = False
t0 = ''
userName = ""
userID = 0
timestamp = dt.datetime
bpmChange = []
currentPath = ''
fadeoutTimer = 5000

instructions = (
    "The following tests measure your ability to synchronize to a varying beat across touch and sound and will take approximately 20 minutes to complete."
    + CRLF+CRLF+CRLF +
    "Carefully place the wearable haptic sleeve on the arm of your choice and designate either your non-dominant or dominant hand to tap on the pad."
    + CRLF +
    "You will hear OR feel a series of audio and haptic (touch) based trials."
    + CRLF +
    "Each are varying in duration and tempo."
    + CRLF +
    "The start of every test is marked with a 3 second long beep."
    + CRLF +
    "Once the test starts please try your best to firmly and quickly tap on the pad to the presented beat."
    + CRLF +
    "For the music based tests, tap on every note."
    + CRLF+CRLF +
    "For the continuous haptic tests, you will feel a pulse moving down and then back up."
    + CRLF +
    "The beat is the pulse felt at the bottom, closest to your hand."
    + CRLF +
    "There will be a practice period of 8 tests which sample a few of the test types."
    + CRLF +
    "You will then hear 3 short beeps and one long beep indicating that the real test will commence."
    + CRLF+CRLF+CRLF +
    "When you are ready advance to the next page and click Start to begin the practice test."
    + CRLF +
    "At the end of the test a survey will popup in the browser, please fill it out."
    + CRLF+CRLF+CRLF +
    "Thank you for your participation!"
    + CRLF+CRLF+CRLF+CRLF
)
audioFile = [
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/click_44.1_16bit_20sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_30sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_16sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_11sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/swing_click_44.1_16bit_8sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_32sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_16sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_11sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/staccato_44.1_16bit_8sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_32sec_45bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_16sec_90bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_11sec_135bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/cres_f_decres_mp_44.1_16bit_8sec_180bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_click_44.1_16bit_20sec_30-60bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_click_44.1_16bit_10sec_75-105bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_click_44.1_16bit_10sec_120-150bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_click_44.1_16bit_10sec_165-195bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_swing_click_44.1_16bit_20sec_30-60bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_swing_click_44.1_16bit_10sec_75-105bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_swing_click_44.1_16bit_10sec_120-150bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_swing_click_44.1_16bit_10sec_165-195bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_staccato_44.1_16bit_30sec_30-60bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_staccato_44.1_16bit_15sec_75-105bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_staccato_44.1_16bit_10sec_120-150bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_staccato_44.1_16bit_10sec_165-195bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_cres_f_decres_mp_44.1_16bit_30sec_30-60bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_cres_f_decres_mp_44.1_16bit_15sec_75-105bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_cres_f_decres_mp_44.1_16bit_10sec_120-150bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/dynamic_cres_f_decres_mp_44.1_16bit_10sec_165-195bpm.wav',
    '/Users/nickpourazima/GitHub/he-sm/AudioFiles/beep-11.wav'
]
audioOnsets = defaultdict(list)
audioOnsets = {
    'A1a1': [1.34675737, 2.67029478, 4.01705215, 5.34058957, 6.68734694, 8.01088435,
             9.35764172, 10.68117914, 12.00471655, 13.35147392, 14.67501134, 16.02176871,
             17.34530612, 18.69206349, 20.01560091],
    'A1a2': [0.67337868, 1.34675737, 2.02013605, 2.67029478, 3.34367347, 4.01705215,
             4.69043084, 5.34058957, 6.01396825, 6.68734694, 7.33750567, 8.01088435,
             8.68426304, 9.35764172, 10.00780045, 10.68117914, 11.35455782, 12.00471655,
             12.67809524, 13.35147392, 14.02485261, 14.67501134, 15.34839002, 16.02176871,
             16.67192744, 17.34530612, 18.01868481, 18.69206349, 19.34222222, 20.01560091],
    'A1a3': [0.46439909, 0.90557823, 1.34675737, 1.78793651, 2.22911565, 2.67029478,
             3.13469388, 3.57587302, 4.01705215, 4.45823129, 4.89941043, 5.34058957,
             5.78176871, 6.2461678,  6.68734694, 7.12852608, 7.56970522, 8.01088435,
             8.45206349, 8.89324263, 9.35764172, 9.79882086, 10.24, 10.68117914,
             11.12235828, 11.56353741, 12.00471655, 12.46911565, 12.91029478, 13.35147392,
             13.79265306, 14.2338322,  14.67501134, 15.11619048, 15.58058957, 16.02176871,
             16.46294785, 16.90412698, 17.34530612, 17.78648526, 18.2276644, 18.69206349,
             19.13324263, 19.57442177, 20.01560091],
    'A1a4': [0.34829932, 0.67337868, 1.021678, 1.34675737, 1.67183673, 2.02013605,
             2.34521542, 2.67029478, 3.0185941, 3.34367347, 3.69197279, 4.01705215,
             4.34213152, 4.69043084, 5.0155102, 5.34058957, 5.68888889, 6.01396825,
             6.33904762, 6.68734694, 7.0124263, 7.33750567, 7.68580499, 8.01088435,
             8.35918367, 8.68426304, 9.0093424,  9.35764172, 9.68272109, 10.00780045,
             10.35609977, 10.68117914, 11.0062585, 11.35455782, 11.67963719, 12.00471655,
             12.35301587, 12.67809524, 13.0031746, 13.35147392, 13.67655329, 14.02485261,
             14.34993197, 14.67501134, 15.02331066, 15.34839002, 15.67346939, 16.02176871,
             16.34684807, 16.67192744, 17.02022676, 17.34530612, 17.67038549, 18.01868481,
             18.34376417, 18.69206349, 19.01714286, 19.34222222, 19.69052154, 20.01560091],
    'A1b1': [0.00000001, 1.34675737, 2.69351474, 4.01705215, 5.36380952, 6.68734694, 8.01088435,
             9.35764172, 10.68117914, 12.02793651, 13.35147392, 14.69823129, 16.02176871,
             17.34530612, 18.69206349, 20.01560091, 21.36235828, 22.68589569, 24.00943311,
             25.35619048, 26.67972789, 28.02648526, 29.35002268, 30.69678005],
    'A1b2': [0.00000001, 0.69659864, 1.34675737, 2.02013605, 2.69351474, 3.34367347, 4.01705215,
             4.69043084, 5.36380952, 6.01396825, 6.68734694, 7.36072562, 8.01088435,
             8.68426304, 9.35764172, 10.03102041, 10.68117914, 11.35455782,
             12.02793651, 12.67809524, 13.35147392, 14.02485261, 14.69823129,
             15.34839002],
    'A1b3': [0.00000001, 0.46439909, 0.90557823, 
             1.34675737, 1.81115646, 2.2523356, 2.69351474, 3.13469388,
             3.57587302, 4.01705215, 4.45823129, 4.89941043, 
             5.36380952, 5.80498866, 6.2461678, 
             6.68734694, 7.12852608, 7.56970522, 8.01088435,
             8.47528345, 8.91646259, 9.35764172, 9.79882086, 10.24],
    'A1b4': [0.0000001, 0.34829932, 0.69659864, 1.021678,
                1.34675737, 1.69505669, 2.02013605, 2.34521542, 
                2.69351474, 3.0185941, 3.36689342, 3.69197279, 
                4.01705215, 4.36535147, 4.69043084, 5.0155102, 
                5.36380952, 5.68888889, 6.01396825, 6.36226757, 
                6.68734694, 7.0124263, 7.36072562, 7.68580499],
    'A2a1': [1.34675737, 2.69351474, 4.01705215, 5.34058957, 6.68734694, 8.01088435,
             9.35764172, 10.68117914, 12.02793651, 13.35147392, 14.67501134, 16.02176871,
             17.34530612, 18.69206349, 20.01560091, 21.36235828, 22.68589569, 24.00943311,
             25.35619048, 26.67972789, 28.02648526],
    'A2a2': [0.69659864, 1.34675737, 2.02013605, 2.69351474, 3.34367347, 4.01705215,
             4.69043084, 5.36380952, 6.01396825, 6.68734694, 7.36072562, 8.01088435,
             8.68426304, 9.35764172, 10.03102041, 10.68117914, 11.35455782, 12.02793651,
             12.67809524, 13.35147392, 14.02485261],
    'A2a3': [0.46439909, 0.90557823, 1.34675737, 1.78793651, 2.2523356, 2.69351474,
             3.13469388, 3.57587302, 4.01705215, 4.45823129, 4.89941043, 5.36380952,
             5.80498866, 6.2461678, 6.68734694, 7.12852608, 7.56970522, 8.01088435,
             8.47528345, 8.91646259, 9.35764172],
    'A2a4': [0.34829932, 0.69659864, 1.021678, 1.34675737, 1.69505669, 2.02013605,
             2.34521542, 2.69351474, 3.0185941, 3.34367347, 3.69197279, 4.01705215,
             4.36535147, 4.69043084, 5.0155102, 5.36380952, 5.68888889, 6.01396825,
             6.36226757, 6.68734694, 7.0124263],
    'A2b1': [1.34675737, 2.69351474, 4.01705215, 5.36380952, 6.68734694, 8.01088435,
             9.35764172, 10.68117914, 12.02793651, 13.35147392, 14.69823129, 16.02176871,
             17.34530612, 18.69206349, 20.01560091, 21.36235828, 22.68589569, 24.00943311,
             25.35619048, 26.67972789, 28.02648526],
    'A2b2': [0.69659864, 1.34675737, 2.02013605, 2.69351474, 3.34367347, 4.01705215,
             4.69043084, 5.36380952, 6.01396825, 6.68734694, 7.36072562, 8.01088435,
             8.68426304, 9.35764172, 10.03102041, 10.68117914, 11.35455782, 12.02793651,
             12.67809524, 13.35147392, 14.02485261],
    'A2b3': [0.46439909, 0.90557823, 1.34675737, 1.78793651, 2.2523356, 2.69351474,
             3.13469388, 3.57587302, 4.01705215, 4.45823129, 4.89941043, 5.36380952,
             5.80498866, 6.2461678, 6.68734694, 7.12852608, 7.56970522, 8.01088435,
             8.47528345, 8.91646259, 9.35764172],
    'A2b4': [0.34829932, 0.69659864, 1.021678, 1.34675737, 1.69505669, 2.02013605,
             2.34521542, 2.69351474, 3.0185941, 3.36689342, 3.69197279, 4.01705215,
             4.36535147, 4.69043084, 5.0155102, 5.36380952, 5.68888889, 6.01396825,
             6.36226757, 6.68734694, 7.0124263],
    'A3a1': [1.13777778, 2.20589569, 3.7384127, 5.50312925, 6.64090703, 7.63936508,
             8.68426304, 10.35609977, 11.70285714, 12.77097506, 14.32671202, 16.20752834,
             17.43818594, 18.45986395, 19.7137415],
    'A3a2': [0.62693878, 1.20743764, 1.92725624, 2.67029478, 3.27401361, 3.85451247,
             4.43501134, 5.17804989, 5.85142857, 6.43192744, 7.15174603, 7.91800454,
             8.54494331, 9.12544218],
    'A3a3': [0.44117914, 0.85913832, 1.25387755, 1.67183673, 2.08979592, 2.53097506,
             3.0185941, 3.50621315, 4.01705215, 4.48145125, 4.96907029, 5.41024943,
             5.82820862, 6.29260771, 6.7570068, 7.2678458, 7.75546485, 8.19664399, 8.63782313,
             9.03256236, 9.45052154, 9.84526077, 10.28643991],
    'A3a4': [0.34829932, 0.67337868, 0.9752381, 1.27709751, 1.60217687, 1.90403628,
             2.22911565, 2.55419501, 2.90249433, 3.25079365, 3.59909297, 3.97061224,
             4.31891156, 4.64399093, 4.96907029, 5.29414966, 5.61922902, 5.92108844,
             6.2461678, 6.59446712, 6.94276644, 7.29106576, 7.66258503, 8.01088435,
             8.38240363, 8.70748299, 9.03256236, 9.33442177, 9.63628118, 9.96136054,
             10.28643991, 10.61151927],
    'A3b1': [0.00000001, 1.13777778, 2.20589569, 3.7384127, 5.52634921, 6.64090703, 7.63936508,
             8.70748299, 10.35609977, 11.70285714, 12.77097506, 14.32671202, 16.20752834,
             17.43818594, 18.4830839],
    'A3b2': [0.00000001, 0.62693878, 1.2306576, 1.92725624, 2.67029478,
             3.29723356, 3.85451247, 4.45823129, 5.17804989, 5.85142857,
             6.43192744, 7.15174603, 7.91800454, 8.54494331, 9.12544218],
    'A3b3': [0.00000001, 0.46439909, 0.85913832, 
             1.27709751, 1.67183673, 2.08979592, 2.55419501,
             3.0185941, 3.52943311, 4.01705215, 4.5046712, 4.96907029,
             5.43346939, 5.85142857, 6.29260771, 6.78022676, 
             7.2678458, 7.75546485, 7.87156463, 8.21986395, 8.63782313,
             9.05578231, 9.45052154, 9.86848073, 
             10.28643991],
    'A3b4': [0.00000001, 0.34829932, 0.67337868, 0.9752381, 1.30031746,
             1.60217687, 1.90403628, 2.22911565, 2.57741497, 2.90249433, 
             3.27401361, 3.62231293, 3.97061224, 4.31891156, 4.66721088, 
             4.99229025, 5.29414966, 5.61922902, 5.92108844, 6.2461678,
             6.59446712, 6.94276644, 7.31428571, 7.66258503, 8.03410431, 
             8.38240363, 8.70748299, 9.03256236, 9.33442177, 9.65950113,
             9.96136054, 10.28643991, 10.61151927],
    'A4a1': [1.34675737, 2.69351474, 4.01705215, 5.15482993, 6.22294785, 7.7322449,
             9.52018141, 10.63473923, 11.65641723, 12.70131519, 14.34993197, 15.7199093,
             16.76480726, 18.32054422, 20.2245805, 21.47845805, 22.52335601, 23.73079365,
             25.07755102, 26.40108844, 27.72462585],
    'A4a2': [0.69659864, 1.34675737, 2.02013605, 2.62385488, 3.2275737, 3.92417234,
             4.69043084, 5.29414966, 5.85142857, 6.45514739, 7.17496599, 7.84834467,
             8.45206349, 9.14866213, 9.93814059, 10.54185941, 11.12235828, 11.79573696,
             12.44589569, 13.11927438, 13.79265306],
    'A4a3': [0.44117914, 0.85913832, 1.27709751, 1.67183673, 2.08979592, 2.53097506,
             3.0185941, 3.52943311, 4.01705215, 4.5046712, 4.96907029, 5.43346939,
             5.85142857, 6.29260771, 6.78022676, 7.2678458, 7.75546485, 8.21986395,
             8.63782313, 9.05578231, 9.45052154],
    'A4a4': [0.34829932, 0.67337868, 0.9752381, 1.30031746, 1.60217687, 1.90403628,
             2.22911565, 2.57741497, 2.90249433, 3.27401361, 3.62231293, 3.97061224,
             4.31891156, 4.66721088, 4.99229025, 5.31736961, 5.61922902, 5.92108844,
             6.2461678, 6.59446712, 6.94276644],
    'A4b1': [1.34675737, 2.69351474, 4.01705215, 5.15482993, 6.22294785, 7.7322449,
             9.52018141, 10.63473923, 11.65641723, 12.70131519, 14.34993197, 15.7199093,
             16.76480726, 18.32054422, 20.2245805, 21.47845805, 22.52335601, 23.73079365,
             25.07755102, 26.40108844, 27.7478458],
    'A4b2': [0.69659864, 1.34675737, 2.02013605, 2.62385488, 3.2275737, 3.92417234,
             4.69043084, 5.29414966, 5.87464853, 6.45514739, 7.17496599, 7.84834467,
             8.45206349, 9.14866213, 9.93814059, 10.54185941, 11.14557823, 11.79573696,
             12.44589569, 13.11927438, 13.79265306],
    'A4b3': [0.44117914, 0.85913832, 1.27709751, 1.67183673, 2.08979592, 2.55419501,
             3.0185941, 3.52943311, 4.01705215, 4.5046712, 4.96907029, 5.43346939,
             5.85142857, 6.29260771, 6.78022676, 7.2678458, 7.75546485, 8.21986395,
             8.63782313, 9.05578231, 9.45052154],
    'A4b4': [0.34829932, 0.67337868, 0.9752381, 1.30031746, 1.6021768, 1.90403628,
             2.22911565, 2.57741497, 2.92571429, 3.27401361, 3.62231293, 3.97061224,
             4.31891156, 4.66721088, 4.99229025, 5.31736961, 5.61922902, 5.92108844,
             6.2461678, 6.59446712, 6.94276644]
}

hapticTestCases = {
    'H1a1': (True, DISCRETE, BPM1, 15),
    'H1a2': (True, DISCRETE, BPM2, 15),
    'H1a3': (True, DISCRETE, BPM3, 15),
    'H1a4': (True, DISCRETE, BPM4, 15),
    'H1b1': (True, CONTINOUS, BPM1, 15),
    'H1b2': (True, CONTINOUS, BPM2, 15),
    'H1b3': (True, CONTINOUS, BPM3, 15),
    'H1b4': (True, CONTINOUS, BPM4, 15),
    'H2a1': (False, DISCRETE, BPM1, 15, 10),
    'H2a2': (False, DISCRETE, BPM2, 15, 5),
    'H2a3': (False, DISCRETE, BPM3, 15, 3),
    'H2a4': (False, DISCRETE, BPM4, 15, 1),
    'H2b1': (False, CONTINOUS, BPM1, 15, 10),
    'H2b2': (False, CONTINOUS, BPM2, 15, 5),
    'H2b3': (False, CONTINOUS, BPM3, 15, 3),
    'H2b4': (False, CONTINOUS, BPM4, 15, 1)
}
practiceTests = {
    'P1H1a1': (True, DISCRETE, BPM1, 10),
    'P2H1a2': (True, DISCRETE, BPM2, 10),
    'P3H1b1': (True, CONTINOUS, BPM1, 10),
    'P4H1b2': (True, CONTINOUS, BPM2, 10),
    'P5H1b3': (True, CONTINOUS, BPM3, 10),
    'P6A1a2': audioFile[1],
    'P7A1b1': audioFile[4],
    'P8A2a1': audioFile[8]
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
    'A2b4': audioFile[15],
    'A3a1': audioFile[16],
    'A3a2': audioFile[17],
    'A3a3': audioFile[18],
    'A3a4': audioFile[19],
    'A3b1': audioFile[20],
    'A3b2': audioFile[21],
    'A3b3': audioFile[22],
    'A3b4': audioFile[23],
    'A4a1': audioFile[24],
    'A4a2': audioFile[25],
    'A4a3': audioFile[26],
    'A4a4': audioFile[27],
    'A4b1': audioFile[28],
    'A4b2': audioFile[29],
    'A4b3': audioFile[30],
    'A4b4': audioFile[31],
}
audioTestCases2 = {
    'A1a1': audioFile[0],
    'A1a2': audioFile[1],
    'A1a3': audioFile[2],
    'A1a4': audioFile[3],
    'A3a1': audioFile[16],
    'A3a2': audioFile[17],
    'A3a3': audioFile[18],
    'A3a4': audioFile[19],
}

hapticList1 = ['H1a1','H1a2','H1a3','H1a4','H2a1','H2a2','H2a3','H2a4']
hapticList2 = ['H1b1','H1b2','H1b3','H1b4','H2b1','H2b2','H2b3','H2b4']
# check for serial
if(os.path.exists(HAPTIC_SERIAL_PORT) and os.path.exists(TAP_SERIAL_PORT)):
    hapticSerial = serial.Serial(HAPTIC_SERIAL_PORT, HAPTIC_BAUD)
    tapSerial = serial.Serial(TAP_SERIAL_PORT, TAP_BAUD, timeout=TIMEOUT)
else:
    print("No serial connected...")
    sys.exit()

# initialize new dataframe
df = {
    'Test':             [],
    'User ID':          [],
    'True Onset':       [],
    'Tap Onset':        [],
    'Asynchrony':       []
}

class mainGUI(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

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
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Please enter your name:", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        self.name = tk.Entry(self)  # add the text entry box for the value
        self.name.pack(padx=5)
        self.myController = controller
        button = tk.Button(self, text="Instructions",
                           command=self.advance)
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
        label.pack(pady=10, padx=10)
        self.myController = controller
        button1 = tk.Button(self, text="Accept",
                            command=self.advance)
        button1.pack()
        button2 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button2.pack()

    def advance(self):
        global startFlag
        startFlag = True
        self.myController.show_frame(TestPage)

class TestPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Get ready!"
                              + CRLF +
                              "Remember, the first 8 tests are practice."
                              + CRLF +
                              "Afterwards, you will hear 3 (1 second) beeps indicating that the real test will begin."
                              + CRLF, font=LARGE_FONT)
        self.label.pack(pady=10, padx=10)
        # self.flash()
        button1 = tk.Button(
            self, text="Start Test", command=self.quit)
        button1.pack()

    def flash(self):
        bg = self.label.cget("background")
        fg = self.label.cget("foreground")
        self.label.configure(background=fg, foreground=bg)
        self.after(500, self.flash)

def haptic(steady, mode, tempo, timer, increment=1):
    global closeFile, startRead, df
    readyFlag = False

    if startRead:
        hapticSerial.write((mode + CRLF).encode())
        hapticSerial.write((tempo + CRLF).encode())
        hapticSerial.flush()
        if steady:
            pass
        elif not steady:
            newTempo = int(tempo)
        readyFlag = True
        start = time.time()

    while readyFlag:
        end = time.time()
        elapsed = end - start
        isOnset = hapticSerial.readline()  # .decode('utf-8')
        if(isOnset == b'onset\r\n'):
            df['True Onset'].append(pd.Timestamp.now())
        if(not steady and elapsed <= timer/4):
            newTempo = newTempo+increment
            hapticSerial.write((str(newTempo) + CRLF).encode())
            bpmChange.append([None, None, None, str(newTempo), None, None])
        elif(not steady and elapsed >= timer/4 and elapsed <= timer/2):
            newTempo = newTempo-increment
            hapticSerial.write((str(newTempo) + CRLF).encode())
            bpmChange.append([None, None, None, str(newTempo), None, None])
        elif(not steady and elapsed >= timer/2 and elapsed <= (timer/2+timer/4)):
            newTempo = newTempo+increment
            hapticSerial.write((str(newTempo) + CRLF).encode())
            bpmChange.append([None, None, None, str(newTempo), None, None])
        elif(not steady and elapsed >= (timer/2+timer/4) and elapsed <= timer):
            newTempo = newTempo-increment
            hapticSerial.write((str(newTempo) + CRLF).encode())
            bpmChange.append([None, None, None, str(newTempo), None, None])

        df['User ID'].append(userID)
        df['Test'].append(t0)
        if(elapsed >= timer):
            hapticSerial.write((OFF+CRLF).encode())
            closeFile = True
            break

def playback(audio_file):
    global closeFile, df
    mixer.pre_init(44100, -16, 2, 64)
    mixer.init()
    mixer.music.load(audio_file)
    mixer.music.set_volume(0.4)
    mixer.music.play()
    testTime = []
    while mixer.music.get_busy():
        testTime.append(pd.Timestamp.now())
        pass
    startTime = testTime[0]
    if(t0[0] == 'P'):
        key = t0[2:6]
        onset = list(audioOnsets.get(key))
    else:
        onset = list(audioOnsets.get(t0))
    for item in onset:
        df['True Onset'].append(startTime+dt.timedelta(0, item))
        df['User ID'].append(userID)
        df['Test'].append(t0)
    closeFile = True

def playBeep(fadeoutTimer):
    global startRead
    mixer.pre_init(44100, -16, 2, 64)
    mixer.init()
    mixer.music.load(audioFile[32])
    mixer.music.set_volume(0.05)
    mixer.music.play()
    mixer.music.fadeout(fadeoutTimer)
    while mixer.music.get_busy():
        pass
    time.sleep(1)
    startRead = True

def getTap():
    global closeFile, startRead, df
    readyFlag = False
    if startRead:
        tapSerial.reset_input_buffer()
        readyFlag = True
    while readyFlag:
        # Ok, let's read one byte
        r = tapSerial.read(1)
        if bytes.decode(r) == "B":  # This could be the beginning of a packet from arduino
            avail = 0  # how many bytes are available
            while avail < PACKET_LENGTH-1:  # read to fill up the packet
                avail = tapSerial.inWaiting()
            # all right, now we can read
            # read the whole packet straight away
            r = tapSerial.read(PACKET_LENGTH-1)
            s = str(r, 'latin-1')
            # Now continue to work with this
            # if we have the correct ending also
            if len(s) == (PACKET_LENGTH-1) and s[-1] == "E":
                df['Tap Onset'].append(pd.Timestamp.now())
        if closeFile:
            closeFile = False
            startRead = False
            break

def dataAnalysis(count):
    global df,hapticList1,hapticList2
    rawData = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in df.items()]))
    rawData = rawData.drop_duplicates(subset=['True Onset'], keep=False)
    rawData['Asynchrony'] = (rawData['Tap Onset'] -
                             rawData['True Onset'])/np.timedelta64(1, 'ms')
    rawData['IOI'] = pd.to_timedelta((rawData['True Onset'].shift(-1)-rawData['True Onset']),unit='ms')/np.timedelta64(1, 'ms')
    rawData['Max'] = (pd.to_timedelta((rawData['IOI'])*.5,
                                      unit='ms')+(rawData['True Onset']))
    rawData['Min'] = (pd.to_timedelta((rawData['IOI'].shift(1))
                                      * .5, unit='ms')+(rawData['True Onset'].shift(1)))

    # # SANITIZE
    # print(range(rawData.shape[0]))
    # for i in reversed(range(rawData.shape[0])):
    #     conditions = [
    #         ((rawData['Tap Onset'].shift(i) >= rawData['Min']) & (rawData['Tap Onset'].shift(i) < rawData['Max'])),
    #         ((rawData['Tap Onset'] >= rawData['Min']) & (rawData['Tap Onset'] < rawData['Max'])),
    #         ((rawData['Tap Onset'].shift(i*-1) >= rawData['Min']) & (rawData['Tap Onset'].shift(i*-1) < rawData['Max']))
    #     ]
    #     choices = [rawData['Tap Onset'].shift(i),rawData['Tap Onset'],rawData['Tap Onset'].shift(i*-1)]
    #     rawData['Sanitized Tap Onset'] = np.select(conditions,choices,default=np.timedelta64('NaT'))

    conditions = [
        ((rawData['Tap Onset'].shift(10) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(10) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(9) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(9) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(8) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(8) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(7) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(7) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(6) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(6) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(5) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(5) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(4) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(4) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(3) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(3) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(2) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(2) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(1) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(1) < rawData['Max'])),
        ((rawData['Tap Onset'] >= rawData['Min']) &
         (rawData['Tap Onset'] < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-1) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-1) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-2) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-2) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-3) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-3) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-4) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-4) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-5) >= rawData['Min'])
         & (rawData['Tap Onset'].shift(-5) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-6) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-6) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-7) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-7) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-8) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-8) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-9) >= rawData['Min']) &
         (rawData['Tap Onset'].shift(-9) < rawData['Max'])),
        ((rawData['Tap Onset'].shift(-10) >= rawData['Min'])
         & (rawData['Tap Onset'].shift(-10) < rawData['Max']))
        ]
    choices = [
        rawData['Tap Onset'].shift(10), rawData['Tap Onset'].shift(9), rawData['Tap Onset'].shift(8), rawData['Tap Onset'].shift(7), 
        rawData['Tap Onset'].shift(6),rawData['Tap Onset'].shift(5), rawData['Tap Onset'].shift(4), rawData['Tap Onset'].shift(3), 
        rawData['Tap Onset'].shift(2), rawData['Tap Onset'].shift(1), rawData['Tap Onset'], rawData['Tap Onset'].shift(-1), 
        rawData['Tap Onset'].shift(-2), rawData['Tap Onset'].shift(-3), rawData['Tap Onset'].shift(-4), rawData['Tap Onset'].shift(-5), 
        rawData['Tap Onset'].shift(-6), rawData['Tap Onset'].shift(-7), rawData['Tap Onset'].shift(-8), rawData['Tap Onset'].shift(-9), 
        rawData['Tap Onset'].shift(-10)
        ]
    rawData['Sanitized Tap Onset'] = np.select(
        conditions, choices, default=np.timedelta64('NaT'))

    rawData['Sanitized Asynchrony'] = (
        rawData['Sanitized Tap Onset']-rawData['True Onset'])/np.timedelta64(1, 'ms')

    rawData = rawData.dropna(subset=['True Onset', 'Max', 'Min'], how='any')
    rawData = rawData.drop_duplicates(subset=['True Onset'], keep=False)

    rawData['Sanitized Mean Asynchrony'] = rawData.groupby(
        'Test')['Sanitized Asynchrony'].transform('mean')
    rawData['Sanitized Std Dev Asynchrony'] = rawData.groupby(
        'Test')['Sanitized Asynchrony'].transform('std')
    rawData['Mean Asynchrony'] = rawData.groupby(
        'Test')['Asynchrony'].transform('mean')
    rawData['Std Dev Asynchrony'] = rawData.groupby(
        'Test')['Asynchrony'].transform('std')
    rawData['Missed Taps'] = rawData['Sanitized Tap Onset'].isnull().sum(axis=0)
    rawData['Phase Correction Response'] = rawData['Sanitized Asynchrony'].shift(-1)-rawData['Sanitized Asynchrony']

    if(rawData[rawData['Test'].isin([hapticList1])]){
        rawData['Latency'] = (rawData['IOI']*1)/4
        rawData['Latency Corrected SA'] = rawData['Sanitized Asynchrony']+rawData['Latency']

    }
    elif(rawData[rawData['Test'].isin([hapticList2])]){
        rawData['Latency'] = (rawData['IOI']*2)/9
        rawData['Latency Corrected SA'] = rawData['Sanitized Asynchrony']+rawData['Latency']
    }

    if not (os.path.isdir('/Users/nickpourazima/GitHub/he-sm/TestOutput/'+userName)):
        os.makedirs('/Users/nickpourazima/GitHub/he-sm/TestOutput/'+userName)
    currentPath = '/Users/nickpourazima/GitHub/he-sm/TestOutput/'+str(userName)
    filename = (userName+' '+t0+' '+time.asctime())
    completeName = os.path.join(currentPath, filename)

    rawData.to_csv(completeName+'.csv')

    # ========== PLOTTING ============
    plt.title('Time vs. Onsets')
    plt.plot(rawData['Sanitized Tap Onset'], 'g^')
    plt.plot(rawData['Tap Onset'], 'ro--')
    plt.plot(rawData['True Onset'], 'bs')
    fig1 = plt.gcf()
    fig1.savefig(completeName+'.png', bbox_inches='tight')
    plotly.tools.set_credentials_file(
        username='afaintillusion', api_key='yDV9rWN1OEY9kfS3VIqV')
    plotly_fig = tls.mpl_to_plotly(fig1)
    # plotly_fig['rawData'][0].update({'name':'Sanitized Tap Onset'})
    # plotly_fig['rawData'][1].update({'name':'Tap Onset'})
    # plotly_fig['rawData'][2].update({'name':'True Onset'})
    plotly_fig['layout'].update(yaxis=dict(title='Time', tickformat=".5f"))
    plotly_fig['layout']['showlegend'] = True
    plotly.offline.plot(plotly_fig, filename=(completeName+'.html'))

    # Re-initialize dataframe and dictionary for next test iteration
    rawData = pd.DataFrame()
    df = {
        'Test':             [],
        'User ID':          [],
        'True Onset':       [],
        'Tap Onset':        [],
        'Asynchrony':       []
    }

    # Check for end of test, if so then output summary data file
    if count == 16:
        all_files = glob.iglob(os.path.join(currentPath, "*.csv"))
        summary = pd.concat((pd.read_csv(f, skipinitialspace=True)
                             for f in all_files), ignore_index=True)
        summaryName = (userName+' Summary '+time.asctime())
        summaryPath = os.path.join(currentPath, summaryName)
        summary.to_csv(summaryPath+'.csv')
        summary.to_excel(summaryPath+'.xlsx')

def main():
    app = mainGUI()
    app.title("Audible & Haptic Test Suite (Author: Nick Pourazima - CMU 18')")
    app.mainloop()
    if(startFlag):
        global t0, userID, fadeoutTimer, allKeys
        counter = 1
        for c in userName:
            userID += int(ord(c))

        # =========== Practice Mode =============
        # practiceKeys = list(practiceTests.keys())
        # for item in practiceKeys:
        #     t0 = item
        #     t1 = Thread(target=playBeep, args=(fadeoutTimer,))
        #     t1.start()
        #     if(t0[2] == 'H'):
        #         t2 = Thread(target=haptic, args=practiceTests.get(item))
        #     elif(t0[2] == 'A'):
        #         t2 = Thread(target=playback, args=[practiceTests.get(item)])
        #     t3 = Thread(target=getTap)
        #     t1.join()
        #     t2.start()
        #     t3.start()
        #     t2.join()
        #     t3.join()
        #     dataAnalysis(counter)
        #     counter += 1
        # fadeoutTimer = 1000
        # t4 = Thread(target=playBeep, args=(fadeoutTimer,))
        # t5 = Thread(target=playBeep, args=(fadeoutTimer,))
        # t6 = Thread(target=playBeep, args=(fadeoutTimer,))
        # t4.start()
        # t4.join()
        # t5.start()
        # t5.join()
        # t6.start()
        # t6.join()

        # ========= ALL TESTS ==========
        # run through test cases (randomly)
        random.seed(10)
        hapticKeys = list(hapticTestCases.keys())
        shuffle(hapticKeys)
        audioKeys = list(audioTestCases.keys())
        shuffle(audioKeys)
        allKeys = hapticKeys + audioKeys
        shuffle(allKeys)
        print(allKeys)
        fadeoutTimer = 3000

        for key in hapticKeys:
            t0 = key
            t1 = Thread(target=playBeep, args=(fadeoutTimer,))
            t1.start()
            if(t0[0] == 'H'):
                t2 = Thread(target=haptic, args=hapticTestCases.get(key))
            elif(t0[0] == 'A'):
                t2 = Thread(target=playback, args=[audioTestCases.get(key)])
            t3 = Thread(target=getTap)
            t1.join()
            t2.start()
            t3.start()
            t2.join()
            t3.join()
            dataAnalysis(counter)
            counter += 1

        webbrowser.open('https://goo.gl/forms/LR5y4uy5fg86QcDW2',
                        new=2, autoraise=True)

if __name__ == "__main__":
    main()  