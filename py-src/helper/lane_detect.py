import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

import img_transform as itf

def process_image(image):
    '''
    Detect lane lines from image using various image transformations

    :param image:
    :return: original image superimposed with lane lines
    '''

    # printing out some stats and plotting
    #print('This image is:', type(image), 'with dimensions:', image.shape)
    ysize = image.shape[0]
    xsize = image.shape[1]
    # image_dst_dir = '../test_images_inter_steps/'
    # image_name_base = 'solidWhiteCurve'

    # First, convert the image into gray scale
    image_gray = itf.grayscale(image)
    # plt.imshow(image_gray, cmap='gray')
    # mpimg.imsave(image_dst_dir + image_name_base + '_01_gray.jpg', image_gray, cmap='gray')


    # Reduce edge detection noise by blurring image
    # Gaussian Blur: kernel_size = 5
    kernel_size = 5
    image_blurred = itf.gaussian_blur(image_gray, kernel_size)
    # plt.imshow(image_blurred, cmap='gray')
    # mpimg.imsave(image_dst_dir + image_name_base + '_02_blur.jpg', image_blurred, cmap='gray')


    # Detect edges
    # Canny Edge Detection: low_threshold = 50, high_threshold = 150
    low_threshold = 50
    high_threshold = 150
    image_edge = itf.canny(image_blurred, low_threshold, high_threshold)
    # plt.imshow(image_edge, cmap='gray')
    # mpimg.imsave(image_dst_dir + image_name_base + '_03_edge.jpg', image_edge, cmap='gray')


    # Find region of interest
    vertices = np.array([[[100, ysize - 1], [420, 330], [550, 330], [900, ysize - 1]]],
                        dtype=np.int32)
    image_regioned = itf.region_of_interest(image_edge, vertices)
    # plt.imshow(image_regioned, cmap='gray')
    # mpimg.imsave(image_dst_dir + image_name_base + '_04_regioned.jpg', image_regioned, cmap='gray')


    # Detect lines using Hough transform
    rho_accu = 1
    theta_accu = np.pi / 180
    hough_threshold = 20
    min_line_length = 30
    max_line_gap = 20
    lines = itf.hough_lines(image_regioned, rho_accu, theta_accu, hough_threshold,
                            min_line_length, max_line_gap)
    #plt.imshow(lines)
    # mpimg.imsave(image_dst_dir + image_name_base + '_05_lines_agg.jpg', lines)


    # Super impose lines on original image
    image_super = itf.weighted_img(lines, image)
    #plt.imshow(image_super)
    # mpimg.imsave(image_dst_dir + image_name_base + '_06_super_agg.jpg', image_super)
    return image_super
