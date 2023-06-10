import HDBrainExtractionTool
import Elastix
import os
import DICOMLib.DICOMUtils as utils
import DICOMScalarVolumePlugin
import re

#define regex patterns
pattern_T1C = r'^(?=.*(?:T1|t1|T1W))(?=.*CE)' #T1C works
pattern_ADC = r'^\d+:\s.*ADC.*' #works ADC
pattern_T1 = r'^\d+:\s(T1|t1|T1W)(?!.*CE)' #works T1
pattern_T2 = r'^\d+:\s(T2|t2|T2W)' #works T2
pattern_FLAIR = r'^\d+:\s(FLAIR|.*dark-fluid.*)' #works FLAIR

def loaddicoms(base_dir):
  print(f'loading files from: {base_dir}')
  global loadedNodeIDs
  loadedNodeIDs = []  # this list will contain the list of all loaded node IDs
  from DICOMLib import DICOMUtils
  with DICOMUtils.TemporaryDICOMDatabase() as db:
    DICOMUtils.importDicom(base_dir, db)
    global patientUIDs
    patientUIDs = db.patients()
    for patientUID in patientUIDs:
      loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))

###########FOLDERS##############
def create_folders():
  global shNode
  shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
  global SceneID
  SceneID = shNode.GetSceneItemID()# get current SceneID
  global folder1
  folder1 = shNode.CreateFolderItem(SceneID, "coreg")# folder create
  global folder2
  folder2 = shNode.CreateFolderItem(SceneID, "skullstripped")

def run_elastix(fixedindex,movingindex):
  try:
    fixedvol = slicer.mrmlScene.GetNthNodeByClass(fixedindex,'vtkMRMLScalarVolumeNode')
    movingvol = slicer.mrmlScene.GetNthNodeByClass(movingindex,'vtkMRMLScalarVolumeNode')
    global v3
    v3 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode',f'{movingvol.GetName()}_coreg')
    shNode.CreateItem(folder1, v3)#put in folder
    parameterFilenm = Elastix.ElastixLogic().getRegistrationPresets()[1][5]
    #Above line uses generic rigid preset
    #to use other presets type the following into the python console to change as appropriate the number [1] above: 
    #show all presets:   Elastix.ElastixLogic().getRegistrationPresets()
    #show setting for first preset: Elastix.ElastixLogic().getRegistrationPresets()[1]
    #get the file associated with the preset(item 5 in the list)Elastix.ElastixLogic().getRegistrationPresets()[1][5]
    print(f'registering {movingvol.GetName()}(moving) with {fixedvol.GetName()}(fixed)')
    #run registration
    Elastix.ElastixLogic().registerVolumes(fixedvol,movingvol,outputVolumeNode = v3, parameterFilenames = parameterFilenm )
  except:
    print(f'Registration failed - check volume indices')

#earlier function using a list to specify volume order
#def run_elastix_multiple(queue):#queus is a list where first index is the fixed volume
#  for i in range(1,len(queue)):#start at 1 to skip first index
#    run_elastix(queue[0],queue[i])

def run_skullstrip(vol):
  global strippedvol
  strippedvol = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLScalarVolumeNode',f'{vol.GetName()} stripped')
  shNode.CreateItem(folder2, strippedvol)
  print('Processing skullstripping')
  HDBrainExtractionTool.HDBrainExtractionToolLogic().process(vol,strippedvol,outputSegmentation = None)

def run_skullstrip_multiple():
  children = vtk.vtkIdList()
  shNode.GetItemChildren(folder1, children) # Add a third argument with value True for recursive query
  for i in range(children.GetNumberOfIds()):
    child = children.GetId(i)
    #print(child)
    print(shNode.GetItemDataNode(child).GetName())#get
    global vol
    vol = shNode.GetItemDataNode(child)
    run_skullstrip(vol)
    #update GUI
    slicer.app.processEvents()

def add_segmentation():
  """
  Connects the segmentation. Adds a segmentation node to the scene
  """
  #global masterVolumeNode
  global segmentationNode
  numseg = len(slicer.util.getNodesByClass('vtkMRMLSegmentationNode'))#number of segmentations in scene
  if numseg == 0:
    print("new segmentation created")
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentationNode.CreateDefaultDisplayNodes() # only needed for display
    #segmentationNode.SetName(nm)
    vol = slicer.mrmlScene.GetNthNodeByClass(T1C_index,'vtkMRMLScalarVolumeNode')
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(vol)
    segmentationNode.GetSegmentation().AddEmptySegment("Total Tumor")
    segmentationNode.GetSegmentation().AddEmptySegment("Necrotic")
    segmentationNode.GetSegmentation().AddEmptySegment("Non-Enhancing Tumor")
    segmentationNode.GetSegmentation().AddEmptySegment("Enhancing Tumor")
    segmentationNode.GetSegmentation().AddEmptySegment("Edema")
    segmentationNode.GetSegmentation().AddEmptySegment("Tumor Core")

def export_skullstrip():
  children = vtk.vtkIdList()
  shNode.GetItemChildren(folder2, children) # Add a third argument with value True for recursive query
  for i in range(children.GetNumberOfIds()):
    child = children.GetId(i)
    #print(child)
    nm = shNode.GetItemDataNode(child).GetName().replace(":", "_")
    print(f'{nm} volume exported')#get 
    global vol
    vol = shNode.GetItemDataNode(child)
    slicer.util.exportNode(vol, f'{exportfolder}\\skullstripped\\{nm}.nii.gz')

