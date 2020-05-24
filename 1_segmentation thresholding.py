#specify folder to draw from and 
import os
firstfile = folder+'\\'+os.listdir(folder)[0]
firstfile = folder+'\\'+os.listdir(folder)[0]
#SET ROOT DIRECTORY to be in the same folder as the cropped files
slicer.mrmlScene.SetRootDirectory(folder)

slicer.util.findChild(slicer.util.mainWindow(), 'LogoLabel').visible = False

#You can print all Segment Editor effect parameter names by typing this into the Python console:
#print(slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentEditorNode"))
# Load dry bone CT of skull into the scene and run this script to automatically segment endocranium
slicer.util.loadVolume("C:\\Users\\jeffzeyl\\Desktop\\RD01r2_2019\\pigeon0000.tif", returnNode=True)

ID = "RD01 2019"##############INPUT SPECIMEN ID HERE
spacing = 0.018
masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
#slicer.util.getNode('pigeon0000')

#set resolution
#name the volume node and input resolution
import os
volnameinapp = 'pigeon0000'
vol_node = slicer.util.getNode(volnameinapp)#the character inside is the one listed in 'data' module
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
vol_node.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()


# Create SEGMENTATION NODE AND LINK TO VOLUME
slicer.app.processEvents()
segmentationNode = slicer.vtkMRMLSegmentationNode()#name segmentation node
slicer.mrmlScene.AddNode(segmentationNode)#add the node to the scene
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)#link the segmentation to the volume

#CREATE EMPTY SEGMENTS
#boneSegmentID = segmentationNode.GetSegmentation().AddEmptySegment("bone")
paintcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint col")
threshcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh col")
paintumbo = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint umbo")
threshumbo = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh umbo")
paintecd = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint ECD")
threshecd = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh ECD")


# Create SEGMENT EDITOR WIDGET to get access to effects
# To show segment editor widget (useful for debugging): segmentEditorWidget.show()
#slicer.app.processEvents()
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)#connect widget to scene
segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
slicer.mrmlScene.AddNode(segmentEditorNode)#add segment editor node to scene
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)#connect segment editor to editor widget
segmentEditorWidget.setSegmentationNode(segmentationNode)#connect segmentation node
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)#connect master node

#PAINT COLUMELLA SETTING
#paintcolseg = segmentationNode.GetSegmentation().AddEmptySegment("paintcol")
#paintcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint col")
#slicer.app.processEvents()
segmentEditorNode.SetSelectedSegmentID(paintcol)
segmentEditorWidget.setActiveEffectByName("Paint")
paintEffect = segmentEditorWidget.activeEffect()
paintEffect.setParameter("BrushRelativeDiameter",10)
paintEffect.setParameter("BrushSphere",1)

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

#MAX ENTROPY THRESHOLD OF COLUMELLA
#OverwriteMode: OverwriteNone
#SelectedSegmentID: threshcol
#ActiveEffectName: "Threshold"
#MaskMode: PaintAllowedInsideSingleSegment #segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideVisibleSegments)
#MaskSegmentID: paintcol
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
segmentEditorNode.SetMaskSegmentID(ID+" paint col")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
#effect.setParameter("Threshold.AutoThresholdMethod","MAXIMUM_ENTROPY")#maximum entropy algorithm
#effect.setParameter("Threshold.AutoThresholdMode","SET_LOWER_MAX")
#effect.setParameter("MinimumThreshold",0)
#effect.setParameter("MaximumThreshold",695)
#effect.setParameter("MaskSegmentID",ID+" paint col")
effect.self().onApply()#apply separate

#run keep largest island on thresholded columella
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")

effect.self().onApply()#apply separate

#quantification table
resultsTableNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTableNode')# create table node
import SegmentStatistics
segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
segStatLogic.getParameterNode().SetParameter("ScalarVolume", 'pigeon0000')############change here to the named volume
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.enabled","False")
segStatLogic.getParameterNode().SetParameter("ScalarVolumeSegmentStatisticsPlugin.voxel_count.enabled","False")
segStatLogic.computeStatistics()
segStatLogic.exportToTable(resultsTableNode)
segStatLogic.showTable(resultsTableNode)

