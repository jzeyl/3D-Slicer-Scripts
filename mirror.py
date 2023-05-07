
#access first model in the scene (indices 0-2 are used by slice views)
modelskull1 = slicer.mrmlScene.GetNthNodeByClass(3, 'vtkMRMLModelNode')

#create new empty model for mirrored skull
modelmirror = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLModelNode','modelmirror')
modelmirror.CreateDefaultDisplayNodes()
modelmirror.GetDisplayNode().SetVisibility2D(True)

#perform mirror operation on second model, using surface toolbox
logic = slicer.util.getModuleLogic('SurfaceToolbox')
logic.transform(modelskull1, modelmirror, scaleX = -1.0)

#update GUI
slicer.app.processEvents()
#
##### Register two models using the 'modelregistration' module
#

#add and access transform node
slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLinearTransformNode', 'auto_registration')
outputTransform = getNode('auto_registration')

#run model registration from IGT model registration module (need to install)
import ModelRegistration as mr
mr.ModelRegistrationLogic().run(modelmirror, modelskull1,outputTransform)

#apply automatic registration transform to the mirrored model
logictransform = slicer.util.getModuleLogic('Transforms')
modelmirror.SetAndObserveTransformNodeID(outputTransform.GetID())

#update GUI
slicer.app.processEvents()
slicer.util.messageBox('Mirror and registration complete. Next is the conversion to segmentations and subtraction')


#create segmentation
def connect():
  """
  Connects the segmentation and volume nodes together in preparation for subsequent functions. Adds a segmentation node to the scene
  """
  global masterVolumeNode
  #Connect the volumes and segmentation to allow programatic access to model-segmentation conversion and segmentation effects
  masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')#detects the first scalar volume
  global segmentationNode
  segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
  segmentationNode.CreateDefaultDisplayNodes() # only needed for display
  segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)

connect()

#convert models to segmentation
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelskull1, segmentationNode)
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelmirror, segmentationNode)

#update GUI
slicer.app.processEvents()

#subtract 
def subtract():
  """
  Subtracts the original skull from the mirrored skull
  """
  # Create segment editor to get access to effects
  segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
  segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
  segmentEditorWidget.setSegmentationNode(segmentationNode)
  segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)
  #getnames
  mirror = segmentationNode.GetSegmentation().GetNthSegment(1).GetName()#get name of original skull
  originalskull = segmentationNode.GetSegmentation().GetNthSegment(0).GetName()#get name of mirror
  ##run subtraction
  segmentEditorWidget.setActiveEffectByName('Logical operators')
  effect = segmentEditorWidget.activeEffect()
  segmentEditorNode.SetSelectedSegmentID(mirror)######perform operations
  effect.setParameter("Operation", "SUBTRACT")
  effect.setParameter("ModifierSegmentID", originalskull)#subtract this selection
  effect.self().onApply()
  #remove segment editor connection
  segmentEditorWidget = None
  slicer.mrmlScene.RemoveNode(segmentEditorNode)

subtract()
print('subtraction complete')

def seg_to_stl(path):
  """
  """
  bafflename = segmentationNode.GetSegmentation().GetNthSegment(1).GetName()#get name of baffle
  segmentIds = vtk.vtkStringArray()
  segmentIds.InsertNextValue(bafflename)
  # Write to STL file
  slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsClosedSurfaceRepresentationToFiles(path, segmentationNode, segmentIds, "STL")

seg_to_stl("c:/tmp")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# write to file (write ALL segments)
#def segmentationnode2stl(path):
#  slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsClosedSurfaceRepresentationToFiles(path, segmentationNode, None, "STL")
#  slicer.util.messageBox(f'Exported stl files to {path}')
#
#segmentationnode2stl("c:/tmp")
#slicer.util.messageBox(f'Exported stl files to {path}')

#help(slicer.modules.modelregistration.logic())
#help(slicer.util.getModuleLogic('modelregistration'))



















