#STEP 1
ID = "myskullid"##################type the name you want for the segmentation & model here
mythresh = 2# input the threshold thickness value you want to dissplay on the colormap label
#NOTE - this scripts interacts with items (volumes, segmentations, models) based on the name 'getNode('xxxx'),
#so if you modify names, you will also need to modify the corresponding part of the script

######################################################SETUP ENVIRONMENT###########################################
#This section creates objects to access volumes, segmentations, and segmentation effects

#set up the volume - name the volume as an object
masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()#value used in threshold computation for segmentation

# Create SEGMENTATION NODE AND LINK TO VOLUME 
segmentationNode = slicer.vtkMRMLSegmentationNode()#name segmentation node
slicer.mrmlScene.AddNode(segmentationNode)#add the node to the scene
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)#link the segmentation to the volume

# Create segment editor to get access to segmentation effects
segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
slicer.mrmlScene.AddNode(segmentEditorNode)#add segment editor node to scene
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)#connect widget to scene
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)#connect segment editor to editor widget
segmentEditorWidget.setSegmentationNode(segmentationNode)#connect segmentation node
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)#connect master node

#calculate the threshold value for maximum entry algorithm segmentation
import vtkITK
ME_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
ME_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
ME_thresholdCalculator.SetMethodToMaximumEntropy()
ME_thresholdCalculator.Update()
Maxentval = ME_thresholdCalculator.GetThreshold()

#STEP 2
####################################################Create skull segmentation######################################################
#create segmentation of the bone using the threshold effect and 'maximum entropy' algorithm
skull = segmentationNode.GetSegmentation().AddEmptySegment(ID)
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetSelectedSegmentID(ID)
segmentEditorNode.SetMaskSegmentID(ID)
segmentEditorWidget.setActiveEffectByName("Threshold")

#apply threshold effect
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
effect.self().onApply()#apply separate
segmentationNode.GetSegmentation().GetSegment(ID).SetColor(0,0,1) #color of segmentation is set to blue here

#apply 'keep largest' island segmentation effect
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
segmentEditorNode.SetSelectedSegmentID(ID)
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
effect.self().onApply()#apply separate
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
segmentEditorNode.SetSelectedSegmentID(ID)
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
effect.self().onApply()#apply separate

#STEP 3
##########################################export segmentation to model#######################################
segmentationNode = getNode(ID)
shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
exportFolderItemId = shNode.CreateFolderItem(shNode.GetSceneItemID(), "Segments")
slicer.modules.segmentations.logic().ExportAllSegmentsToModels(segmentationNode, exportFolderItemId)

#STEP 4
##########################Generate a label-map volume from the segmentation of the skull##########################
labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode, labelmapVolumeNode, masterVolumeNode)
slicer.util.saveNode(labelmapVolumeNode, "c:/tmp/BodyComposition-label.nrrd")

#STEP 5
###########################Create a medial surface from the label-map using the BinaryThinningImageFilter##################
##note this is computationally expensive step- many take many minutes to complete #####
import SampleData
import SimpleITK as sitk
import sitkUtils
# Get input volume node
inputVolumeNode_label =  slicer.util.getNode('LabelMapVolume')#the string here is what you have the labelmap named as
# Create new volume node for output
binarythinning_outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode", "binarythinning_filter")#second string is name you give it
# Run filter
inputImage = sitkUtils.PullVolumeFromSlicer(inputVolumeNode_label)
filter = sitk.BinaryThinningImageFilter()
outputImage = filter.Execute(inputImage)
sitkUtils.PushVolumeToSlicer(outputImage, binarythinning_outputVolumeNode)
# Show processing result
#slicer.util.setSliceViewerLayers(background=binarythinning_outputVolumeNode)

#STEP 6
#############################Create a distance map from the medial surface using the DanielssonDistanceMapImageFilter ###############3
### with options Input is Binary = Yes and Use Image Spacing=Yes
# Get input volume node
inputVolumeNode_label =  slicer.util.getNode("binarythinning_filter")#the string here "binarythinning_filter" is what you are naming the labelmap
# Create new volume node for output
DanielssonDistanceMap_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "DanielssonDistance")#second string is name you give it

# Run filter
inputImage = sitkUtils.PullVolumeFromSlicer(inputVolumeNode_label)
filter = sitk.DanielssonDistanceMapImageFilter()
filter.InputIsBinaryOn()#input is binary,
filter.SetUseImageSpacing(True)#use image spaceing
outputImage = filter.Execute(inputImage)
sitkUtils.PushVolumeToSlicer(outputImage, DanielssonDistanceMap_node)

