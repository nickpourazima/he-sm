# Patch Info
This Max patch utilizes the beat tracking algorithm and code from Adam Stark to trigger over serial comm to a connected MCU (Arduino/Pro Trinket).

 -  Prerequisites: 
	 - [BTrack](https://github.com/adamstark/BTrack) Max External by Adam Stark
	 - Make sure you're running in 32-bit mode
	 - Serial at 115200 baud by default (can be modified)
 - Note:
	 - sfplay~ will play met click based on audio input
	 - for less variability connect mean to atoi instead of the directly route bpm number