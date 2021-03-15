
#You can print all Segment Editor effect parameter names by typing this into the Python console:
#print(slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentEditorNode"))
# Load dry bone CT of skull into the scene and run this script to automatically segment endocranium
#slicer.util.loadVolume("C:\\Users\\jeffzeyl\\Desktop\\RD01r2_2019\\pigeon0000.tif", returnNode=True)

slicer.util.loadVolume(r"C:\Users\jeffz\Desktop\copyoutput\Jun5 batch\Pcrow\crowbetter0000.tif", returnNode=True)
spacing = 0.021875#set resolution
ID = "PCrow"

masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
#or can get the volume node by the name slicer.util.getNode('pigeon0000')
#print(mastervolumeNode)
#set resolution
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()

# Create SEGMENTATION NODE AND LINK TO VOLUME (if there isn't one already existing! otherwise, node can be named using the preceding command)
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

#make segmentation display node
segmentationDisplayNode=segmentationNode.GetDisplayNode()
#set 3d opacity at 0.5
#segmentationDisplayNode.SetSegmentOpacity3D(ID+" thresh umbo", 0.50)
#segmentationDisplayNode.SetSegmentOpacity3D(ID+" thresh ECD", 0.50)
#segmentationDisplayNode.SetSegmentOpacity3D(ID+" paint col", 0.50)

#but segment colour set in segmentation node:
segmentationNode.GetSegmentation().GetSegment(ID+" thresh umbo").SetColor(1,0,0)
segmentationNode.GetSegmentation().GetSegment(ID+" thresh ECD").SetColor(0,1,0)

#add segment editor node
segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
slicer.mrmlScene.AddNode(segmentEditorNode)#add segment editor node to scene

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

Moments_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
Moments_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
Moments_thresholdCalculator.SetMethodToMoments()
Moments_thresholdCalculator.Update()
Momentsval = Moments_thresholdCalculator.GetThreshold()

Otsu_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
Otsu_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
Otsu_thresholdCalculator.SetMethodToOtsu()
Otsu_thresholdCalculator.Update()
Otsuval = Otsu_thresholdCalculator.GetThreshold()

