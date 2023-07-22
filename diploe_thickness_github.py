import os
import SimpleITK as sitk
import sitkUtils
import time

#threshold settings
thresholdskull_lwr = 333
thresholddiploe_lwr = 95
thresholddiploe_uppr = 1000

class diploeprocess():

  #Go to Segment editor
  #“Add” new Segment called “skull” and change color to “Bone”
  #“Add” a second segment, rename “diploe”, and change color to “Cartilage”
  def connect(self):
    """
    Connects the segmentation and volume nodes together in preparation for subsequent functions. Adds a segmentation node to the scene
    """
    global masterVolumeNode
    global segmentationNode
    global segmentEditorNode
    global segmentEditorWidget
    #Connect the volumes and segmentation to allow programatic access to model-segmentation conversion and segmentation effects
    masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')#detects the first scalar volume
  
    numseg = len(slicer.util.getNodesByClass('vtkMRMLSegmentationNode'))#number of segmentations in scene
    if numseg == 0:
      print("new segmentation created")
      segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
      segmentationNode.CreateDefaultDisplayNodes() # only needed for display
      segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
      segmentationNode.GetSegmentation().AddEmptySegment("skull")
      segmentationNode.GetSegmentation().AddEmptySegment("diploe")
    else:
      print("Segment effect widget connected to first segmentation in scene")
      segmentationNode = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
      segmentationNode.CreateDefaultDisplayNodes() # only needed for display
      segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    # Create segment editor to get access to effects
    segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
    # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
    segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
    segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
    segmentEditorWidget.setSegmentationNode(segmentationNode)
    segmentEditorWidget.setSourceVolumeNode(masterVolumeNode)
    segmentationNode.GetSegmentation().GetSegment('skull').SetColor(0.9450980392156862, 0.8392156862745098, 0.5686274509803921)  # color should be set in segmentation node
    segmentationNode.GetSegmentation().GetSegment('diploe').SetColor(0.43529411764705883, 0.7215686274509804, 0.8235294117647058)
  
  #Threshold “skull” using the range 333-max (max is ~2916 for the sample volume I will send, most range from 2900-3100) and Apply
  #threshold
  def skull_thresh(self):
    """
    threshold skull at 333-max
    """
    global volumeScalarRange
    volumeScalarRange= masterVolumeNode.GetImageData().GetScalarRange()#get scalar range so max value is used
    segmentEditorWidget.setActiveEffectByName('Threshold')
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID('skull')
    effect.setParameter("MinimumThreshold", str(thresholdskull_lwr))#lo
    effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
    effect.self().onApply()
    print(f'skull segment threshold at {thresholdskull_lwr}-{volumeScalarRange[1]}(lower-upper)')
  
  #Keep Largest Island and Apply everywhere, overwrite all
  
  def keeplargestisland(self):
      """
      keep largest island, overwrite all
      """
      segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteAllSegments)
      #run keep largest island on thresholded columella
      segmentEditorWidget.setActiveEffectByName("Islands")
      effect = segmentEditorWidget.activeEffect()
      segmentEditorNode.SetSelectedSegmentID('skull')
      effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
      effect.self().onApply()#apply separate
  
  #Smoothing —> Closing (fill holes) 3mm everywhere, overwrite all, Apply
  def smooth_close_holes(self, mm): 
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteAllSegments)
    segmentEditorWidget.setActiveEffectByName("Smoothing")
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID('skull')
    effect.setParameter("SmoothingMethod", "MORPHOLOGICAL_CLOSING")
    effect.setParameter("KernelSizeMm", mm)
    effect.self().onApply()
    print(f'closing holes on "skulls" segment at kernel size of {mm}mm')
  
  #Smoothing —> Gaussian 1mm everywhere, overwrite all, Apply
  def smooth_gaussian(self, mm): 
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteAllSegments)
    segmentEditorWidget.setActiveEffectByName("Smoothing")
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID('skull')
    effect.setParameter("SmoothingMethod", "GAUSSIAN")
    effect.setParameter("GaussianStandardDeviationMm", mm)
    effect.self().onApply()
    print(f'gaussian smoothing run on "skulls" segment at standard deviation of {mm}mm')
  
  ####DIPLOE SEGMENTATION##########
  #Use the Logical Operators tool to make “diploe” a copy of “skull”
  def copy_skull(self): 
    segmentEditorWidget.setActiveEffectByName('Logical operators')
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID('diploe')
    effect.setParameter("Operation", "COPY")
    effect.setParameter("ModifierSegmentID", 'skull')#copy this selection
    effect.self().onApply()
    print('copy created from skull to diploe')
  
  #Threshold “diploe” using the range 95-1000
  #Editable area is “inside diploe”
  #Modify other segments: “Allow overlap”
  #Apply
  #threshold 
  #https://apidocs.slicer.org/master/vtkMRMLSegmentationNode_8h_source.html#l00159 mask mode reference
  
  def diploe_thresh(self):
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
    segmentEditorNode.SetMaskSegmentID('diploe')#editable area inside diploe
    segmentEditorNode.SetMaskMode(5)#slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment
    
    segmentEditorNode.SetSelectedSegmentID('diploe')
    segmentEditorWidget.setActiveEffectByName('Threshold')
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold", str(thresholddiploe_lwr))#lo
    effect.setParameter("MaximumThreshold",str(thresholddiploe_uppr))
    effect.self().onApply()
    print(f'skull segment threshold at {thresholddiploe_lwr}-{thresholddiploe_uppr}(lower-upper)')
  
  #Smoothing —> Gaussian 1mm inside diploe only, allow overlap, Apply
  def smooth_gaussian_diploe(self, mm): 
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
    segmentEditorWidget.setActiveEffectByName("Smoothing")
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID('diploe')
    effect.setParameter("SmoothingMethod", "GAUSSIAN")
    effect.setParameter("GaussianStandardDeviationMm", mm)
    effect.self().onApply()
    print(f'gaussian smoothing run on "diploe" segment at standard deviation of {mm}mm')
  
  def export_to_models(self):
    segmentationNode = getNode("Segmentation")
    self.shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    exportFolderItemId = self.shNode.CreateFolderItem(self.shNode.GetSceneItemID(), "Segments")
    slicer.modules.segmentations.logic().ExportAllSegmentsToModels(segmentationNode, exportFolderItemId)
  
  #- Export ONLY “diploe” segment as a labelmap
  def export_diploe(self):
    self.labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode','diploe_labelmap')
    ##make all segment non-visible except seg of interest
    segmentationNode.GetDisplayNode().SetAllSegmentsVisibility(0)#make all
    segmentationNode.GetDisplayNode().SetSegmentVisibility('diploe',1)
    slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode,  self.labelmapVolumeNode, masterVolumeNode)
  
  #######################2. Apply Simple Filter###########################
  #- Go to Filtering —> Simple Filters module
  #- Filter: BinaryThinningImageFilter
  #- input volume: Segmentation-label
  #- output volume: Create new volume
  #- Apply (on my computer this step takes the longest, around ~180s)
  def apply_binary_thinning(self):
    # Get input volume node
    self.inputVolumeNode_label =  slicer.util.getNode('diploe_labelmap')#the string here is what you have the labelmap named as
    # Create new volume node for output
    self.binarythinning_outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode", "BinaryThinningImageFilter Output")#second string is name you give it
    # Run filter
    inputImage = sitkUtils.PullVolumeFromSlicer(self.inputVolumeNode_label)
    filter = sitk.BinaryThinningImageFilter()
    outputImage = filter.Execute(inputImage)
    sitkUtils.PushVolumeToSlicer(outputImage, self.binarythinning_outputVolumeNode)
    print('binary filter applied')
  
  #################################3. Apply Danielsson Filter###############################
  #- In the same module, change filter to DanielssonDistanceMapImageFilter
  #- input volume: BinaryThinningImageFilter Output
  #- output volume: Create new volume
  #- Check first box (“Input is binary”) and third box (“Use image spacing”)
  #- Apply
  #############################Create a distance map from the medial surface using the DanielssonDistanceMapImageFilter ###############3
  ### with options Input is Binary = Yes and Use Image Spacing=Yes
  # Get input volume node
  def apply_danielsson_filter(self):
    self.inputVolumeNode_label =  slicer.util.getNode("BinaryThinningImageFilter Output")#the string here "binarythinning_filter" is what you are naming the labelmap
    # Create new volume node for output
    self.DanielssonDistanceMap_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "DanielssonDistanceMapImageFilter Output")#second string is name you give it
    # Run filter
    inputImage = sitkUtils.PullVolumeFromSlicer(self.inputVolumeNode_label)
    filter = sitk.DanielssonDistanceMapImageFilter()
    filter.InputIsBinaryOn()#input is binary,
    filter.SetUseImageSpacing(True)#use image spaceing
    outputImage = filter.Execute(inputImage)
    sitkUtils.PushVolumeToSlicer(outputImage, self.DanielssonDistanceMap_node)
    print('Danielsson filter applied')
  
  ###########################################4. Probe Volume with Model###########################
  #- Go to module Surface Models —> Probe Volume with Model
  #- input volume: DanielssonDistanceMapImageFilter Output
  #- input model: diploe
  #- output model: Create new Model as “distance_model”
  #- Output array name: NRRD Image
  #- Apply
  def createprobevoltomodel(self):
    """create texture on model  using CLI module"""
    # Set parameters
    parameters = {}
    parameters["InputVolume"] = getNode("DanielssonDistanceMapImageFilter Output")#input volume [image]
    parameters["InputModel"] = slicer.mrmlScene.GetNthNodeByClass(4,'vtkMRMLModelNode')#diplo should be second model (after 3 slice models)
    parameters["OutputArrayName"] = "NRRD Image"
    self.outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode","distance_model")
    parameters["OutputModel"] = self.outputModelNode
    
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
    return self.outputModelNode

