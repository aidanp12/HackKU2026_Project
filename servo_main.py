import time
from machine import Pin, PWM
from micropython_servo_pdm import ServoPDMRP2Async
import sys
import random


servo1_pwm = PWM(Pin(16))
servo2_pwm = PWM(Pin(17))
servo3_pwm = PWM(Pin(18))

# Set the parameters of the servo pulses, more details in the "Documentation" section
freq = 50
min_us = 500
max_us = 2500
max_angle = 180
min_angle = 0

# create a servo object
servo = [
            ServoPDMRP2Async(pwm=servo1_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle), 
            ServoPDMRP2Async(pwm=servo2_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle), 
            ServoPDMRP2Async(pwm=servo3_pwm, min_us=min_us, max_us=max_us, freq=freq, max_angle=max_angle, min_angle=min_angle)
]

last_blink = time.time()
eyes_closed = False
next_blink = 0
open_eyes = last_blink * 2 # make it so this doesnt ever cause the thing to get caught up in a boot loop

# read servo data from over serial port
while True:
    print("reading")
    line = sys.stdin.readline()
    if line: # proceed when serial input is detected
        current_time = time.time()
        
        # simple blinking mechanism, just adds some character to it
        if current_time >= last_blink + next_blink and not eyes_closed:
            servo[0].set_angle(125)
            open_eyes = current_time + 1
            eyes_closed = True
        elif current_time >= open_eyes and eyes_closed:
            servo[0].set_angle(80)
            eyes_closed = False
            next_blink = random.randint(10, 30)
            last_blink = current_time
        
        # process serial data, set servo angles accordingly
        try:
            data = line.strip().split(" = ")
            servo[int(data[0])].set_angle(int(data[1]))
        except:
            pass
