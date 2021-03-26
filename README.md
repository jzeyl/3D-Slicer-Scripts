# 3DSlicer Automation Python Scripts
This repository includes Python scripts for running commands for 3D Slicer 4.10.1 using the built-in interpreter. Using these scripts greatly speeds up repetitive tasks for loading and processin volumes that would require button-clicking the GUI while working through many files. It automatates the creation of segmentation nodes, markup nodes with unique identifies for each specimen. Then there are functions which run specific effects (e.g., segmentation, modifying markups) using those nodes.
Scripts were based on the nightly scripts repository____
 and looking at 3D Slicer source code_________ 



## 1. Creating data for the first time
For each volume, give the ID code, resolution, and the file path for the folder where the volume located. 

>* *1_set up volume and segmentation nodes.py*  

Next, repeatable segmentation nodes can be created with the unique IDs in the naming:
>* set up segmentations.py
![alt text](addsegnames.png)
OR, if opening previously saved scenes file 

Next there is a need to populate markup nodes, also named according to unique IDs:

>* fcsv_template(): set up fcsv names
![alt text](markupscreated.png)  

If a scene file has previously been saved with those segmentation and markup nodes, the following script will allow for the python interpreter to have access to the previously created nodes:
>* *set resolution on previously saves scene.py*

## Functions
There are several custom functions which are run on volume, which are defined in the 'staticfunction.py' file.

>* *staticfunctions.py* 

  

**Segmentation functions:**  
colthresh() - run threshold on selected segment.
-sets the maximum entropy algorithm as minimum-
![alt text](colthresh.png)
colkeeplargestisland() runs the largest island on the 
thresholded columella

ecd() - sets the threshold on a segmented end of endosseous cochlear
duct (uses all values less than maxent) (highlights soft tissues)
-also runs keep largest island

umbo_ME_ISOtest() runs a threshold test, but doesn't apply it. If the threshold
doesn't work, the user can modify manually using the GUI

umbo_MES_ISO_apply() = runs threshold test and applies it



**Markup functions:**  
computedEC_TMmarkup() - joins together points from multiple fcsv
objects, in order to later be used in markup-to-model which will cover
an area encompassing points of intereset

ETmarkuptomodel() - runs the markup to model to create a region of interest
using the fcsv input

**Input/output function:**  
opennewvolume(): given the path for a folder, it opens the first 
volume , or file containing "tif", and also sets the ID and spacing
writecolvoltofile() - writes the columella volume to a file

fcsv_display_smaller() - change the display of all the markup nodes and lock for editing

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




