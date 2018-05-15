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


readIn = pd.read_csv('/Users/nickpourazima/GitHub/he-sm/Completed Tests/John/John Summary Sat May  5 20:33:37 2018.csv')
readIn = readIn.groupby('Test')
readIn['Missed Taps'] =readIn['Sanitized Tap Onset'].sum(axis=0)
readIn['Phase Correction Response'] = readIn['Sanitized Asynchrony'].shift(-1)-readIn['Sanitized Asynchrony']
readIn.to_csv('/Users/nickpourazima/GitHub/he-sm/Completed Tests/John/John  New Summary Sat May  5 20:33:37 2018.csv')