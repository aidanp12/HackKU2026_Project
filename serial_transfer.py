"""
This is mostly just used to test the serial connection, and sets the eye back to "standard" position

"""

import serial


pico = serial.Serial("COM4", 115200)

line_x = f"1 = {int(float(95.1))}\n"
line_y = f"2 = {int(float(80.15))}\n"
print(line_x)
print(line_y)
pico.write(line_x.encode())
pico.write(line_y.encode())
