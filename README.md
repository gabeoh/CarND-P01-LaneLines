# CarND-P01-LaneLines
CarND-P01-LaneLines is the first project of Udacity Self-Driving Car program.
This project implements a pipeline to detect lane lines from images and video
streams.

The output of the pipeline is images and videos annotated with detected lane
lines. 

## File Structure
- **P1.ipynb** - Project IPython notebook
- **P1_writeup.md** - Project write-up report
- **py-src** - Directory containing raw python scripts used in the project
- **test_images** - Provided input test images 
- **test_videos** - Provided input test videos
- **test_images_output** - test images annotated with lane lines
  - **raw_line** - images annotated with raw lines found through Hough transform
- **test_videos_output** - test videos annotated with lane lines
  - **raw_line** - videos annotated with raw lines found through Hough transform
- **test_images_inter_steps** - intermediate images at each transformation step

## Getting Started
### [Download ZIP](https://github.com/gabeoh/CarND-P01-LaneLines/archive/master.zip) or Git Clone
```
git clone https://github.com/gabeoh/CarND-P01-LaneLines.git
```

### Setup environment

You can set up the environment following
[CarND-Term1-Starter-Kit - Miniconda](https://github.com/udacity/CarND-Term1-Starter-Kit/blob/master/doc/configure_via_anaconda.md).
This will install following packages required to run this application.

- Miniconda
- Python
- Jupyter Notebook

### Usage

There are two ways of running this project.

#### Jupyter Notebook
Open `P1.ipynb`, the project IPython notebook, using Jupyter Notebook.
```
jupyter notebook P1.ipynb
```

#### Running Python scripts
You can also run Python scripts directly from command line.
```
$ cd py-src

# Run lane line annotation on test images
$ python p01_lanelines_01_image.py

# Run lane line annotation on test videos
$ python p01_lanelines_02_video.py
```

## License
Licensed under [MIT](https://github.com/gabeoh/CarND-P01-LaneLines/blob/master/LICENSE)
License.