#############################
#make a list of the sub-folders of the maindirectory (basedir)
dir_list = os.listdir(base_directory)#list contents of root directory
directories = [item for item in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, item))]#only select folders, not files

# make list of folder names saved as 'full_path'
full_path_folders = []
for folder in directories:
  joinedpth = os.path.join(base_directory, folder)
  full_path_folders.append(joinedpth)

#################loop folders, open volumes, process, and export mrb and individual data nodes to same folder as original volume #####33
for i in range(0,len(full_path_folders)):
  volinside = os.listdir(full_path_folders[i])
  volinside = [file for file in volinside if file.endswith('.nrrd')]#select only nrrd files
  #print(volinside[0])
  volpath = f'{full_path_folders[i]}\\{volinside[0]}'#get first nrrd file
  print(volpath)
  #load volume
  loadedVolumeNode = slicer.util.loadVolume(rf'{volpath}')
  print(f'loaded following volume: {volpath}')
  #instantiation of segmentation
  dp = diploeprocess()
  dp.connect()
  #skull segmentation
  dp.skull_thresh()
  dp.keeplargestisland()
  dp.smooth_close_holes(3)  
  dp.smooth_gaussian(1)  
  dp.keeplargestisland()
  #diploe segmentation
  dp.copy_skull()
  dp.diploe_thresh()
  dp.smooth_gaussian_diploe(1)
  #distancemodelling
  dp.export_to_models()#Export both “skull” and “diploe” as models
  dp.export_diploe()
  dp.apply_binary_thinning()
  dp.apply_danielsson_filter()
  dp.createprobevoltomodel()#run the function and generate the model
  #export
  sceneSaveFilename = os.path.dirname(volpath) + "/saved-scene-" + time.strftime("%Y%m%d-%H%M%S") + ".mrb"
  ################################### Save scene ########################
  if slicer.util.saveScene(sceneSaveFilename):
    logging.info("Scene saved to: {0}".format(sceneSaveFilename))
    print('Scene saved to mrb file')
  else:
    logging.error("Scene saving failed")
  ############################### export individual nodes ############################
  #- Color Table
  #- Segmentations.seg.nrrd
  #- skull.vtk
  #- diploe.vtk
  #- Segmentation-label.nrrd
  #- Segmentation-label Color Table
  #- BinaryThinningImageFilter Output.nrrd
  #- DanielssonDistanceMapImageFilter Output.nrrd
  #- distance_model.v
  slicer.util.exportNode(segmentationNode,os.path.dirname(volpath)+"\\Segmentations.seg.nrrd")#-
  slicer.util.exportNode(slicer.mrmlScene.GetNthNodeByClass(3,'vtkMRMLModelNode'),os.path.dirname(volpath)+"\\skull.vtk")#-
  slicer.util.exportNode(slicer.mrmlScene.GetNthNodeByClass(4,'vtkMRMLModelNode'),os.path.dirname(volpath)+"\\diploe.vtk")#-
  slicer.util.exportNode(dp.labelmapVolumeNode,os.path.dirname(volpath)+"\\Segmentation-label.nrrd")#-
  slicer.util.exportNode(slicer.util.getNode('diploe_labelmap_ColorTable'),os.path.dirname(volpath)+"\\Segmentation-label Color Table.ctbl")#-
  slicer.util.exportNode(dp.binarythinning_outputVolumeNode,os.path.dirname(volpath)+"\\BinaryThinningImageFilter Output.nrrd")#-
  slicer.util.exportNode(dp.DanielssonDistanceMap_node,os.path.dirname(volpath)+"\\DanielssonDistanceMapImageFilter Output.nrrd")#-
  slicer.util.exportNode(dp.outputModelNode,os.path.dirname(volpath)+"\\distance_model.vtk")#- 
  os.path.dirname(volpath)
  print(f'files exported to {full_path_folders[i]}')
  #clear the scene before opening the next volume (next iteration of the loop)
  slicer.mrmlScene.RemoveNode(segmentationNode)
  slicer.mrmlScene.RemoveNode(segmentEditorNode)
  slicer.mrmlScene.Clear(0)

