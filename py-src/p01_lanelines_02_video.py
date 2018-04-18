# Import everything needed to edit/save/watch video clips
from moviepy.editor import VideoFileClip
from IPython.display import HTML
import os

from helper import lane_detect as ld

# Process videos under '../test_videos/'
video_src_dir = '../test_videos/'
video_dst_dir = '../test_videos_output/'
videos = ['solidWhiteRight.mp4', 'solidYellowLeft.mp4']
for video_name in videos:
    print('Reading "%s"...' % video_name)
    video_path = video_src_dir + video_name

    video_out_path = video_dst_dir + video_name
    ## To speed up the testing process you may want to try your pipeline on a shorter subclip of the video
    ## To do so add .subclip(start_second,end_second) to the end of the line below
    ## Where start_second and end_second are integer values representing the start and end of the subclip
    ## You may also uncomment the following line for a subclip of the first 5 seconds
    ##clip1 = VideoFileClip("test_videos/solidWhiteRight.mp4").subclip(0,5)
    clip = VideoFileClip(video_path)
    clip_processed = clip.fl_image(ld.process_image)  # NOTE: this function expects color images!!

    # Write line detected videos to files
    clip_processed.write_videofile(video_out_path, audio=False)

