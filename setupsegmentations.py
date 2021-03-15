segmentationNode = slicer.vtkMRMLSegmentationNode()#name segmentation node
slicer.mrmlScene.AddNode(segmentationNode)#add the node to the scene
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationDisplayNode=segmentationNode.GetDisplayNode()

segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)#link the segmentation to the volume
#CREATE EMPTY SEGMENTS
paintcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint col")
paintumbo = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint umbo")
threshumbo = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh umbo")
paintecd = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint ECD")

threshecd = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh ECD")

#threshcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh col")
#add segment editor node

segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
slicer.mrmlScene.AddNode(segmentEditorNode)#add segment editor node to scene
#if previously saved
#segmentEditorNode = slicer.util.getNode('SegmentEditor')
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

