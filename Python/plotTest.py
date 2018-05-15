from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'osx')
# %matplotlib osx
import numpy, scipy, matplotlib.pyplot as plt, IPython.display as ipd
import librosa, librosa.display
import stanford_mir; stanford_mir.init()


x, sr = librosa.load('AudioFiles/click_44.1_16bit_20sec_45bpm.wav')
print(x.shape, sr)

plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr)

onset_frames = librosa.onset.onset_detect(x, sr=sr)
print(onset_frames) # frame numbers of estimated onsets

onset_times = librosa.frames_to_time(onset_frames)
print(onset_times)