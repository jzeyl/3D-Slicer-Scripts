

# 3D Slicer Automation Python Scripts
3D Slicer software has a [scripts repository](https://www.slicer.org/wiki/Documentation/Nightly/ScriptRepository) for automating tasks in the software using the software's built-in interpreter. Using these scripts greatly speeds up repetitive tasks for loading and processing volumes that would otherwires require repetative button-clicking the GUI while working through many files. 


The present repository is a collection of some of my personal Python scripts I have used for running commands for 3D Slicer 4.1 and Slicer 5. The scripts automatically create segmentation nodes and markup nodes with unique identifier for each volume/specimen. There are several functions to run specific effects available through the GUI (e.g., segmentation effects, modifications to markup display) using those segmentation and markup nodes. 

##  Miscellaneous scripts:
>* *change color of background display 3d.py* -   
>* *switch mouse int markup mode.py* - 
>* *thickness.py* - compute thickness
>* *functions_baffle_planner* - modele to segmentations and access segmentation logic
>* *load_dicom_modified_otsu.py* load dicom and automatically run grayscale model maker using otsu threshold. Can be run from command line using arguments for DICOM folder 
>* *mirror.py* use of surface toolbox to transform/rotate model and use of model registration module within IGT
>* *elasitxreg_skullstripping_shnode* running elastix registration and skull stripping. organization in folders and export volumes, segmentation, and scene files
>* *commandl line_loopfolders_volume rendering* using argparse run a custom volume rendering and screenshot export on all files in a folder
>* *2D slice_distance_thresh_outline* specifying a current slice (specify red, green, or yellow axis), this hollows a segmentation to get a segmentation outline for two segmentations on that slice. then, extracts the numyp array to calculate the distances between two segmentation. Then, converting back to RAS coordinates, plost the outlines within a given distance of the other
>* *Crop volume using ROI* - automatation of crop volume module. Some investigation of dicom tags
>* *AIAA jun 17.py* - autosegmentation using nvidia AIAA
>* *XRAY batch_jun19.py* - apply median filter and mask volume segmentation effects. Draw text using opencv and imageio, save as png/jpg. Combine before and after images, sidebyside
>* *diploe_thickness_github.py* - apply segmentation effects, then run binary thinning and danielssondistance filters, to create a thickenss map using 'probe model with volume'
>* *diploe_pt2.py* - slice a model into 3D grid using dynamic modeler and using 'clean' from surface toolbox. Saving mean thickness to a text file. Batch process
>* *seg2thickness.py* - load segmentation for each folder, along with danielssondistance volume, to create a thickness map for each segmentation and save to a file
>* *radiomics2.py* - batch-run radiomics module inside slicer and save results to excel files

Additional scripts cover my particular analysis for  
(1) the [setup of segmentations and effects given a volume that has been imported](#1.-creating-data-for-the-first-time) and   
(2) [importing from a folder](#2.-importing-data-from-a-folder,-setting-resolutions),   

## 1. Creating data for the first time
First, create a unique ID code, resolution, and file path for the folder where the volume is located are created. 

>* *1_set up volume and segmentation nodes.py*  

Next, repeatable segmentation nodes are created with the unique IDs in the naming:

>* set up segmentations.py
![alt text](addsegnames.PNG)


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



