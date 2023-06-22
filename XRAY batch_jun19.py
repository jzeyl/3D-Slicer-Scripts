import os
import pydicom
import numpy as np
from datetime import datetime
import cv2
import imageio


def getdirnames(directory):
  # Get a list of all .dcm files in the directory with their full paths
  global dir
  dir = directory
  global file_list
  file_list = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.dcm')]
  # Print the list of full file paths
  for file_path in file_list:
    print(file_path)
  global file_namesimple
  file_namesimple = []
  # Print only the filenames without extension
  for file_path in file_list:
    file_namesimple.append(os.path.splitext(os.path.basename(file_path))[0])

def runMedian(inputVolumeNode,neighborsize):
  """median filter on a volume. Volume node and size of pixels as inputs. Creates a new volume
  """
  # Set parameters
  parameters = {}
  parameters["neighborhood"] = [neighborsize,neighborsize,neighborsize]
  parameters["inputVolume"] = inputVolumeNode
  outputVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode', 'Median Filtered Volume')
  parameters["outputVolume"] = outputVolumeNode
  # Execute
  median_module = slicer.modules.medianimagefilter
  cliNode = slicer.cli.runSync(median_module, None, parameters)
  # Process results
  if cliNode.GetStatus() & cliNode.ErrorsMask:
    # error
    errorText = cliNode.GetErrorText()
    slicer.mrmlScene.RemoveNode(cliNode)
    raise ValueError("CLI execution failed: " + errorText)
  # success
  slicer.mrmlScene.RemoveNode(cliNode)
  return outputVolumeNode

def load_DICOM(path):
  """
  loads dicom from file path into slicer, saves as volume node
  """
  slicer.util.loadVolume(path)
  global pthh
  pthh = path
  global vol_original
  vol_original = slicer.mrmlScene.GetNthNodeByClass(0,'vtkMRMLScalarVolumeNode')


def savetoDICOM(savepath):
  """
  makes a copy of the original and modifies the PixelData and SOPInstanceUID
  """
  #get voxel data from modified volume (3rd one in the scene)
  volmod = slicer.mrmlScene.GetNthNodeByClass(2,'vtkMRMLScalarVolumeNode')
  voxels = slicer.util.arrayFromVolume(volmod)#get pixel data from modified volume 
  #read metadata from oroginal dicom
  original =pydicom.dcmread(pthh)
  #make copy of original
  global cpy
  cpy = original.copy()
  cpy.SOPInstanceUID = pydicom.uid.generate_uid()#generate new UID
  cpy.PixelData = voxels.tobytes()
  #cpy.save_as(savepath)
  #print(f'saving to {savepath}')

def connect():
  """
  Creates new segmentation for mask effects. Connects the segmentation and volume nodes together in preparation for subsequent functions. Adds a segmentation node to the scene
  """
  global masterVolumeNode
  global segmentationNode
  global segmentEditorNode
  global segmentEditorWidget
  #Connect the volumes and segmentation to allow programatic access to model-segmentation conversion and segmentation effects
  masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(1, 'vtkMRMLScalarVolumeNode')#detects the first scalar volume
  #numseg = len(slicer.util.getNodesByClass('vtkMRMLSegmentationNode'))#number of segmentations in scene
  segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode",'Seg_')
  segmentationNode.GetSegmentation().AddEmptySegment("mask")
  # Create a new segmentation display node
  global d
  d = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationDisplayNode")
  # Add it as a display node to the segmentation node
  segmentationNode.AddAndObserveDisplayNodeID(d.GetID())
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  # Create segment editor to get access to effects
  segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
  # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
  segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
  segmentEditorWidget.setSegmentationNode(segmentationNode)
  segmentEditorWidget.setSourceVolumeNode(masterVolumeNode)

