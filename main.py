import time
from prepare_image import divide_on_chunks,divide_on_chunks_simple, prepare_image
import cv2
import serial

# ---------- user zone begin ----------

# simple instruction: put your img of any resolution in project folder and name it "init.png"
# plug in arduino and check it's serial port, should be smth like COM7 Replace it with real name
input_img_name = "init_2.png"
serial_port = 'COM7'

# user zone end

# change COM7 to real port of arduino. autodetection in process
arduino = serial.Serial(port=serial_port, baudrate=115200, timeout=.1)

init_img = cv2.imread(input_img_name)
prepare_image(init_img, "120.png", result_down_width=320, result_down_height=320)

img = cv2.imread("120.png",cv2.IMREAD_GRAYSCALE)

# waiting for arduino to restart
time.sleep(2)
string_weight = 8
buffer = bytearray([])

for i in range(int(img.shape[0]/string_weight)):

    for j in range(int(img.shape[1])):
        buffer += divide_on_chunks_simple(img, chunk_row=int(i), chunk_column=int(j))

    print(buffer)
    print(len(buffer))
    print('pexels ')
    print(str(int(img.shape[1])))

    arduino.write(str.encode(str(int(img.shape[1]))))
    arduino.write(str.encode(' '))
    arduino.write(buffer)

    print('bytes in buffer ')
    print(arduino.inWaiting())
    buffer = bytearray([])

    while not arduino.inWaiting():
        time.sleep(0.01)
    print(arduino.read())


