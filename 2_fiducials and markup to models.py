######################################################################################3
#import empty fiducial markups
FIDNode1 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode1.SetName(ID+" TM")#creates a new segmentation
FIDNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode2.SetName(ID+" RW")#creates a new segmentation
FIDNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode3.SetName(ID+" CA")#creates a new segmentation
FIDNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode4.SetName(ID+" EC")#creates a new segmentation
FIDNode5 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
FIDNode5.SetName(ID+"ECandTMmrk_outline")#creates a new segmentation

####SELECT POINTS in GUI###


#USE MARKUP FIDUCIALS SELECTED TO OUTLINE TM AND EXTRACOLUMELLA REGION FROM , FOR SUBSEQUENT AUTO SEGMENTATION
import numpy as np

#Extracolumella
numberfiducialpoints = FIDNode4.GetNumberOfFiducials()#g
points = np.zeros([numberfiducialpoints,3])#4 rows, 3 columns (i.e., 4 points, each with x,y,z)
FIDNode4.GetNthFiducialPosition(0,points[0,:])#get first point of EC markup (umbo)
umbo = points[0,]
FIDNode4.GetNthFiducialPosition(1,points[1,:])#get second point from first row of numpy array
coltip = points[1,]

#add the columella and umbo point to the new "ECandTMmrk_outline" node
FIDNode5.AddFiducial(umbo[0],umbo[1],umbo[2])#add umbo
FIDNode5.AddFiducial(coltip[0],coltip[1],coltip[2])#add coltip point

#add TM markup points to an array, and add from array to 
numberfiducialpoints = FIDNode1.GetNumberOfFiducials()
points = np.zeros([numberfiducialpoints,3])#array to populate with TM fiducial points

for i in range(0, numberfiducialpoints):#put the TM points into the 'points' array
  FIDNode1.GetNthFiducialPosition(i, points[i,:])

#add the fiducial nodes from the 'points array' to the "ECandTMmrk_outline" node
for i in range(0,numberfiducialpoints):
  FIDNode5.AddFiducial(points[i,][0],points[i,][1],points[i,][2])


#now run the markups model in GUI to create a model. 
# 
# Then need to import as a segmentation
modeloutlinenode =slicer.util.getNode('EC_TM_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")

#now run the thresholding on the EC_TM_mod area
#create maxent segment, isodata segment, and subtract the two
thresh_EC_TMseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" ECplusTM")#create new segmentation ID

#ISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" ECplusTM")
segmentEditorNode.SetMaskSegmentID('EC_TM_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(ISOval))
effect.setParameter("MaximumThreshold",str(Maxentval))

effect.self().onApply()#apply separate


# Make segmentation results nicely visible in 3D
segmentationDisplayNode = segmentationNode.GetDisplayNode()

#segmentation colour
segmentationDisplayNode.SetSegmentOpacity3D(ID+" ECplusTM", 0.4)

segmentationDisplayNode.SetAllSegmentsVisibility()

fiducialDisplayNode.SetVisibility(False) # Hide all points
fiducialDisplayNode.SetVisibility(True) # Show all points



FIDNode1.GetDisplayNode()
FIDNOde1DisplayNode = FIDNode1.GetDisplayNode()
FIDNOde1DisplayNode.SetVisibility(False) # Hide all points
FIDNOde1DisplayNode.SetSelectedColor(1,1,0) # Set color to yellow