def threshKI(target):
  """
  Applies the Kittle-Illingworth Automatic threshold (to be used for separating foreground/background)
  """
  volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()
  segmentEditorWidget.setActiveEffectByName("Threshold")
  effect = segmentEditorWidget.activeEffect()
  print(effect)
  segmentEditorNode.SetSelectedSegmentID(target)######perform operations
  effect.setParameter("MinimumThreshold", str(KI_val))
  effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
  effect.self().onApply()#apply effect
  segmentEditorWidget.setActiveEffect(None)#unselect effect

def keeplargestisland(target):
  ###
  # run keep 'largest island' effect to contain segmentation to largest object 
  ### 
  segmentEditorWidget.setActiveEffectByName("Islands")
  effect = segmentEditorWidget.activeEffect()
  segmentEditorNode.SetSelectedSegmentID(target)######perform operations
  effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
  effect.self().onApply()#apply separate
  segmentEditorWidget.setActiveEffect(None)

def mask(target):
  '''
  #run 'Mask volume' segmentation effect to remove background (i.e. all areas not contained in the segmentation
  #created preceding segmentation effects)
  '''
  segmentEditorWidget.setActiveEffectByName("Mask volume")
  effect = segmentEditorWidget.activeEffect()
  segmentEditorNode.SetSelectedSegmentID(target)######perform operations
  effect.setParameter("FillValue", str(0))#fill outside as 0
  effect.setParameter("Operation", "FILL_OUTSIDE")
  global maskedVolume
  maskedVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode", "Temporary masked volume")
  effect.self().outputVolumeSelector.setCurrentNode(maskedVolume)#set output volume
  #set input volume - alreaddy default segmentation
  effect.self().onApply()
  segmentEditorWidget.setActiveEffect(None)

#################################################################################################
#DRAW TEXT ON IMAGE ARRAY BEFORE
#################################################################################################

