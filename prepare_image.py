import cv2
import numpy


def prepare_image(original_image: numpy.ndarray = cv2.imread('init.png'),
                  result_black_image_name: str = "resized_bw.png",
                  result_down_width=160, result_down_height=160):
    """
    This function convert image from root folder to black and white
     and shrink it down to given size. Saves result image into root folder as well
    :param original_image: image in numpy array representation
    :param result_black_image_name: name of shrinked image in root folder
    :param result_down_width: width of result image in pixels
    :param result_down_height: height of result image in pixels
    :return: non
    """

    # resize image to given size
    resized_down = cv2.resize(original_image, (result_down_width, result_down_height), interpolation=cv2.INTER_LINEAR)

    # convert resized image to grayscale format
    resized_down_gray_image = cv2.cvtColor(resized_down, cv2.COLOR_BGR2GRAY)
    # convert grayscale image to black and white into resized_down_black_image variable
    (thresh, resized_down_black_image) = cv2.threshold(resized_down_gray_image, 127, 255, cv2.THRESH_BINARY)

    # debug mode, display final image
    if __name__ == "__main__":
        cv2.imshow('Resized Down by defining height and width', resized_down_black_image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    # save result image into root folder
    cv2.imwrite(result_black_image_name, resized_down_black_image)


def divide_on_chunks_simple(bw_img: numpy.ndarray = cv2.imread('resized_bw.png', cv2.IMREAD_GRAYSCALE),
                            chunk_row: int = 0,
                            chunk_column: int = 0, string_weight=8):
    """
    This function extruct slice of pixels of given image and convert it to bytearray
    it is used to get 8 pixels which will be printed by InkJet Bioprinter by one time
    (we simply take subarray from image array with size of 8*1, pixels 8 rows 1 column)
    :param string_weight: amount of used duse used at one time fo print (strongly recommended to left it as default)
    :param bw_img: black and wight image which will be converted to byte array and printed
    :param chunk_row: serial number of 8-pixel height row  y-coordinate(0 - top row, 1 - second row from the top of image)
    :param chunk_column: serial number of column x-coordinate
    :return: bytearray of pixels of given row ready to send to arduino
    """

    # subarray of image 8*1, pixels: 8 rows 1 column, 8 pixels in total
    chunk = bw_img[chunk_row * string_weight:(chunk_row * string_weight + string_weight),
            chunk_column:(chunk_column + 1)]

    # image is represented by 2-dimensional array, each pixel represented by integer value: 0-black or 255-white
    # we concatenate array into string and invert it (because 1 in serial protocol will activate duse and will give black pixel)
    # example array [0, 255, 0, 0, 255, 255, 255, 0] should be converted to '100' string
    chunk_string_tmp = ""
    for i in chunk:
        # invert prepared_img
        if i == 255:
            chunk_string_tmp += '0'
        else:
            chunk_string_tmp += '1'
    # convert string to binary integer value in LSF order because of serial protocol order
    packed_chunk = [int(chunk_string_tmp[::-1], 2)]
    # save and return result bytearray
    sending_data = bytearray(packed_chunk)
    return sending_data

# testing module
if __name__ == "__main__":
    img = cv2.imread('init_2.png')
    prepare_image(img)