def export_coreg():
  children = vtk.vtkIdList()
  shNode.GetItemChildren(folder1, children) # Add a third argument with value True for recursive query
  for i in range(children.GetNumberOfIds()):
    child = children.GetId(i)
    #print(child)
    nm = shNode.GetItemDataNode(child).GetName().replace(":", "_")
    print(f'{nm} volume exported')#get 
    global vol
    vol = shNode.GetItemDataNode(child)
    slicer.util.exportNode(vol, f'{exportfolder}\\coreg\\{nm}.nii.gz')


##set the argument for the folder path
#In slicer, assign the path to the main folder containing all the patient folders as 'basedir'. Then assign the
#file location of this python file.
#e.g.
#basedir = r'C:\Users\joe\Downloads\hoedha-attachments\unzip'
#pythonfile = r"C:\Users\joe\Desktop\elastix_skull_stripping\jun_6_skullstripping.py"
#
#Then, run this code by typing the following into the slicer console
#exec(open(pythonfile).read())

#make a list of the sub-folders of the maindirectory (basedir)
dir_list = os.listdir(basedir)
# Iterate over the these foldernames to get a list of the full folder paths
full_path = []
for folder in dir_list:
    joinedpth = os.path.join(basedir, folder)
    full_path.append(joinedpth)
    #print(full_path)


####################Loop through the patient folders
for i in range(0,len(full_path)):
  loaddicoms(full_path[i])
  volumes = getNodesByClass('vtkMRMLScalarVolumeNode')
  volumenames = []#get imported volume names
  for e in range(0,len(volumes)):
     volumenames.append(volumes[e].GetName())
  #loop through volume names and when matching, assign corresponding index
  for index, name in enumerate(volumenames):
    if re.search(pattern_ADC, name):
      global ADC_index
      ADC_index = index
      print(f'ADC volume is at index {ADC_index}')
    elif re.search(pattern_FLAIR, name):
      global FLAIR_index
      FLAIR_index = index
      print(f'Flair volume is at index {FLAIR_index}')
    elif re.search(pattern_T1, name):
      global T1_index
      T1_index = index
      print(f'T1 volume is at index {T1_index}')
    elif re.search(pattern_T2, name):
      global T2_index
      T2_index = index
      print(f'T2 volume is at index {T2_index}')
    elif re.search(pattern_T1C, name):
      global T1C_index
      T1C_index = index
      print(f'T1C volume is at index {T1C_index}')
    else:
      print(f'volume {name} does not match any of the regex rules')
  #create folders
  create_folders()
  #run registrations
  try:
    run_elastix(T1C_index,T1_index)
  except: 
    print('failed to run registration between T1C and T1. check volume indices')
  try:
    run_elastix(T1C_index,T2_index)
  except: 
    print('failed to run registration between T1C and T2. check volume indices')
  try:
    run_elastix(T1C_index,FLAIR_index)
  except: 
    print('failed to run registration between T1C and FLAIR. check volume indices')
  try:
    run_elastix(T1C_index,ADC_index)
  except:
    print('failed to run registration between T1C and ADC. check volume indices')
  #run skull-stripping
  print('skullstripping in progress...')
  #run on T1C
  try:
    run_skullstrip(slicer.mrmlScene.GetNthNodeByClass(T1C_index,'vtkMRMLScalarVolumeNode'))
  #run skull stripping on all coreg volumes
  except:
    print('failed to perform skull stripping on T1C. Check if "T1C_index" exists.')
  try:
    run_skullstrip_multiple()
  except:
    print("skullstripping of coreg volumes failed")
  #add pre-populated segmentation to the scene
  try:
    add_segmentation()
  except: 
    print('addition of segmentation failed')
  ####################EXPORT##################################################
  #setup folder location
  exportfolder = f'{full_path[i]}\\export'
  #make directories for volumes
  os.makedirs(exportfolder)
  os.makedirs(f'{exportfolder}\\coreg')
  os.makedirs(f'{exportfolder}\\skullstripped')
  os.makedirs(f'{exportfolder}\\segmentation')
  ##########export volumes in respective folders##############3
  export_skullstrip()
  print('skullstripping volumes exported')
  export_coreg()
  print('coreg volumes exported')
  #export segmentation
  seg1 = slicer.mrmlScene.GetNthNodeByClass(0,'vtkMRMLSegmentationNode')
  slicer.util.exportNode(seg1, f'{exportfolder}\\segmentation\\{seg1.GetName()}.seg.nrrd')
  print('segmentation exported')
  ################# Save scene #################
    # Generate file name
  import time
  sceneSaveFilename = full_path[i] + "\\saved-scene-" + time.strftime("%Y%m%d-%H%M%S") + ".mrb"
  
  if slicer.util.saveScene(sceneSaveFilename):
    logging.info("Scene saved to: {0}".format(sceneSaveFilename))
    print('scene file exported')
  else:
    logging.error("Scene saving failed")
  ######CLEAR SCENE and variables of current file before next iteration
  slicer.mrmlScene.Clear(0)
  del loadedNodeIDs
  del ADC_index
  del T1_index
  del T2_index
  del T1C_index
  del FLAIR_index









