import time
from prepare_image import divide_on_chunks_simple, prepare_image
import cv2
import serial

# ---------- user zone begin ----------

# simple instruction: put your prepared_img of any resolution in project folder and name it "init.png"
# plug in arduino and check it's serial port, should be COM+number (for windows)
input_img_name = "init.png"
serial_port = 'COM7'

# user zone end

# set communication with arduino
arduino = serial.Serial(port=serial_port, baudrate=115200, timeout=.1)
# open image to convert to black and wight low resolution image ready to print
init_img = cv2.imread(input_img_name)
prepare_image(init_img, "resized_bw.png", result_down_width=160, result_down_height=160)

# load prepared black and wight image
prepared_img = cv2.imread("resized_bw.png", cv2.IMREAD_GRAYSCALE)

# waiting for arduino to set serial connection (arduino restarts each time it sets serial communication)
time.sleep(2)

# print by 8 pixels at a time to simplify data transfer (8 pixels = 1 byte)
string_weight = 8

# output buffer in bytes send to arduino
buffer = bytearray([])

# image is two-dimensional array of ones and zeros (1 or 255 in our case)
# we take a row of 8 pixels and store it in buffer. Then send the buffer to arduino,
# take another row of 8 pixels and repeat till the end of image

for i in range(int(prepared_img.shape[0] / string_weight)): # prepared_img.shape[0] is a height of image in pixels

    # concatenate row of 8 pixels in buffer
    for j in range(int(prepared_img.shape[1])):
        buffer += divide_on_chunks_simple(prepared_img, chunk_row=int(i), chunk_column=int(j))

    # debug information
    print(buffer)
    print(len(buffer))
    print('pexels ')
    print(str(int(prepared_img.shape[1])))

    # serial communication protocol is in following format:
    # 1) send amount of following bytes
    # 2) send blank spase ' '
    # 3) send all bytes
    # 4) then wait for arduino response
    arduino.write(str.encode(str(int(prepared_img.shape[1]))))
    arduino.write(str.encode(' '))
    arduino.write(buffer)

    # debug information
    print('bytes in buffer ')
    print(arduino.inWaiting())

    # cleean buffer variable
    buffer = bytearray([])

    # wait for arduino response
    while not arduino.inWaiting():
        time.sleep(0.03)
    # debug information
    print(arduino.read())


