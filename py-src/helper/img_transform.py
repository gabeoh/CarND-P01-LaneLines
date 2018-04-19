import numpy as np
import matplotlib.pyplot as plt
import cv2
import math


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)


def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)


def region_of_interest(img, vertices):
    """
    Applies an image mask.

    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    # defining a blank mask to start with
    mask = np.zeros_like(img)

    # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def find_aggregated_line(lines_x, lines_y, y_bottom, y_top):
    """
    Find two end-points (bottom and top) of aggregated line for given line collection.
    The endpoints are determined by given y coordinate range
    :param lines_x: x coordinates of lines
    :param lines_y: y coordinates of lines
    :param y_bottom: bottom end y coordinate of aggregated line segment
    :param y_top: top end y coordinate of aggregated line segment
    :return: (x, y) coordinates of two end-points of aggregated line segment
    """

    # First, make sure that lines_x and lines_y are non-empty same size arrays
    assert(len(lines_x) > 0 and len(lines_x) == len(lines_y))

    # Compute straight lines that fit line endpoints for left and right line segments
    line_fit = np.polyfit(lines_x, lines_y, 1)

    # Find start and end points for aggregated lines
    x_bottom = int(round((y_bottom - line_fit[1]) / line_fit[0]))
    x_top = int(round((y_top - line_fit[1]) / line_fit[0]))

    return [(x_bottom, y_bottom), (x_top, y_top)]


def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """

    # Identify line end points of each line (separate into left and right lines)
    lines_left_x = []
    lines_left_y = []
    lines_right_x = []
    lines_right_y = []
    xsize = img.shape[1]
    x_middle = int(round(xsize / 2))
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2 - y1) / (x2 - x1)
            if (slope > -0.9 and slope < -0.5) and (x1 < x_middle and x2 < x_middle):
                lines_left_x.extend([x1, x2])
                lines_left_y.extend([y1, y2])
            elif (slope > 0.4 and slope < 0.8) and (x1 > x_middle and x2 > x_middle):
                lines_right_x.extend([x1, x2])
                lines_right_y.extend([y1, y2])
            else:
                #print('Ignore outlier lines - slope: %f, (%d, %d), (%d, %d)' % (slope, x1, y1, x2, y2))
                pass

    # Determine Y range for aggregated lines
    ysize = img.shape[0]
    y_bottom, y_top = ysize - 1, min(lines_left_y + lines_right_y)

    # Find and draw aggregated lines for left and right line collections respectively
    if (len(lines_left_x) > 0):
        point_bottom, point_top = find_aggregated_line(lines_left_x, lines_left_y, y_bottom, y_top)
        cv2.line(img, point_bottom, point_top, color, thickness)
    if (len(lines_right_x) > 0):
        point_bottom, point_top = find_aggregated_line(lines_right_x, lines_right_y, y_bottom, y_top)
        cv2.line(img, point_bottom, point_top, color, thickness)

def draw_lines_old(img, lines, color=[255, 0, 0], thickness=2):
    """
    The original draw_lines function provided in the project
    """
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img


# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.

    `initial_img` should be the image before any processing.

    The result image is computed as follows:

    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)
