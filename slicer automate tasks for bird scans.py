#specify folder to draw from and 
import os
folder = 'F:\\0CT Scans\\1_Jan 2019\\17012019_03 Sooty shearwater\\sootybac of head 17b\\earcrp' #\Substack (368-749)0000.tif"
ID = "Sooty01 2019"
spacing = 0.032#input resolution
firstfile = folder+'\\'+os.listdir(folder)[0]

vol = slicer.util.loadVolume(firstfile, returnNode=True)#load volume from file
slicer.mrmlScene.SetRootDirectory(folder)#set root directory to be in the same folder as the cropped files

#name the volume node and input resolution
volnamesubstack = os.listdir(folder)[0]
vol_node = slicer.util.getNode(volnamesubstack.replace('.tif',''))#the character inside is the one listed in 'data' module
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
vol_node.SetSpacing(imagespacing)#assign resolution to volume

import vtkSegmentationCorePython as vtkSegmentationCore# need to import this to add empty segment function
#seg = getNode('Segmentation')#name the default segmentation node
segNode = slicer.vtkMRMLSegmentationNode()
slicer.mrmlScene.AddNode(segNode)#adds in a segmentation, defaults to 'Segmentation1'
theSegmentation = segNode.GetSegmentation()
theSegmentation.AddEmptySegment(ID+"paint col")
theSegmentation.AddEmptySegment(ID+"thresh col")
theSegmentation.AddEmptySegment(ID+"paint umbo")
theSegmentation.AddEmptySegment(ID+"thresh umbo")
theSegmentation.AddEmptySegment(ID+"paint ECD")
theSegmentation.AddEmptySegment(ID+"thresh ECD")

#import empty fiducial markups
FIDNode1 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode1.SetName(ID+" TM")#creates a new segmentation
FIDNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode2.SetName(ID+" RW")#creates a new segmentation
FIDNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode3.SetName(ID+" CA")#creates a new segmentation
FIDNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode4.SetName(ID+" EC")#creates a new segmentation
