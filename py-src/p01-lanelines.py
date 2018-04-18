#importing some useful packages
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2
import os

from tf_helpers import tf_helpers as tf

def detect_lane_lines(image):
    # printing out some stats and plotting
    print('This image is:', type(image), 'with dimensions:', image.shape)
    ysize = image.shape[0]
    xsize = image.shape[1]

    # First, convert the image into gray scale
    image_gray = tf.grayscale(image)
    # plt.imshow(image_gray, cmap='gray')

    # Reduce error detection noise by blurring image
    # Gaussian Blur: kernel_size = 5
    kernel_size = 5
    image_blurred = tf.gaussian_blur(image_gray, kernel_size)
    # plt.imshow(image_blurred, cmap='gray')

    # Detect edges
    # Canny Edge Detection: low_threshold = 50, high_threshold = 150
    low_threshold = 50
    high_threshold = 150
    image_edge = tf.canny(image_blurred, low_threshold, high_threshold)
    # plt.imshow(image_edge, cmap='gray')

    # Find region of interest
    vertices = np.array([[[120, ysize - 1], [420, 330], [550, 330], [880, ysize - 1]]],
                        dtype=np.int32)
    image_regioned = tf.region_of_interest(image_edge, vertices)
    # plt.imshow(image_regioned, cmap='gray')

    # Detect lines using Hough transform
    rho_accu = 1
    theta_accu = np.pi / 180
    hough_threshold = 20
    min_line_length = 40
    max_line_gap = 15
    lines = tf.hough_lines(image_regioned, rho_accu, theta_accu, hough_threshold,
                           min_line_length, max_line_gap)
    #plt.imshow(lines)


    # Super impose lines on original image
    image_super = tf.weighted_img(lines, image)
    #plt.imshow(image_super)
    return image_super

# Process images under '../test_images/'
image_src_dir = '../test_images/'
image_dst_dir = '../test_images_output/'
images = os.listdir(image_src_dir)
for image_name in images:
    print('Reading "%s"...' % image_name)
    image_path = image_src_dir + image_name

    # Read the image and find lane lines from it
    image = mpimg.imread(image_path)
    image_line_detected = detect_lane_lines(image)

    # Write line detected images to files
    image_out_path = image_dst_dir + image_name
    mpimg.imsave(image_out_path, image_line_detected)
    print('The output image is written to: %s\n' % image_out_path)

