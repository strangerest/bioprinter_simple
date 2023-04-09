# coding=utf-8
# coding=utf-8

import numpy as np
import cv2
import serial
import time


serInk = serial.Serial(port='COM8', baudrate=115200, timeout=1)
serMove = 0 #= serial.Serial(port='/dev/tty.usbserial-A4030QY1', baudrate=115200, timeout=1)
img = cv2.imread(r"black420.jpg")

waitIdx = 0
waitNum = 1
stage = 1


btmp = img[:,:,0]
for i in range(len(btmp)): # this loop makes black and white bitmap from colored file
    for j in range(len(btmp[i])):
        if btmp[i][j] < 128:
           btmp[i][j] = 1
        else: 
           btmp[i][j] = 0


'''
картинка 420*420, 35 строк по 12 пикселей, одна строка 840 байт (2 байта на 12 пикс * 420)
'''
rowSize = 840
blockSize = 40
rows = 35 
rowH = 12

totalBytesWritten = 0
totalBytesRead = 0
while totalBytesWritten < rowSize * rows:
    request = "" 
    print "waiting for new request"
    while True:
        request = serInk.read(2)
        if request != "":
            break
    print "request =", ord(request[0]), ord(request[1]) # row num and block num
    
    row = ord(request[0])
    block = ord(request[1])
    
    #row12 = btmp[rowH * row : rowH * (row+1), :]
    row12 = btmp[rowH * row : rowH * (row+1), :]
    row12 = row12[::-1, :]
    bytesWritten = 0
    for i in range(block*blockSize / 2, (block+1) * blockSize / 2):  # 2 байта на строчку
        toPort = np.packbits(np.insert(row12[:,i],0,np.zeros(4).astype(np.uint8)))
        bytesWritten += serInk.write(toPort)
    
    totalBytesWritten += bytesWritten
    
    print "totalBytesWritten =", totalBytesWritten
    serInk.write(chr(0xff))  
    
    if (row == 0) and (block == 0):
        import subprocess

     
        
        subprocess.Popen("c:\python27\python \"clear_sync.py\"", stdout=None, shell=False)
       # time.sleep(2.0)
    #else:
    #    time.sleep(1.5)
  #  while serInk.inWaiting() < 4:
  #      print "w =",serInk.inWaiting()
  #      time.sleep(0.01)
  #  readBytes = serInk.read(4)
  #  for i, c in enumerate(readBytes):
   #     print "k =", i, "in =", bin(ord(c))
        
    
    if totalBytesWritten % rowSize == 0:    
    #verification
        while serInk.inWaiting() < 6:
            #print "w =",serInk.inWaiting()
            time.sleep(0.01)
        #print "w =",serInk.inWaiting()
        readBytes = serInk.read(6)
        for i, c in enumerate(readBytes):
            print "k =", i, "mil =", hex(ord(c))

        
        for j in range(0, rowSize / 2):
            rowBuf = serInk.read(2)
            toPrinter = serInk.read(2)
            time.sleep(0.0001)
            print "j =", j, "rb[0] =", bin(ord(rowBuf[0])), ", rb[1] =", bin(ord(rowBuf[1])), "prn[0] =",bin(ord(toPrinter[0])), "prn[1] =",bin(ord(toPrinter[1]))