def add_text_to_image(image, text, location):
  ###
  #draw text on output png or jpg
  ###
  image_with_text = image.copy()
  font = cv2.FONT_HERSHEY_SIMPLEX
  mx = image.max()
  text_color = (int(mx))  # White color is set to the highest pixel value in the image
  text_thickness = 2
  text_size = cv2.getTextSize(text, font, 1, text_thickness)[0]
  padding = 10
  if location == 'T-R':
      org = (image.shape[1] - text_size[0] - padding, text_size[1] + padding)
  elif location == 'T-L':
      org = (padding, text_size[1] + padding)
  elif location == 'T-C':
      org = ((image.shape[1] - text_size[0]) // 2, text_size[1] + padding)
  elif location == 'B-R':
      org = (image.shape[1] - text_size[0] - padding, image.shape[0] - padding)
  elif location == 'B-L':
      org = (padding, image.shape[0] - padding)
  elif location == 'B-C':
      org = ((image.shape[1] - text_size[0]) // 2, image.shape[0] - padding)
  #print(location)
  #print(type(org))
  cv2.putText(image_with_text, text, org, font, 1, text_color, text_thickness, cv2.LINE_AA)
  return image_with_text

##########################RUN##############33


def imgprocess_single(filelocation,medfiltersize, imgtype,location):
  load_DICOM(filelocation)
  original = pydicom.dcmread(filelocation)
  original_image = original.pixel_array
  # 
  #cv2.imshow("Combined Image", combined_img)
  #cv2.waitKey(0)
  #cv2.destroyAllWindows()
  runMedian(vol_original,medfiltersize)
  #set automatic threshold for mask
  masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(1, 'vtkMRMLScalarVolumeNode')
  import vtkITK ###Get kittle-Illingworth threshold
  _thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
  _thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
  _thresholdCalculator.SetMethodToKittlerIllingworth()#autothreshold
  _thresholdCalculator.Update()
  global KI_val
  KI_val = _thresholdCalculator.GetThreshold()#the threshold value
  connect()
  threshKI('mask')
  keeplargestisland('mask')
  mask('mask')
  dcmname = os.path.splitext(os.path.basename(filelocation))[0]
  dcmfullpath = fr'{os.path.dirname(filelocation)}\\{dcmname}_median_filter_mask.dcm'
  print(f'saving file to {dcmfullpath}')
  savetoDICOM(fr'{os.path.dirname(filelocation)}\\{dcmname}_median_filter_mask.dcm')
  cpy.save_as(dcmfullpath)#save modified data to dicom
  #################################EXPORT#####################
  image_path = dcmfullpath#this is a newly generated file
  image_name = os.path.splitext(os.path.basename(image_path))[0]
  modimage = cpy.pixel_array 
  #get information about date created/date modified
  created_date = datetime.fromtimestamp(os.path.getctime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
  modified_date = datetime.fromtimestamp(os.path.getmtime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
  text = f'{image_name}, Created: {created_date}, Modified: {modified_date}'
  print(f"Created Date: {created_date}")
  print(f"Modified Date: {modified_date}")
  print(text)
  #output_image = add_text_to_image(cpy.pixel_array, text, 'T-L')
  ################## Combine the image arrays side by side###############################
  cmbotextout = f'{os.path.dirname(image_path)}\\{image_name}_combo.{imgtype}'
  print(f'saving DICOM with text to {cmbotextout}')
  combined_img = np.concatenate((original_image, modimage), axis=1)
  print(combined_img.shape)
  #add text
  output_image = add_text_to_image(combined_img, text, location)
  #pngtextout = f'{os.path.dirname(image_path)}\\{image_name}_end.png'
  #print(f'saving DICOM with text to {pngtextout}')
  if imgtype == 'png':
    imageio.imwrite(cmbotextout, output_image)
  # Convert the image to grayscale
  if imgtype == 'jpg':
      # Normalize the pixel values to the range of 0-255
      normalized_image = ((output_image - output_image.min()) * (255.0 / (output_image.max() - output_image.min()))).astype(np.uint8)
      # Save the normalized grayscale image as JPEG
      cv2.imwrite(cmbotextout, normalized_image)
  #####################write to png modified###############################
  #output_image = add_text_to_image(cpy.pixel_array, text, location)
  pngtextout = f'{os.path.dirname(image_path)}\\{image_name}_original.{imgtype}'
  print(f'saving DICOM with text to {pngtextout}')
  if imgtype == 'png':
    imageio.imwrite(pngtextout, original_image)
  if imgtype == 'jpg':
      # Normalize the pixel values to the range of 0-255
      normalized_image = ((original_image - original_image.min()) * (255.0 / (original_image.max() - original_image.min()))).astype(np.uint8)
      # Save the normalized grayscale image as JPEG
      cv2.imwrite(pngtextout, normalized_image)
  ##################################write original######################
  output_image = add_text_to_image(cpy.pixel_array, text, location)
  pngtextout = f'{os.path.dirname(image_path)}\\{image_name}_.{imgtype}'
  print(f'saving DICOM with text to {pngtextout}')
  if imgtype == 'png':
    imageio.imwrite(pngtextout, output_image)
  if imgtype == 'jpg':
      # Normalize the pixel values to the range of 0-255
      normalized_image = ((output_image - output_image.min()) * (255.0 / (output_image.max() - output_image.min()))).astype(np.uint8)
      # Save the normalized grayscale image as JPEG
      cv2.imwrite(pngtextout, normalized_image)
  #write to dicom
  cpy.PixelData = output_image.tobytes()
  dcmtextout = f'{os.path.dirname(image_path)}\\{image_name}_.dcm'
  print(f'saving DICOM with text to {dcmtextout}')
  cpy.save_as(dcmtextout)
  #remove DICOM with 
  os.remove(dcmfullpath)
  slicer.mrmlScene.Clear(0)


def imgprocess_batch(folder,medfiltersize,imgtype,location):
   getdirnames(folder) 
   for i in range(0,len(file_list)):
     imgprocess_single(file_list[i],parameters['medfiltersize'],parameters['imgtype'],parameters['location'])