#double the medial thickness to get a volume with total thickness, not medial thickness
volumeNode = getNode('DanielssonDistance')
a = arrayFromVolume(volumeNode)
# Increase scalar values by two
a[:] = a * 2.0
arrayFromVolumeModified(volumeNode)
#type a again and see that the array values have doubled


#STEP 7
#################### create the model with the colored thickness##########################
#this function maps the thickness values onto the model. It essentially connects the 
#relevant parameters (i.e., input volume, model) into the existing C++ function
#for mor information see https://slicer.readthedocs.io/en/latest/developer_guide/python_faq.html?highlight=CLI#how-to-run-a-cli-module-from-python

def createprobevoltomodel(inputVolumeNode):
  """create texture on model  using CLI module"""
  # Set parameters
  parameters = {}
  parameters["InputVolume"] = inputVolumeNode#input volume [image]
  parameters["InputModel"] = slicer.util.getFirstNodeByName(ID, className="vtkMRMLModelNode")
  parameters["OutputArrayName"] = "thickness_model"
  outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode","thickness")
  parameters["OutputModel"] = outputModelNode
  
    #parameters of CLU module
    #Group: IO
    #  InputVolume [image]: Input volume
    #  InputModel [geometry]: Input model
    #  OutputModel [geometry]: Output model
    #  OutputArrayName [string]: Output array name
  # Execute
  grayMaker = slicer.modules.probevolumewithmodel
  cliNode = slicer.cli.runSync(grayMaker, None, parameters)
  # Process results
  if cliNode.GetStatus() & cliNode.ErrorsMask:
    # error
    errorText = cliNode.GetErrorText()
    slicer.mrmlScene.RemoveNode(cliNode)
    raise ValueError("CLI execution failed: " + errorText)
  # success
  slicer.mrmlScene.RemoveNode(cliNode)
  return outputModelNode

volumeNode = getNode("DanielssonDistance")#get the appropriate volume node
createprobevoltomodel(volumeNode)#run the function and generate the model


##STEP 8 
#####Create the colormap label
thicknessMapNode = getNode("thickness")#call the model with the thickness painted on it

# Create color node
colorNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLProceduralColorNode")
colorNode.UnRegister(None)  # to prevent memory leaks
colorNode.SetName(slicer.mrmlScene.GenerateUniqueName("MedialThicknessMap"))
#colorNode.SetAttribute("Category", "MedialThicknessModule")
# The color node is a procedural color node, which is saved using a storage node.
# Hidden nodes are not saved if they use a storage node, therefore the color node must be set to visible.
colorNode.SetHideFromEditors(False)
slicer.mrmlScene.AddNode(colorNode)

#make 
import numpy as np
scalars = vtk.util.numpy_support.vtk_to_numpy(thicknessMapNode.GetPolyData().GetPointData().GetScalars())
maxThickness    = np.max(scalars)
#set threshrange
thresh = mythresh/maxThickness# this will be used to compute wheree the thickness threshold will occur on the label (as a proportion of max thickness)

# Colormap - threshold 
colorMap = colorNode.GetColorTransferFunction()
colorMap.RemoveAllPoints()#specify points for color map
colorMap.AddRGBPoint(0.0, 0.0, 0.0, 1.0)
colorMap.AddRGBPoint(thresh, 0.0, 0.0, 1.0)#put one color for all values below threshold
colorMap.AddRGBPoint(thresh+0.01, 1.0, 0.0, 0.0)#put one color for all values below threshold
colorMap.AddRGBPoint(1, 1.0, 0.0, 0.0)#

# Display color legend
thicknessMapNode.GetDisplayNode().SetAndObserveColorNodeID(colorNode.GetID())
##NOTE - if you want other default color schemes, just replace this line with the preceding. Here is the 'rainbow' theme:
#thicknessMapNode.GetDisplayNode().SetAndObserveColorNodeID("vtkMRMLColorTableNodeRainbow")

colorLegendDisplayNode = slicer.modules.colors.logic().AddDefaultColorLegendDisplayNode(thicknessMapNode)
colorLegendDisplayNode.SetTitleText("Thickness (mm)")
colorLegendDisplayNode.SetLabelFormat("%4.1f mm")


