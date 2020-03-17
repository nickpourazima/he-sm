# he-sm
The **Haptic Enviro-Sensing Metronome** (he-sm) is a project completed by Nick Pourazima in May 2018 in partial fulfillment of the degree of Masters of Science in Music and Technology.
- [he-sm](#he-sm)
	- [Abstract](#abstract)
	- [Thesis](#thesis)
	- [Arduino Code](#arduino-code)
	- [Audio Files](#audio-files)
	- [Completed Tests](#completed-tests)
	- [Debug](#debug)
	- [Max](#max)
	- [python](#python)
	- [Misc. media](#misc-media)
	- [Haptic Operation Instruction Manual](#haptic-operation-instruction-manual)
## Abstract
`
The following work is an expansion of sensorimotor synchronization re- search. It provides an evaluation of the intervening space between the beat as it applies to the modalities of touch and sound. The crux of the experiment is a tap test comparison of continuous and discrete impulses over static (isochronous) and dynamic (non-isochronous) pulse intervals.
Time-based response metrics of a wearable haptic are contrasted to a suite of audible tests. Though vast evidence promotes an auditory advantage in guiding rhythmic accuracy and low asynchrony, this work hypothesizes a haptic benefit when the dynamically changing beat is occupied with a continuous wave across the modality of touch.
The analysis of 16 subjects (8 professionals, 8 amateur and non-musicians) resulted in favorable results for the haptic device during the dynamic test cases as contrasted to the auditory test results. Though the auditory modality yielded the best results for the isochronous test cases, the haptic device won out for non-isochronous or dynamically changing beats with a much cleaner standard deviation. This implies a greater synchronization ability with the haptic device and strongly supports the hypothesis of this work.
The overarching goal is to inform validity and design of a haptic wear- able which seeks to supplant the traditional metronome experience in providing a meaningful gestural system. The work holds value towards future entrainment studies in expressive musical performance but can be expanded to include extra-musical applications such as stroke and Parkinson’s patient gait rehabilitation practice.
`


## Thesis
- [**An evaluation of the interstitial beat across the modalities of touch and sound for the characterization of a meaningful haptic metronome**](https://github.com/afaintillusion/he-sm/blob/master/Thesis/np_thesis.pdf)
## Arduino Code
- [*fsr_silent_disc.ino*](https://github.com/afaintillusion/he-sm/blob/master/Arduino/fsr_silent_disc/fsr_silent_disc.ino)  is a modification of work by [Ben Schulz](https://www.ncbi.nlm.nih.gov/pubmed/26542971).
- [*main.ino*](https://github.com/afaintillusion/he-sm/blob/master/Arduino/main/main.ino) is designed to run on an AdaFruit Pro Trinket 16MHz.
- [*hesm.ino*](https://github.com/afaintillusion/he-sm/blob/master/Arduino/Rev%202%20Wireless/hesm.ino) is designed to run in the Particle environment, specifically with a Bluz board.
## Audio Files
- 24 bit 44.1kHz wav files used during the auditory tests.
- If you'd like to use these for your own testing, please make sure to change the directory in [*testSuite.py*](https://github.com/afaintillusion/he-sm/blob/master/Python/testSuite.py)
## Completed Tests
- This is where the raw data is stored from the test results run on subjects for this work.
## Debug
- Some tools and sketches used to test system latency.
- txjitter binary compiled from Golang written by [Craig Hesling](https://github.com/linux4life798)
## Max
- [Modified beat detection patch](https://github.com/afaintillusion/he-sm/blob/master/Max/Beat%20Detection%20Modified.maxpat) to trigger haptic device. Original work by [Adam Stark](https://github.com/adamstark)
## python
- The Analysis folder contains the Onset Detection conducted on each audio file to collect onset times as well as the Jupyter Notebook utilized for data analysis.
- [combo.py](https://github.com/afaintillusion/he-sm/blob/master/Python/combo.py) is a small script that takes multiple completed test csv files and combines them into a single Pandas dataframe.
- [testSuite.py](https://github.com/afaintillusion/he-sm/blob/master/Python/testSuite.py) is the test suite for testing out both the audible and haptic test cases on users. For more details on methodology please see Appendix B of [np_thesis.pdf](https://github.com/afaintillusion/he-sm/blob/master/Thesis/np_thesis.pdf).
## Misc. media
- [Development/design iteration pictures and videos as well as user testing images](https://photos.app.goo.gl/LSvh9r4QoSpXpAqK6)
## [Haptic Operation Instruction Manual](https://docs.google.com/document/d/1vB0zk6RceEyYD20hWCYP4Afg4Ua1DJR6iZ438ZEw02U/edit?usp=sharing)
