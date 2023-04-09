# # Importing Libraries
# import serial
# import time
# import cv2
# import numpy as np
#
# img = cv2.imread("420.png", cv2.IMREAD_GRAYSCALE)
# # print(img)
# first_chank = img[12:24,1:2] # можем обрезать по пикселям
# print(first_chank)
# test_string = "0000"
# for i in first_chank:
#     if i==255:
#         test_string+='1'
#     else:
#         test_string+='0'
# test_string='0000000011111111'
# print(bin(int(test_string[8:],2)))
# print(bin(int(test_string[:8],2)))
# prime_numbers = [int(test_string[8:],2),int(test_string[:8],2)]
#
# prime_numbers_2 = np.packbits(first_chank,axis=0)
# print(prime_numbers_2)
# sending_data =bytearray(prime_numbers_2)
# print(sending_data)
# arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
#
# time.sleep(2.5)
#
# arduino.write(sending_data)
# # arduino.write(sending_data)
#
# print('debug')
# print(arduino.readline()) # printing the value
# print(arduino.readline()) # printing the value
# print(arduino.readline()) # printing the value


array1 =[4, 5, 6]
array2 =[7,8,9]
ar1 =bytearray(array1)
ar2=bytearray(array2)
ar3=ar1+ar2
print(ar3)