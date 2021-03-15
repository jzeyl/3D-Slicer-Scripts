# 3DSlicer automation scripts
This repository includes Python scripts for processing many microCT scans, going through many volumes. These are to be run in the 3D slicer interpreter  3D Slicer 4.10.1. Using these scripts greatly speeds up repetitive tasks that would require button-clicking the GUI while working through many files.

Scripts were are based on the nightly scripts repository_____
 and source code_________ 

For each volume, give the ID code, resolution, and the file path for the folder where the scene file (#1) or volume (#2) is located.

## 1. Creating data for the first time
Opening up new filess and creating objects with unique ID:

>* *1_set up volume and segmentation nodes.py*  

>* set up segmentations.py
![alt text](addsegnames.png)
OR, if opening previously saved scenes file 

>* *set resolution on previously saves scene.py*



>* *2_fiducials and markup to models.py* - this gives consistent naming to  (if there was a previously save scene with the fcsv files, this is not needed)
![alt text](markupscreated.png)
>* *3_fiducials and markup to models.py* - models made based on the fcsv values - this limits the area to 

Then run processes on the volume:

>* *staticfunctions.py* - setup all the functions for implementing 3D processing. Creates empty segments with unique specimen ID.  



>* *4_markups to models.py* - use the markup-to-models module to create model from fcsv points  . This creates a 3D region of interest for further segmentation

![alt text](markupstomodel.png)
-it then converts the model to a segmentation, which can be
![alt text](tosegmentations.png)
![alt text](segmentedinsidemodel.png)
## 2. Importing data from a folder, setting resolutions
 
These set of scripts are for loading a volume, several fcsv files and models based all located in the same folder. This is for making nice figures without having to load all the segmentations

Loading volume, setting resolution, and formatting the color, opacity of the models and fcsv points
>* *volume.py* -   
    * load the volume in the folder.   
    * Also reads from a file the columella footplate or sets the plane to fit between 3 points along the columella.  
    * Exports a png file  
    * moves the plane through 3 points
>* *models.py*  
    * load the stl 3D files in the folder and adjust opacity, visibility and colour  
>* *fcsv.py*  
    * load the fcsv files and make them all black and of the correct size.  
    * Also uses the markups to model module to connect the fcsv points as models (The color and thickness of the models can be adjusted)  

Created gif of rotating 3D models and points:
>* *screencapture.py* -  creates a 3D rotation in the horizonal plane gif.

## 3. Miscellaneous scripts:
>* *change color of background display 3d.py*  
>* *switch mouse int markup mode.py*


## 4. Static functions descriptionss
colthresh() - run threshold on selected segment.
-sets the maximum entropy algorithm as minimum-
![alt text](colthresh.png)
colkeeplargestisland() runs the largest island on the 
thresholded columella

writecolvoltofile() - writes the columella volume to a file

ecd() - sets the threshold on a segmented end of endosseous cochlear
duct (uses all values less than maxent) (highlights soft tissues)
-also runs keep largest island

umbo_ME_ISOtest() runs a threshold test, but doesn't apply it. If the threshold
doesn't work, the user can modify manually using the GUI

umbo_MES_ISO_apply() = runs threshold test and applies it

computedEC_TMmarkup() - joins together points from multiple fcsv
objects, in order to later be used in markup-to-model which will cover
an area encompassing points of intereset

ETmarkuptomodel() - runs the markup to model to create a region of interest
using the fcsv input

opennewvolume(): given the path for a folder, it opens the first 
volume , or file containing "tif", and also sets the ID and spacing

fcsv_template(): set up fcsv names

fcsv_display_smaller()


