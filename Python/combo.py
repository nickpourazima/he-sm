import os
import glob
import pandas as pd

currentPath = '/Users/nickpourazima/GitHub/he-sm/TestOutput/Temp/Temp2'
all_files = glob.iglob(os.path.join(currentPath, "*.csv"))
summary = pd.concat((pd.read_csv(f, skipinitialspace=True) for f in all_files), ignore_index=True)
summaryName = ('Combo_Final')
summaryPath = os.path.join(currentPath, summaryName)
summary.to_csv(summaryPath+'.csv')
# summary.to_excel(summaryPath+'.xlsx')
