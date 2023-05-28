volumeNode = slicer.mrmlScene.GetNthNodeByClass(0,'vtkMRMLScalarVolumeNode')
segmentationNode = slicer.mrmlScene.GetNthNodeByClass(0,'vtkMRMLSegmentationNode')



def makelabelmap():
  # Export segmentation to a labelmap
  global labelmapVolumeNode
  labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode','lblmap_volume')
  slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode, labelmapVolumeNode, volumeNode)
  global lblcount
  lblcount = 1

#center 3d view and slice views, to fill background
def reset_views():
    layoutManager = slicer.app.layoutManager()
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetFocalPoint()#just resets the focal point, camera might be tilted off still
    threeDView.resetCamera()#reset to snap to face on, anterior position
    #reset slice views
    for col in ["Red","Yellow","Green"]:
        slicer.app.layoutManager().sliceWidget(col).fitSliceToBackground()




def getROI(axis = 'red'):
  #get image dimensions and resolution to inform bounding box
  xboxdist = (volumeNode.GetImageData().GetBounds()[1]*volumeNode.GetSpacing()[0])
  yboxdist = (volumeNode.GetImageData().GetBounds()[3]*volumeNode.GetSpacing()[1])
  zboxdist = (volumeNode.GetImageData().GetBounds()[5]*volumeNode.GetSpacing()[2])
  xboxdistres = volumeNode.GetSpacing()[0]
  yboxdistres = volumeNode.GetSpacing()[1]
  zboxdistres = volumeNode.GetSpacing()[2]
  if axis == 'red': 
    redSliceNode = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed')
    sliceTransformMatrix = redSliceNode.GetSliceToRAS()
    roi = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsROINode', 'SliceExportROI_red')
    roiTransformMatrix = vtk.vtkMatrix4x4()
    roiTransformMatrix.DeepCopy(sliceTransformMatrix)
    roi.SetAndObserveObjectToNodeMatrix(roiTransformMatrix)
    roi.SetSize([xboxdist,yboxdist,zboxdistres])
  if axis == 'green':
    greenSliceNode = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeGreen')
    sliceTransformMatrix = greenSliceNode.GetSliceToRAS()
    roi = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsROINode', 'SliceExportROI_green')
    roiTransformMatrix = vtk.vtkMatrix4x4()
    roiTransformMatrix.DeepCopy(sliceTransformMatrix)
    roi.SetAndObserveObjectToNodeMatrix(roiTransformMatrix)
    roi.SetSize([xboxdist,zboxdist,yboxdistres])
  if axis == 'yellow':  
    yellowSliceNode = slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeYellow')
    sliceTransformMatrix = yellowSliceNode.GetSliceToRAS()
    roi = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsROINode', 'SliceExportROI_yellow')
    roiTransformMatrix = vtk.vtkMatrix4x4()
    roiTransformMatrix.DeepCopy(sliceTransformMatrix)
    roi.SetAndObserveObjectToNodeMatrix(roiTransformMatrix)
    roi.SetSize([yboxdist,zboxdist,xboxdistres])#off


def crop_original(axis = 'red'):
  reset_views()
  if axis == 'red':
    getROI('red')
    roi = getNode('SliceExportROI_red')
    nm = 'vol_slice_red'
    out = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode', nm)
  if axis == 'green':
    getROI('green')
    roi = getNode('SliceExportROI_green')
    nm = 'vol_slice_green'
    out =slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode', nm)
  if axis == 'yellow':
    getROI('yellow')
    roi = getNode('SliceExportROI_yellow')
    nm = 'vol_slice_yellow'
    out = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode', nm)
  #crop roi as new volume             
  cropLogic = slicer.modules.cropvolume.logic()
  cvpn = slicer.vtkMRMLCropVolumeParametersNode()
  cvpn.SetROINodeID(roi.GetID())
  cvpn.SetInputVolumeNodeID(volumeNode.GetID())
  cvpn.SetOutputVolumeNodeID(out.GetID())
  cropLogic.Apply(cvpn)
  slicer.mrmlScene.RemoveNode(roi)


  
  slicer.mrmlScene.RemoveNode(cvpn)
  return output_volume_node


#labelmapVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0,'vtkMRMLLabelMapVolumeNode')
def crop_labelmap(axis = 'red'):
  reset_views()
  if axis == 'red':
    getROI('red')
    roi = getNode('SliceExportROI_red')
    #nm = 'seg_slice_red'
    #out = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode', nm)
  if axis == 'green':
    getROI('green')
    roi = getNode('SliceExportROI_green')
    #nm = 'seg_slice_green'
    #out = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode', nm)
  if axis == 'yellow':
    getROI('yellow')
    roi = getNode('SliceExportROI_yellow')
    #nm = 'seg_slice_yellow'
    #out = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode', nm)
  #crop roi as new volume             
  cropLogic = slicer.modules.cropvolume.logic()
  cvpn = slicer.vtkMRMLCropVolumeParametersNode()
  cvpn.SetROINodeID(roi.GetID())
  cvpn.SetInputVolumeNodeID(labelmapVolumeNode.GetID())
  cropLogic.Apply(cvpn)
  slicer.mrmlScene.RemoveNode(roi)
  #slicer.mrmlScene.RemoveNode(labelmapVolumeNode)
  global lblcount
  lblcount = lblcount +1


