import cv2
import numpy as np
img = cv2.imread("420.png", cv2.IMREAD_GRAYSCALE)
# print(img)
first_chank = img[12:24,1:2] # можем обрезать по пикселям
print(first_chank)
test_string = ""
for i in first_chank:
    if i==255:
        test_string+='1'
    else:
        test_string+='0'
print(test_string)
print(int(test_string,2))


import serial
import time
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
print(arduino.is_open)
sending_data =bytearray(int(test_string, 2))
# arduino.write(int(test_string, 2))
arduino.write(b'a')
data = arduino.readline()
print(data)
# print(first_chank)
# print()
# b = np.packbits(first_chank, axis=0)
# print(b[0,0]," " ,format(b[0,0], '#010b'))
# print(b[1,0]," ", format(b[1,0], '#010b'))
#
# print(b)
# # Importing Libraries
# import serial
# import time
# arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
# def write_read(x):
#     arduino.write(bytes(x, 'utf-8'))
#     time.sleep(0.05)
#     data = arduino.readline()
#     return data
# while True:
#     num = input("Enter a number: ") # Taking input from user
#     value = write_read(num)
#     print(value) # printing the value
