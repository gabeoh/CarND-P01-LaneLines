#importing some useful packages
import matplotlib.image as mpimg
import os

from helper import lane_detect as ld

# Process images under '../test_images/'
image_src_dir = '../test_images/'
image_dst_dir = '../test_images_output/'
images = os.listdir(image_src_dir)
for image_name in images:
    print('Reading "%s"...' % image_name)
    image_path = image_src_dir + image_name

    # Read the image and find lane lines from it
    image = mpimg.imread(image_path)
    image_line_detected = ld.process_image(image)

    # Write line detected images to files
    image_out_path = image_dst_dir + image_name
    mpimg.imsave(image_out_path, image_line_detected)
    print('The output image is written to: %s\n' % image_out_path)

