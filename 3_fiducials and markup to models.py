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
#CLICK TM FIRST!


#set ficudial display nodes
FIDNode1DisplayNode = FIDNode1.GetDisplayNode()
FIDNode1DisplayNode.SetGlyphScale(0.15)
FIDNode1DisplayNode.SetTextScale(0.1)
FIDNode1DisplayNode.SetSelectedColor(1,0,0)#red

FIDNode2DisplayNode = FIDNode2.GetDisplayNode()
FIDNode2DisplayNode.SetGlyphScale(0.15)
FIDNode2DisplayNode.SetTextScale(0.1)
FIDNode2DisplayNode.SetSelectedColor(0,1,0)#green

FIDNode3DisplayNode = FIDNode3.GetDisplayNode()
FIDNode3DisplayNode.SetGlyphScale(0.15)
FIDNode3DisplayNode.SetTextScale(0.1)
FIDNode3DisplayNode.SetSelectedColor(1,1,0)#green

FIDNode4DisplayNode = FIDNode4.GetDisplayNode()
FIDNode4DisplayNode.SetGlyphScale(0.15)
FIDNode4DisplayNode.SetTextScale(0.1)

FIDNode5DisplayNode = FIDNode5.GetDisplayNode()
FIDNode5DisplayNode.SetGlyphScale(0.15)
FIDNode5DisplayNode.SetTextScale(0.1)
FIDNode5DisplayNode.SetSelectedColor(0,0,0)#black

#lock the models to they don't get modified (1 = locked, 0 = unlocked)
FIDNode1.SetLocked(1)
FIDNode2.SetLocked(1)
FIDNode3.SetLocked(1)
FIDNode4.SetLocked(1)
FIDNode5.SetLocked(1) #keep this one open

#get nodes of TM and EC if already
#FIDNode1 = slicer.util.getFirstNodeByName('WCP-03-2019 TM')
#FIDNode4 = slicer.util.getFirstNodeByName('WCP-03-2019 EC')


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


#
################SAVE##################
 ################SAVE##################
 ################SAVE##################




## Write to STL file
#colout = segmentationNode.GetClosedSurfaceRepresentation(thresh_EC_TMseg)
#writer = vtk.vtkSTLWriter()
#writer.SetInputData(colout)
#writer.SetFileName("c:/tmp/something.stl")
#writer.Update()
#
#writer = vtk.vtkSTLWriter()
#writer.SetInputData(surfaceMesh)
#writer.SetFileName("C:/Users/jeffzeyl/Desktop/Volumetest.stl")
#writer.Update()
#"C:\Users\jeffzeyl\Desktop\Volumetest.stl"
#
## Make segmentation results nicely visible in 3D
#segmentationDisplayNode = segmentationNode.GetDisplayNode()
#
##segmentation colour
#segmentationDisplayNode.SetSegmentOpacity3D(ID+" ECplusTM", 0.4)
#
#segmentationDisplayNode.SetAllSegmentsVisibility()
#
#fiducialDisplayNode.SetVisibility(False) # Hide all points
#fiducialDisplayNode.SetVisibility(True) # Show all points
#
#
#
#FIDNode1.GetDisplayNode()
#FIDNOde1DisplayNode = FIDNode1.GetDisplayNode()
#FIDNOde1DisplayNode.SetVisibility(False) # Hide all points
#FIDNOde1DisplayNode.SetSelectedColor(1,1,0) # Set color to yellow
#
#defaultMarkupsDisplayNode = slicer.vtkMRMLMarkupsDisplayNode()
#defaultMarkupsDisplayNode.SetGlyphScale(0.3)
#defaultMarkupsDisplayNode.SetTextScale(0.3)
#
#segmentationNode = slicer.vtkMRMLSegmentationNode()#name segmentation n
#segmentationNodedisplaynode = segmentationNode.GetDisplayNode()
##remove 3D view
#segmentationNodedisplaynode.SetSegmentVisibility2DFill('pigeon paint col', 0)
#segmentationNodedisplaynode.SetSegmentVisibility2DOutline('pigeon paint col', 0)
#segmentationNodedisplaynode.SetSegmentVisibility3D('pigeon paint col', 0)
#
#
#modelnode =slicer.util.getNode('pigeon paint col')#create model node from the just created model
##remove visibility of 'EC_TM_mod' model
#modelnodeDisplayNode = modelnode.GetDisplayNode()
