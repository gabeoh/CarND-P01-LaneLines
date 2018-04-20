# **Finding Lane Lines on the Road** 

---

## Objective
The object of this project is to:
* Make a pipeline that finds lane lines on the road

[//]: # (Image References)


[image1]: ./examples/grayscale.jpg "Grayscale"

[image01]: ./test_images_inter_steps/solidWhiteCurve_01_gray.jpg
[image02]: ./test_images_inter_steps/solidWhiteCurve_02_blur.jpg
[image03]: ./test_images_inter_steps/solidWhiteCurve_03_edge.jpg
[image04]: ./test_images_inter_steps/solidWhiteCurve_04_regioned.jpg
[image05]: ./test_images_inter_steps/solidWhiteCurve_05_lines.jpg
[image06]: ./test_images_inter_steps/solidWhiteCurve_06_super.jpg
[image05_agg]: ./test_images_inter_steps/solidWhiteCurve_05_lines_agg.jpg
[image06_agg]: ./test_images_inter_steps/solidWhiteCurve_06_super_agg.jpg

---

## Reflection

### 1. Pipeline Description

#### Pipeline Steps
My pipeline consisted of 6 steps. 

**Step 1 - Grayscale**  
Convert the image into a single-channel grayscale image.
![Grayscale][image01]

**Step 2 - Gaussian Blur**  
Blur the grayscale image using Gaussian Blur algorithm in order to reduce
edge detection error.
![Blur][image02]

**Step 3 - Canny Edge Detection**  
Detect edges using Canny Edge Detection algorithm.
![Canny Edges][image03]

**Step 4 - Region of Interest**  
Find region of interest and mask out areas outside of the region.
![Region][image04]

**Step 5 - Hough Transform**  
From the edge image, detect line segments using Hough Transform.
![Hough Lines][image05]

**Step 6 - Superimposition**  
Finally, superimpose the detected line segments onto the original image.
![Lines Superimposed][image06]


#### Draw Aggregated Lines
In order to aggregate detected line segments into a single line for left
and right lanes respectively, following steps are added to ```draw_lines()```
function. 

**1. Lane Determination**  
- First, find two end points for each line segment detected from Hough
Transform
- Find the slope of the line segment
- Determine whether the line segment belongs to left or right lanes
  - Two criteria are used for the side determination; *slope* and *x-coordinate*
  - For a line segment to belong to the left lane, the slope must be
    negative and x-coordinates of both end points should be smaller than
    midpoint of the image
  - For the right lane, similarly, positive slope and x-coordinate bigger
    than the midpoint
- Tightened slope ranges to filter out inconsistent segments
  - While reviewing annotated video outputs, I noticed the lane lines sometimes
    go out of the expected region
  - The problem was mitigated by tightening slope ranges and discard outliers
  - By iterative trial and reviewing discarded line segments, the slope ranges
    are determined
    - Left lane slope range: (-0.9, -0.5)
    - Right lane slope range: (0.4, 0.8) 

**2. Find Line Equations**
- By using ```np.polyfit()``` function on the line endpoints found in the
  above step, the linear polynomial equations for fitting lines are determined

**3. Determine Line End Points**
- The end points for each aggregated line are determined by computing
  x-coordinates for _pre-determined y-coordinates*_ using the fitting polynomials
- _pre-determined y-coordinates*_
  - ```y_bottom```: y-coordinate of pixels on the bottom of the image
    (```img.shape[0] - 1```)
  - ```y_top```: minimum, or top, y-coordinate all line segments collected

**Aggreated Lane Lines**  
![Hough Lines][image05_agg]

**Aggreated Lane Lines Over The Original Image**  
![Lines Superimposed][image06_agg]


### 2. Limitations

One limitation of the pipeline is that it assumes ideal environments.  There
are several factors that could cause the pipeline to misbehave.

**1. Displacement of lane lines**  

The pipeline assumes that the position of the lane lines is relatively fixed
in the image.  However, the position relative to the fixed camera location
could vary.

Potential causes for the displacement include vehicle movements and roadway
curvature changes.

**2. Interruption by external objects**

In reality, the driver's view gets constantly interfered by external objects
such as other vehicles, humans, and animals.  These interruptions can cause
the pipeline to misidentify the lane lines.

**3. Variations in lighting and road shades**

Variations in lighting, shadow, and road colors can cause the edges of lane
lines less distinct.  This can result in both false positive and false negative
edge detection errors.


### 3. Possible Improvements

I can think of several ways to improve the pipeline; in terms of both accuracy
and performance.

**1. Cross-Image Analysis**

For the video analysis, the current pipeline treats each frame independently.
The frames in time proximity, however, tend to have some resemblance.  By
referencing lines detected previous frames, the pipeline can reduce error and
it can be more robust against view disruptions.

**2. Early Pruning**

As far as we are only concerned with detecting lane lines from the image, only
about a quarter of the image contains meaningful information.

In the later step, the pipeline filter out the portions of processed images that
are outside of the region of interest.  By pruning earlier, the performance of
grayscaling and edge detection can be improved. 

**3. Parameter Determination**

Transformations used in the pipeline, such as grayscale, Gaussian blur, Canny
edge detection, and Hough transformation, are all parameterizable.  It is
crucial to select appropriate parameter values for a successful lane line
detection.

The only way for us to evaluate these parameter selections is to manually
review resulting images for each parameter variation.  This limits the number
of different parameter combinations we can test, and the quality of the results
is vulnerable to human perception error.

It may be very difficult to completely eliminate the need for human guidance
when determining such parameters.  However, if we have means of quantifying
result qualities, we can perform a large number of iterations with varying
parameter values.  This way, we can find a more accurate solution in a much
more efficient manner. 
