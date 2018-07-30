# he-sm
Haptic Enviro-Sensing Metronome Thesis Project by Nick Pourazima in partial fullfillment for the degree of Masters of Science in Music and Technology.

## Contents
### 1. Arduino Code
- [*fsr_silent_disc.ino*](https://github.com/afaintillusion/he-sm/blob/master/Arduino/fsr_silent_disc/fsr_silent_disc.ino)  is a modification of work by [Ben Schulz](https://www.ncbi.nlm.nih.gov/pubmed/26542971).
- [*main.ino*](https://github.com/afaintillusion/he-sm/blob/master/Arduino/main/main.ino) is designed to run on an AdaFruit Pro Trinket 16MHz.
- [*hesm.ino*](https://github.com/afaintillusion/he-sm/blob/master/Arduino/Rev%202%20Wireless/hesm.ino) is designed to run int he Particle environment, specifically with a Bluz board.
### 2. Audio Files
- 24 bit 44.1kHz wav files used during the auditory tests.
- If you'd like to use these for your own testing, please make sure to change the directory in [*testSuite.py*](https://github.com/afaintillusion/he-sm/blob/master/Python/testSuite.py)
### 3. Completed Tests
- This is where the raw data is stored from the test results run on subjects for this work.
### 4. Debug
- Some tools and sketches used to test system latency.
- txjitter binary compiled from Golang written by [Craig Hesling](https://github.com/linux4life798)
### 5. Max
- [Modified beat detection patch](https://github.com/afaintillusion/he-sm/blob/master/Max/Beat%20Detection%20Modified.maxpat) to trigger haptic device. Original work by [Adam Stark](https://github.com/adamstark)
### 6. python
- The Analysis folder contains the Onset Detection conducted on each audio file to collect onset times as well as the Jupyter Notebook utilized for data analysis.
- [combo.py](https://github.com/afaintillusion/he-sm/blob/master/Python/combo.py) is a small script that takes multiple completed test csv files and combines them into a single Pandas dataframe.
- [testSuite.py](https://github.com/afaintillusion/he-sm/blob/master/Python/testSuite.py) is the test suite for testing out both the audible and haptic test cases on users. For more details on methodology please see Appendix B in [np_thesis.pdf](https://github.com/afaintillusion/he-sm/blob/master/Thesis/np_thesis.pdf).
### 7. Thesis Paper
- **An evaluation of the interstitial beat across the modalities of touch and sound for the characterization of a meaningful haptic metronome**
	- [np_thesis.pdf](https://github.com/afaintillusion/he-sm/blob/master/Thesis/np_thesis.pdf)