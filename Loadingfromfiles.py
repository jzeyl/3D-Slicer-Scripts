filesinfolder = slicer.util.getFilesInDirectory(r'C:\Users\jeffzeyl\Desktop\copyoutput\Jun25 batch\ADP01')

vol = "tif"
volfile = [i for i in filesinfolder if vol in i] 

fcsvregex = "fcsv"
fcsvfiles = [i for i in filesinfolder if fcsvregex in i] 

stlregex = "stl"
stlfiles = [i for i in filesinfolder if stlregex in i] 

#get file sizes
import os
for i in range(0,len(stlfiles)):
    os.stat(stlfiles[i]).st_size

#select files greater than 1000000

#load volume
slicer.util.loadVolume(volfile)

#SET ID AND SPACING

#set up volume resolution
masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
import itertools
imagespacing = [spacing]*3
masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()


#load fiducial files
for i in range(0,len(fcsvfiles)):
    slicer.util.loadMarkupsFiducialList(fcsvfiles[i])










"C:/Users/jeffzeyl/Desktop/copyoutput/Jun10 batch/BO_02"

#load volume
slicer.util.loadVolume(firstfile, returnNode=True)

#load fcsv


#load models greater than certain size


#displaynodelist = slicer.mrmlScene.GetNodesByClass('vtkMRMLMarkupsDisplayNode')
#for i in range(len(displaynodelist)):
#    print(displaynodelist[i])
#slicer.mrmlScene.GetNthNodeByClass(1,'vtkMRMLMarkupsDisplayNode').

#displaynodelist[0]

masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()

#set up segmentatin node
segmentationNode = slicer.util.getNode('Segmentation')

segmentationDisplayNode=segmentationNode.GetDisplayNode()
#if previously saved
segmentEditorNode = slicer.util.getNode('SegmentEditor')

# Create segment editor to get access to effects
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)#connect widget to scene
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)#connect segment editor to editor widget
segmentEditorWidget.setSegmentationNode(segmentationNode)#connect segmentation node
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)#connect master node

# Compute bone threshold value automatically
import vtkITK
ME_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
ME_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
ME_thresholdCalculator.SetMethodToMaximumEntropy()
ME_thresholdCalculator.Update()
Maxentval = ME_thresholdCalculator.GetThreshold()

ISO_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
ISO_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
ISO_thresholdCalculator.SetMethodToIsoData()
ISO_thresholdCalculator.Update()
ISOval = ISO_thresholdCalculator.GetThreshold()

#SET DISPLAY OF ALL FIDUCIALS AND LOCK
displaynodelist = slicer.util.getNodesByClass('vtkMRMLMarkupsDisplayNode')
for i in range(len(displaynodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetGlyphScale(0.15)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetTextScale(0.15)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetSelectedColor(0,0,0)#black

#get names of marksup
markupfiducials = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')

for i in range(len(markupfiducials)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').SetLocked(1)


FIDNode5 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode5.SetName(ID+"ECandTMmrk_outline")#creates a new segmentation
FIDNode5DisplayNode = FIDNode5.GetDisplayNode()
FIDNode5DisplayNode.SetGlyphScale(0.15)
FIDNode5DisplayNode.SetTextScale(0.1)
FIDNode5DisplayNode.SetSelectedColor(1,0,0)#black

#FIDNode1 = getNode(ID+" TM")
#FIDNode2 = getNode(ID+" RW")
#FIDNode3 = getNode(ID+" CA")
#FIDNode4 = getNode(ID+" EC")
FIDNode5 = getNode(ID+"ECandTMmrk_outline")



#get the names of all the markups
markuplist = []
#markuplst.extend[0*range(len(markupfiducials))]

#make a list of the markups present
for i in range(len(markupfiducials)):
    markuplist.append(slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').GetName())

markuplist

FIDNode4 = slicer.util.getNode(markuplist[3])#Fignod4 is EC
FIDNode1 = slicer.util.getNode(markuplist[0])#Fignode1 is TM perimeter

#import re
##fruit_list = ['raspberry', 'apple', 'strawberry']
#TMindex = [i for i, item in enumerate(markuplst) if re.search('TM', item)]
#Set lock all of the markupfiducials

#slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').GetName(ID+)


#setcolor of models to all the same colour
modelnodelist = slicer.util.getNodesByClass('vtkMRMLModelNode')

#get the names of all the models
for i in range(len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetName()

#set colour of all to red
for i in range(3,len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetDisplayNode().SetColor(0,1,0)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetDisplayNode().SetOpacity(0.5)
    
#make all models visible or not:
for i in range(3,len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').SetDisplayVisibility(0)
#convert models to markups

#markups fiducial node
for i in range(len(displaynodelist)):
    inputMarkups = slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode')
    #create model node
    ECTMModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
    ECTMModel.SetName('_newmm')
    ECTMModel.CreateDefaultDisplayNodes()
    ECTMModel.GetDisplayNode().SetSliceIntersectionVisibility(True)
    ECTMModel.GetDisplayNode().SetColor(0,0,0)
    #create markups to model node
    markupsToModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
    markupsToModel.SetAutoUpdateOutput(True)
    markupsToModel.SetAndObserveMarkupsNodeID(inputMarkups.GetID())#set input node
    markupsToModel.SetAndObserveModelNodeID(ECTMModel.GetID())#set model node (only needed for the first one)
    markupsToModel.SetModelType(1)#curve
    markupsToModel.SetTubeRadius(0.05)
    markupsToModel.SetTubeLoop(1)#1 = curve is a loop
    markupsToModel.SetCurveType(0)#polynomial least squares


####check the coverage of the model in 4d view
# CONVERT TO segmentation
modeloutlinenode = slicer.util.getNode(ID+'EC_TM_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'EC_TM_mod' model and 
modeloutlinenode.SetDisplayVisibility(0)