#OR STORE STATS AS DICTIONARY:
#import SegmentStatistics
#segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
#segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_origin_ras.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_diameter_mm.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_x.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_y.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_z.enabled",str(True))
#segStatLogic.computeStatistics()
#stats = segStatLogic.getStatistics()


#MAX ENTROPY THRESHOLD OF ECD
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh ECD")
segmentEditorNode.SetMaskSegmentID(ID+" paint ECD")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
#effect.setParameter("AutoThresholdMode",'SET_MIN_UPPER')
#effect.setParameter("AutoThresholdMethod","MAXIMUM_ENTROPY")#maximum entropy algorithm
effect.setParameter("MinimumThreshold", str(0))
effect.setParameter("MaximumThreshold",str(Maxentval))

effect.self().onApply()#apply separate

#run KEEP LARGEST ISLAND on thresholded columella
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
segmentEditorNode.SetSelectedSegmentID(ID+" thresh ECD")
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")

effect.self().onApply()#apply separate

#ISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh umbo")
segmentEditorNode.SetMaskSegmentID(ID+" paint umbo")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(ISOval))
effect.setParameter("MaximumThreshold",str(Maxentval))

effect.self().onApply()#apply separate

#TO DO - default settings paint for umbo. - 3d sphere
#TO DO - threshold Umbo - lower iso



#OTHER FIDUCIAL CODE< MAY BE USEFUL:
# Get point positions as numpy array
#import numpy as np
#nOfFiduciallPoints = FIDNode5.GetNumberOfFiducials()
#points = np.zeros([nOfFiduciallPoints,3])
#for i in range(0, nOfFiduciallPoints):
#  FIDNode5.GetNthFiducialPosition(i, points[i,:])
#
#points[2][1]
#points[2][1]

#Change markup fiducial display properties
#Display properties are stored in display node(s) associated with the fiducial node.
#defaultMarkupsDisplayNode = slicer.vtkMRMLMarkupsDisplayNode()
#defaultMarkupsDisplayNode.SetGlyphScale(0.3)
#defaultMarkupsDisplayNode.SetTextScale(0.3)
#slicer.mrmlScene.AddDefaultNode(defaultMarkupsDisplayNode)
#
#fiducialNode = getNode('F')
#fiducialDisplayNode = fiducialNode.GetDisplayNode()
#fiducialDisplayNode.SetSelectedColor(1,1,0) # Set color to yellow
#
#fiducialDisplayNode.SetVisibility(False) # Hide all points
#fiducialDisplayNode.SetVisibility(True) # Show all points
#fiducialDisplayNode.SetViewNodeIDs(["vtkMRMLSliceNodeRed", "vtkMRMLViewNode1"]) # Only show in red slice view and first 3D view
##################################################################################333

##fidNode = getNode("vtkMRMLMarkupsFiducialNode1")
##n = fidNode.AddFiducial(4.0, 5.5, -6.0)
##fidNode.SetNthFiducialLabel(n, "new label")
### each markup is given a unique id which can be accessed from the superclass level
##id1 = fidNode.GetNthMarkupID(n)
### manually set the position
##fidNode.SetNthFiducialPosition(n, 6.0, 7.0, 8.0)
### set the label
##fidNode.SetNthFiducialLabel(n, "New label")
### set the selected flag, only selected = 1 fiducials will be passed to CLIs
##fidNode.SetNthFiducialSelected(n, 1)
### set the visibility flag
##fidNode.SetNthFiducialVisibility(n, 0)  



# Make segmentation results nicely visible in 3D
segmentationDisplayNode = segmentationNode.GetDisplayNode()
segmentationDisplayNode.SetSegmentOpacity3D(threshcol, 0.4)

# Find largest object, remove all other regions from the segment
slicer.app.processEvents()
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
effect.self().onApply()


# Make segmentation results visible in 3D
#segmentationNode.CreateClosedSurfaceRepresentation()
