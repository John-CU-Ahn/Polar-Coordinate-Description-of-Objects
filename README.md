# Polar-Coordinate-Description-of-Objects

## Description
Microscopy is a powerful tool in biology, allowing observations of biological phenomenon on the micron scale.
Under varying experimental conditions, the shapes of these objects over time need to be described in a quantitative way.
By defining a center point and sweeping out a survey radius line to describe the shape via degrees and radii, the shape of the cell can more easily be quantified.

## Implementation
The input data must be a tif file. This particular code is designed for tif stacks of images. An avi file showcasing the types of thresholded data ideal for this code is titled, "Thresholded p collini cell.avi."
![frame p coll](https://github.com/John-CU-Ahn/Polar-Coordinate-Description-of-Objects/assets/140204157/8269002c-0f90-4f26-aa37-0e472059ba77)

Type in the file directory leading to your input tif file into the "Polar coordinate description.py" script. The script will locate the center of the object, collect a series of line profiles containing pixel values sweeping out from the center point, and then calculate the radii associated with each degree (theta value). It will output a csv file of each radii at each degree over time.

The "Polar coordinate graphs.py" file will generate graphs of the radii from the csv file.

The "Make movie.py" file will generate a movie of the polar coordinate graphs in an mp4 file.

The "Polar coordinate graph movie.mp4" file showcases the polar coordinate graphs generated from the tif file used to create the "Thresholded p collini cell.avi" movie file.
![frame 138](https://github.com/John-CU-Ahn/Polar-Coordinate-Description-of-Objects/assets/140204157/f233d324-7ea3-4e9b-abac-b737cda613dc)
