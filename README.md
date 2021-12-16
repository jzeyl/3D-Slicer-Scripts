# 3DSlicer Automation Python Scripts
This repository includes Python scripts for running commands for 3D Slicer 4.10.1 using the built-in interpreter. Using these scripts greatly speeds up repetitive tasks for loading and processing volumes that would otherwires require repetative button-clicking the GUI while working through many files. It automotates the creation of segmentation nodes and markup nodes with unique identifies for each volume/specimen. Then there are functions which run specific effects (e.g., segmentation effects, modifications to markup display) using those segmentation and markup nodes.
Scripts are based on modifications of the 3D Slicer nightly scripts repository https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository
 and 3D Slicer source code https://github.com/Slicer/Slicer. 



## 1. Creating data for the first time
First, a unique ID code, resolution, and file path for the folder where the volume is located are created. 

>* *1_set up volume and segmentation nodes.py*  

Next, repeatable segmentation nodes are created with the unique IDs in the naming:
>* set up segmentations.py
![alt text](addsegnames.PNG)

=======
OR, if opening previously saved scenes file 

Next there is a need to populate markup nodes, also named according to unique IDs:

>* fcsv_template(): set up fcsv names
![alt text](markupscreated.PNG)
=======
![alt text](markupscreated.PNG)  

If a scene file has previously been saved with those segmentation and markup nodes, the following script will allow for the python interpreter to have access to the previously created nodes:

>* *set resolution on previously saves scene.py*

## Functions
There are several custom functions which are run on volume, which are defined in the 'staticfunction.py' file. This script includes the following functions:

  

### **Segmentation functions:**  
**colthresh()** - run threshold on selected segment.
-sets the maximum entropy algorithm as minimum-
![alt text](colthresh.PNG)  
**colkeeplargestisland()** - runs the largest island on the 
thresholded columella

**ecd()** - sets the threshold on a segmented end of endosseous cochlear duct (uses all values less than maxent) (highlights soft tissues). Also runs keep largest island

**umbo_ME_ISOtest()** - runs a threshold test, but doesn't apply it. If the threshold
doesn't work, the user can modify manually using the GUI

**umbo_MES_ISO_apply()**- runs threshold test and applies it



### **Markup functions:**  
**computedEC_TMmarkup()** - joins together points from multiple fcsv
objects, in order to later be used in markup-to-model which will cover an area encompassing points of intereset

**ETmarkuptomodel()** - runs the markup to model to create a region of interest
using the fcsv input

### **Input/output functions:**  
**opennewvolume()** - given the path for a folder, it opens the first volume , or file containing "tif", and also sets the ID and spacing  
**writecolvoltofile()** - writes the columella volume to a file  
**fcsv_display_smaller()** - change the display of all the markup nodes and lock for editing

### **Markups-to-models module to select segmentation region** 
>The *4_markups to models.py* file uses the markup-to-models module to create a model from fcsv points. This 3D model can then be converted to a segmentation as a region of interest for further processing.

![alt text](markupstomodel.PNG)
-it then converts the model to a segmentation, which can be edited using the normal segmentation effects:  
![alt text](tosegmentation.PNG)
![alt text](segmentedinsidemodel.PNG)

## 2. Importing data from a folder, setting resolutions
 
These set of scripts are for loading a volume, several fcsv files, and models from a single folder. This allows for loading components of interest without having to load all the segmentations. The scripts also format the color and opacity of the models and fcsv points
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




