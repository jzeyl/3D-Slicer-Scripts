import os
import time
import re

#function to find mrb files in each patient folder
def find_file_with_extension(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                return os.path.join(root, file)
    return None  # If no file with the given extension is found


#connect to segmentation node, editor, set reference volume ('refvol' object, which will be based on regex rules)
def connect():
  """
  Connects the segmentation and volume nodes together in preparation for subsequent functions. Adds a segmentation node to the scene
  """
  #global masterVolumeNode
  global segmentationNode
  global segmentEditorNode
  global segmentEditorWidget
  #Connect the volumes and segmentation to allow programatic access to model-segmentation conversion and segmentation effects
  #masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(index, 'vtkMRMLScalarVolumeNode')#detects the first scalar volume
  numseg = len(slicer.util.getNodesByClass('vtkMRMLSegmentationNode'))#number of segmentations in scene
  if numseg == 0:
    print("nosegmentation present")
  else:
    print("Segment effect widget connected to first segmentation in scene")
    segmentationNode = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
    segmentationNode.CreateDefaultDisplayNodes() # only needed for display
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(refvol)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  # Create segment editor to get access to effects
  segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
  # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
  segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
  segmentEditorWidget.setSegmentationNode(segmentationNode)
  #segmentEditorWidget.setSourceVolumeNode(masterVolumeNode)

################# Get a list of subfolders in the base directory####################
#'base_directory' path is set in the slicer python console
subfolders = [os.path.join(base_directory, folder) for folder in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, folder))]

# Print the full paths of the subfolders
print('Processing the following folders:') 
for folder in subfolders:
    print(folder)

################Run processing on each patient folder####################
for i in range(0,len(subfolders)):
  #find_first mrb file
  scenefile = find_file_with_extension(subfolders[i],'mrb')
  print(f'searching for scene file in {subfolders[i]}')
  #print(i)
  print(f'opening scenefile: {scenefile}')
  #load scene file
  slicer.util.loadScene(scenefile)
  #access skullstripped folder
  shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
  # Get folder named 'skullstripped'
  sceneItemID = shNode.GetSceneItemID()
  subjectItemID = shNode.GetItemChildWithName(sceneItemID, "skullstripped")
  #isolate relevent volume using regex
  volnames_skullstripped = []
  pattern_T1C = r'^(?=.*(?:T1|t1|T1W))(?=.*CE)' #T1C works
  #loop through names of volumes in 'skullstripped' folder and test regex rules:
  children = vtk.vtkIdList()
  shNode.GetItemChildren(subjectItemID, children) # Add a third argument with value True for recursive query
  for j in range(children.GetNumberOfIds()):
    child = children.GetId(j)
    #print(child)
    print(shNode.GetItemDataNode(child).GetName())
    volnames_skullstripped.append(shNode.GetItemDataNode(child).GetName())
  for k in range(0,len(volnames_skullstripped)):
    if re.search(pattern_T1C, volnames_skullstripped[k]):
       print(f'matched volume at {volnames_skullstripped[k]} ')
       refvol = getNode(volnames_skullstripped[k])
    else:
       print('not target volume')
  
  #set model
  aiaaModelName ="clara_pt_brain_mri_segmentation_t1c"
  connect()#connect to segmentation to apply editor effects
  
  # Run Nvidia AIAA automated
  segmentEditorWidget.setActiveEffectByName("Nvidia AIAA")
  effect = segmentEditorWidget.activeEffect()
  effect.self().ui.segmentationModelSelector.currentText = aiaaModelName#apply model to settings
  effect.self().onClickSegmentation()#run automatic segmentation
  segmentationNode.CreateClosedSurfaceRepresentation() #show in 3D view
  lastsegindex = segmentationNode.GetSegmentation().GetNumberOfSegments()-1

  segmentationNode.GetSegmentation().GetNthSegment(lastsegindex).SetName('Tumor Mask')
  print('tumor segmentation created')
  
  #remove 3 empty markup nodes which were automatically generated as part of the AIAA function 
  slicer.mrmlScene.RemoveNode(getNode('A'))
  slicer.mrmlScene.RemoveNode(getNode('P'))
  slicer.mrmlScene.RemoveNode(getNode('N'))
  
  #naming for mrb file to be exported
  sceneSaveFilename = subfolders[i] + "\\saved-scene-AIAA segmentation_" + time.strftime("%Y%m%d-%H%M%S") + ".mrb"
  
  #save mrb file and log
  if slicer.util.saveScene(sceneSaveFilename):
    logging.info("Scene saved to: {0}".format(sceneSaveFilename))
    print('scene file exported')
  else:
    logging.error("Scene saving failed")
  
  #save export
  slicer.util.exportNode(segmentationNode, f'{subfolders[i]}\\{time.strftime("%Y%m%d-%H%M%S")}_segmentation_tumor_mask.seg.nrrd')
  
  #delete old mrb file
  try:
    os.remove(scenefile)
    print(f"File '{scenefile}' (pre-AIAA) has been deleted.")
  except OSError as e:
    print(f"Error occurred while deleting the file: {e}")
  
  #clear scene before next mrb file will be loaded
  slicer.mrmlScene.Clear(0)