# HackKU2026\_Project

Animatronic Eye



### Overview

This project is a simple hardware-focused system, combining camera feedback with servo control and microcontroller processing.

The 3D prints I used were by Morgan Manly on makerworld (https://makerworld.com/en/models/1217249-animatronic-eye-v4#profileId-1910851).



#### Contents

Repository contains 3 files:


* vision.py
* serial\_trasnfer.py
* servo\_main.py



Serial transfer isn't a necessary file, it's mostly just there for recentering and testing serial connection.



#### Vision.py



This is where most the magic happens. Intended to be run on a system with more processing power than a microcontroller, this file handles camera input, object detection, and serial transmission. The necessary libraries are:

* deep\_sort\_realtime
* ultralytics
* opencv-python
* serial

From there it's mostly plug in play. May need to change the cap variable to a different video device if you only have one connected. Similarly, the pico COM port needs to match your connected microcontroller.



#### Servo\_main.py

Ran on the pico microcontroller. Need the micropython\_servo\_pdm library, available on GitHub or via Thonny's library search. The code processes an input over serial connection, then uses basic string manipulation to derive servo instructions. 



##### Serial\_transfer.py

Was used to test serial transfer. Kept it around to recenter the eye whenever something breaks.

