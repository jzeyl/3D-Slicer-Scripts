

#specify folder to draw from and 
#\\Substack (135-715)0000.tif
import os
folder = "F:\\0CT Scans\\1_Jan 2019\\18012018_09 K151\\k151 oct17 16bbackofhead\\earcrp"
#\Substack (256-653)0000.tif
ID = "K151 2018"
spacing = 0.032#yes
firstfile = folder+'\\'+os.listdir(folder)[0]

#scene arleady saved
ID = "Flamingo01 2019"
spacing = 0.032#yes

#load volume
slicer.util.loadVolume(firstfile, returnNode=True)

#SET ROOT DIRECTORY to be in the same folder as the cropped files
slicer.mrmlScene.SetRootDirectory(folder)

#remove 3D slicer logo to increase room
slicer.util.findChild(slicer.util.mainWindow(), 'LogoLabel').visible = False

#You can print all Segment Editor effect parameter names by typing this into the Python console:
#print(slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentEditorNode"))
# Load dry bone CT of skull into the scene and run this script to automatically segment endocranium
#slicer.util.loadVolume("C:\\Users\\jeffzeyl\\Desktop\\RD01r2_2019\\pigeon0000.tif", returnNode=True)


masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
#slicer.util.getNode('pigeon0000')

#set resolution
#name the volume node and input resolution
#vol_node = slicer.util.getNode(os.listdir(folder)[0].replace('.tif',''))#the character inside is the one listed in 'data' module
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()

segmentationNode = slicer.util.getNode('Segmentation')

# Create SEGMENTATION NODE AND LINK TO VOLUME (if there isn't one already existing! otherwise, node can be named using the preceding command)
slicer.app.processEvents()
segmentationNode = slicer.vtkMRMLSegmentationNode()#name segmentation node
slicer.mrmlScene.AddNode(segmentationNode)#add the node to the scene
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)#link the segmentation to the volume

#CREATE EMPTY SEGMENTS
#boneSegmentID = segmentationNode.GetSegmentation().AddEmptySegment("bone")
paintcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint col")
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
#segmentEditorNode.SetSelectedSegmentID(paintcol)
#segmentEditorWidget.setActiveEffectByName("Paint")
#paintEffect = segmentEditorWidget.activeEffect()
#paintEffect.setParameter("BrushRelativeDiameter",10)
#paintEffect.setParameter("BrushSphere",1)

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

Moments_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
Moments_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
Moments_thresholdCalculator.SetMethodToMoments()
Moments_thresholdCalculator.Update()
Momentsval = Moments_thresholdCalculator.GetThreshold()

#MAX ENTROPY THRESHOLD OF COLUMELLA
#OverwriteMode: OverwriteNone
#SelectedSegmentID: threshcol
#ActiveEffectName: "Threshold"
#MaskMode: PaintAllowedInsideSingleSegment #segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideVisibleSegments)
#MaskSegmentID: paintcol
threshcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh col")
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
segmentEditorNode.SetMaskSegmentID(ID+" paint col")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
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
segStatLogic.getParameterNode().SetParameter("ScalarVolume", os.listdir(folder)[0].replace('.tif',''))############change here to the named volume
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.enabled","False")
segStatLogic.getParameterNode().SetParameter("ScalarVolumeSegmentStatisticsPlugin.voxel_count.enabled","False")
segStatLogic.computeStatistics()
segStatLogic.exportToTable(resultsTableNode)
segStatLogic.showTable(resultsTableNode)

#OR STORE STATS AS DICTIONARY:
import SegmentStatistics
segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_origin_ras.enabled",str(True))
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_diameter_mm.enabled",str(True))
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_x.enabled",str(True))
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_y.enabled",str(True))
segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_z.enabled",str(True))
segStatLogic.computeStatistics()
stats = segStatLogic.getStatistics()


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

#moments/ISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
effect = segmentEditorWidget.activeEffect()
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh umbo")
segmentEditorNode.SetMaskSegmentID(ID+" paint umbo")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect.setParameter("MinimumThreshold", str(ISOval))#//str(Momentsval)
effect.setParameter("MaximumThreshold",str(Maxentval))

effect.self().onApply()#apply separate

#remove visibility of painted segments
segmentationNodedisplaynode = segmentationNode.GetDisplayNode()#make display node

segmentationNodedisplaynode.SetSegmentVisibility2DFill(ID+" paint col", 0)
segmentationNodedisplaynode.SetSegmentVisibility2DOutline(ID+" paint col", 0)
segmentationNodedisplaynode.SetSegmentVisibility3D(ID+" paint col", 0)

segmentationNodedisplaynode.SetSegmentVisibility2DFill(ID+" paint umbo", 0)
segmentationNodedisplaynode.SetSegmentVisibility2DOutline(ID+" paint umbo", 0)
segmentationNodedisplaynode.SetSegmentVisibility3D(ID+" paint umbo", 0)

segmentationNodedisplaynode.SetSegmentVisibility2DFill(ID+" paint ECD", 0)
segmentationNodedisplaynode.SetSegmentVisibility2DOutline(ID+" paint ECD", 0)
segmentationNodedisplaynode.SetSegmentVisibility3D(ID+" paint ECD", 0)

segmentationNodedisplaynode.SetSegmentVisibility2DFill(ID+" thresh ECD", 1)

#TO DO - default settings paint for umbo. - 3d sphere
#TO DO - threshold Umbo - lower iso

#show segmentation in 3D
segmentationNode.CreateClosedSurfaceRepresentation()

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

# Make segmentation results visible in 3D
#segmentationNode.CreateClosedSurfaceRepresentation()
