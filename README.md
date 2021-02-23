# 3Dslicer-scripts
Python scripts for processing many microCT scans, going through many volumes. These are to be run in the 3D slicer interpreter to minimize repetitive tasks in 3D Slicer. Based on nightly scripts repository and source code. Using these scripts greatly speeds up the process.

For each volume, give the ID code, resolution, and the file path for the folder where the scene file (#1) or volume (#2) is located.



## creating data for the firs time
> 1_set up volume and segmentation nodes.py  

OR 
opening previously saved scenes and creating objects with unique ID

> set resolution on previously saves scene

Then run the processes on the 3D data:

>staticfunctions.py - setup all the functions for implementing 3D processing  . Creates empty segments.
> 2_segentation effects.py - run segmentation effects. This includes 3d painting different structures of interest (columella, umbo, and endosseous cochlear duct tip) and using the 'smallest island' and custom automatich thresholding.
> 2_fiducials and markup to models.py - this gives consistent naming to  (if there was a previously save scene with the fcsv files, this is not needed)
> 3_fiducials and markup to models.py - models made based on the fcsv values - this limits the area to 

>4_markups to models.py - use the markup-to-models module to create model from fcsv points
## 2. importing data from a folder, setting resolutions
 
>volume.py - load the volume in the folder. Also read from a file the columella footplate or sets the plane to fit between 3 points along the columella. Exports a png file  
>models.py  -load the stl 3D files in the folder and adjust visibility and colour  
>fcsv.py  - load the fcsv files and make them all black and of the correct size. Also uses the markups to model module to connect the fcsv points as models (The color and thickness of the models can be adjusted)  
> screencapture.py -  creates a 3D rotation in the horizonal plane gif.

## 3. Miscellaneous scripts:
> change color of background display 3d.py  
> switch mouse int markup mode.py