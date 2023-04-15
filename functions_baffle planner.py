
def subtract():
  """
  Subtracts the skull (first segment) from the baffle (second segment)
  """
  masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')
  segmentationNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLSegmentationNode')
  segmentationNode.CreateDefaultDisplayNodes() # only needed for display
  segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
  # Create segment editor to get access to effects
  segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
  segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
  segmentEditorWidget.setSegmentationNode(segmentationNode)
  segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)
  #getnames
  bafflename = segmentationNode.GetSegmentation().GetNthSegment(1).GetName()#get name of baffle
  skullname = segmentationNode.GetSegmentation().GetNthSegment(0).GetName()#get name of skull
  ##run subtaction
  segmentEditorWidget.setActiveEffectByName('Logical operators')
  effect = segmentEditorWidget.activeEffect()
  segmentEditorNode.SetSelectedSegmentID(bafflename)######perform operations
  effect.setParameter("Operation", "SUBTRACT")
  effect.setParameter("ModifierSegmentID", skullname)#subtract this selection
  effect.self().onApply()
  #remove segment editor connection
  segmentEditorWidget = None
  slicer.mrmlScene.RemoveNode(segmentEditorNode)


def smooth(mm):
  """
  Smooth the baffle (the second segment) using median smoothing. Takes an argument in mm.
  """
  masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')
  segmentationNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLSegmentationNode')
  segmentationNode.CreateDefaultDisplayNodes() # only needed for display
  segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
  # Create segment editor to get access to effects
  segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
  segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
  segmentEditorWidget.setSegmentationNode(segmentationNode)
  segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)
  #getnames of segments in segmentation
  bafflename = segmentationNode.GetSegmentation().GetNthSegment(1).GetName()#get name of baffle
  skullname = segmentationNode.GetSegmentation().GetNthSegment(0).GetName()#get name of skull
  ##run Smoothing
  segmentEditorWidget.setActiveEffectByName("Smoothing")
  effect = segmentEditorWidget.activeEffect()
  segmentEditorNode.SetSelectedSegmentID(bafflename)
  effect.setParameter("SmoothingMethod", "MEDIAN")
  effect.setParameter("KernelSizeMm", mm)
  effect.self().onApply()
  #remove segment editor connection
  segmentEditorWidget = None
  slicer.mrmlScene.RemoveNode(segmentEditorNode)


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

def modelToSeg():
  """
  Converts model and baffle to segmentations. Takes the first and second models in the scene (besides from the 3 slice models already present in the 
  scene by default). Skull should be the first model, baffle the second.
  """
  modelskull = slicer.mrmlScene.GetNthNodeByClass(3, 'vtkMRMLModelNode')
  modelbaffle = slicer.mrmlScene.GetNthNodeByClass(4, 'vtkMRMLModelNode')
  # Import the model into the segmentation node
  slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelskull, segmentationNode)
  slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modelbaffle, segmentationNode)


def seg_to_obj(path, segmentationNode):
  """
  Convert baffle to obj. Converts the second segmentation. Takes as arguments the name of the segmentation("Segmentation" by default), and saves an obj file as the name of the segmentation .
  Example usage: seg_to_obj("c:/tmp", "Segmentation")
  """
  segmentationNode = getNode(segmentationNode)
  bafflename = segmentationNode.GetSegmentation().GetNthSegment(1).GetName()#get name of baffle
  segmentIds = vtk.vtkStringArray()
  segmentIds.InsertNextValue(bafflename)
  # Write to STL file
  slicer.vtkSlicerSegmentationsModuleLogic.ExportSegmentsClosedSurfaceRepresentationToFiles(path, segmentationNode, segmentIds, "OBJ")