def cropVolumeUsingROI(input_volume_node, roi_node, output_volume_node=None, 
        interpolation_mode='linear', fill_value=0, isotropic=True):
    """ Run Crop Volume using input ROI
    """
    cropVolumeNode = slicer.vtkMRMLCropVolumeParametersNode()
    cropVolumeNode.SetScene(slicer.mrmlScene)
    cropVolumeNode.SetName("MyCropVolumeParametersNode")
    cropVolumeNode.SetIsotropicResampling(isotropic)
    if interpolation_mode=='linear':
        interp_mode = cropVolumeNode.InterpolationLinear
    elif interpolation_mode=='nn':
        interp_mode = cropVolumeNode.InterpolationNearestNeighbor
    
    cropVolumeNode.SetInterpolationMode(interp_mode)
    
    cropVolumeNode.SetFillValue(fill_value)
    cropVolumeNode.SetROINodeID(roi_node.GetID())  # roi
    slicer.mrmlScene.AddNode(cropVolumeNode)
    if output_volume_node is None:
        output_volume_node = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode', input_volume_node.GetName() + '_roiCropped')
    
    cropVolumeNode.SetInputVolumeNodeID(input_volume_node.GetID())  # input
    cropVolumeNode.SetOutputVolumeNodeID(output_volume_node.GetID())  # output
    slicer.modules.cropvolume.logic().Apply(cropVolumeNode)  # do the crop
    slicer.mrmlScene.RemoveNode(cropVolumeNode)
    return output_volume_node

cropVolumeUsingROI(input_volume_node, roi_node, output_volume_node=None, 
        interpolation_mode='linear', fill_value=0, isotropic=True)












##########333
def pathFromNode(node):
  storageNode = node.GetStorageNode()
  if storageNode is not None: # loaded via drag-drop
    filepath = storageNode.GetFullNameFromFileName()
  else: # Loaded via DICOM browser
    instanceUIDs = node.GetAttribute('DICOM.instanceUIDs').split()
    filepath = slicer.dicomDatabase.fileForInstance(instanceUIDs[0])
  return filepath


#node = slicer.util.getNode("volume1")
path = pathFromNode(volumeNode)
print("DICOM path=%s" % path)


import os
outputFolder = os.path.dirname(path)


from pydicom import dcmread
ds = dcmread(path)

volumecrp = slicer.mrmlScene.GetNthNodeByClass(2,'vtkMRMLScalarVolumeNode')
labelcrp = slicer.mrmlScene.GetNthNodeByClass(1,'vtkMRMLLabelMapVolumeNode')

# Create patient and study and put the volume under the study
shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
# set IDs. Note: these IDs are not specifying DICOM tags, but only the names that appear in the hierarchy tree
#patientItemID = shNode.CreateSubjectItem(shNode.GetSceneItemID(), "test patient")
#studyItemID = shNode.CreateStudyItem(patientItemID, "test study")
volumeShItemID = shNode.GetItemByDataNode(volumecrp)
#shNode.SetItemParent(volumeShItemID, studyItemID)


import DICOMScalarVolumePlugin
exporter = DICOMScalarVolumePlugin.DICOMScalarVolumePluginClass()
exportables = exporter.examineForExport(volumeShItemID)
for exp in exportables:
  # set output folder
  exp.directory = outputFolder

exporter.export(exportables)


            for tagName, tagValue in tagDictionary.items():
                exp.setTag(tagName, tagValue)

#####################
count = 0
index = []

for i in range(0,len(ds.items())):
  elem = ds[list(ds.keys())[i]]#hexidecimal tak, all have them
  print(elem.keyword)#standard elements have keyword
  if elem.keyword != "":
    count += 1
  else:
    index.append(i)

print(str(count) + ' have keywords. empty at:')
print(index)


##########3
dc2 = dcmread(r"C:\Users\jeffz\Downloads\150-DF891791-G\150-DF891791-G\ScalarVolume_23\IMG0001.dcm")

#compare two dicom files
taginnew = []
tagmissing = []

for item in list(ds.keys()):
    if item in list(dc2.keys()):
        print(f"{item} tag is in new file")
        taginnew.append(item)
    else:
        print(f"{item} is not in new file")
        tagmissing.append(item)


dc2.save_as(r"C:\Users\jeffz\Downloads\150-DF891791-G\150-DF891791-G\ScalarVolume_23\IMG0001out.dcm")

dc3 = dcmread(r"C:\Users\jeffz\Downloads\150-DF891791-G\150-DF891791-G\ScalarVolume_23\IMG0001out.dcm")



#update exported DICOM
for i in taginnew:
  print(i)
  dc2[i].value = ds[i].value

dc2[tagmissing[0]]

from pydicom.datadict import dictionary_VR
try:
  dictionary_VR(tagmissing[20])
catch:
  






"C:\Users\jeffz\Downloads\150-DF891791-G\150-DF891791-G\ScalarVolume_31\IMG0001.dcm"

           directoryName = 'ScalarVolume_' + str(exportable.subjectHierarchyItemID)
            directoryDir = qt.QDir(exportable.directory)
            directoryDir.mkpath(directoryName)
            directoryDir.cd(directoryName)
            directory = directoryDir.absolutePath()
            logging.info("Export scalar volume '" + volumeNode.GetName() + "' to directory " + directory)