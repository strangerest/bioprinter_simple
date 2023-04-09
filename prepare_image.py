import cv2
import os

import numpy
import numpy as np


def prepare_image(original_image: numpy.ndarray = cv2.imread('init.png'), result_black_image_name: str = "120.png",
                  result_down_width=120, result_down_height=120):
    # original_image = cv2.imread(original_image_name)

    resized_down = cv2.resize(original_image, (result_down_width, result_down_height), interpolation=cv2.INTER_LINEAR)

    # filters
    resized_down_gray_image = cv2.cvtColor(resized_down, cv2.COLOR_BGR2GRAY)
    (thresh, resized_down_black_image) = cv2.threshold(resized_down_gray_image, 127, 255, cv2.THRESH_BINARY)

    # Display images
    if __name__ == "__main__":
        cv2.imshow('Resized Down by defining height and width', resized_down_black_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    cv2.imwrite(result_black_image_name, resized_down_black_image)

def divide_on_chunks_simple(img: numpy.ndarray = cv2.imread('120.png', cv2.IMREAD_GRAYSCALE), chunk_row: int = 0, chunk_column: int = 0):
    string_weight = 8
    chunk = img[chunk_row * string_weight:(chunk_row*string_weight + string_weight), chunk_column:(chunk_column + 1)]
    chunk_string_tmp = ""  # we want to get 16 digits (2 bytes) and have only 12 duse so extra 4 zeros
    for i in chunk:
        # invert img
        if i == 255:
            chunk_string_tmp += '0'
        else:
            chunk_string_tmp += '1'
    packed_chunk = [int(chunk_string_tmp[::-1],2)]
    sending_data = bytearray(packed_chunk)
    return sending_data

def divide_on_chunks(img: numpy.ndarray = cv2.imread('120.png', cv2.IMREAD_GRAYSCALE), chunk_row: int = 0, chunk_column: int = 0):
    """
    TODO: if img height is not dividable by 12 last row should be added by zeros to 12
    :param original_image_name:
    :param chunk_row:
    :param chunk_column:
    :return: bytearray of 12 duse array
    """

    # img = cv2.imread(original_image_name, cv2.IMREAD_GRAYSCALE)
    string_weight = 10

    chunk = img[chunk_row * string_weight:(chunk_row*string_weight + string_weight), chunk_column:(chunk_column + 1)]
    # print(chunk)
    chunk_string_tmp = "000000"  # we want to get 16 digits (2 bytes) and have only 12 duse so extra 4 zeros
    for i in chunk:
        # invert img
        if i == 255:
            chunk_string_tmp += '0'
        else:
            chunk_string_tmp += '1'


    packed_chunk = [int(chunk_string_tmp[8:], 2), int(chunk_string_tmp[:8], 2)]
    if packed_chunk[0]=='\n':
        packed_chunk[0]==3
    if packed_chunk[1]=='\n':
        packed_chunk[1]==3
    sending_data = bytearray(packed_chunk)
    return sending_data

def divide_on_lines(img, chunk_row=0):
    line_array = bytearray()
    for j in range(int(img.shape[1])):
        line_array+=divide_on_chunks(img,chunk_row=chunk_row,chunk_column=j)
    return line_array

if __name__ == "__main__":
    img= cv2.imread('init_2.png')
    prepare_image(img)
    print(divide_on_lines(cv2.imread('120.png', cv2.IMREAD_GRAYSCALE)))
    # print(divide_on_chunks())

