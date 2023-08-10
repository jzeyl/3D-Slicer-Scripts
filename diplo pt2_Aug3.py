#########For each patient folder, the script looks for the 'diploe.vtk' and the 'DanielssonDistanceMapImageFilter Output.nrrd' 
#files, loads them, loads the markup planes, runs the cuts.
#Each model is then 'cleaned' (surface toolbox module) to remove unused points. 
#If there are no points in the model, script writes a zero to the results file, otherwise if there are points in the model, 
#it uses probevolume with model to get the thickness map, then extracts the array data for the thickness map and writes 
#the mean of the array to the file. Script uses the name of the folder to write each patient to file.
#*This is medial thickness (i.e. no adjustment from the last script), so to get total thickness you would multiply by 2*. 
#Segmentation with all cuts and the whole 'diploe' are saved to the same folder as 'Segmentation.nrrd' 
#

#base_directory = r"C:\Users\jeffz\Desktop\p1\data" #(root folder with patient subfolders inside)
##fileout = r"C:\Users\jeffz\Desktop\p1\thicknessout.txt"
#
##base_directory = r"C:\Users\jeffz\Desktop\jesse_slicer_automation\data"
#fileout = r"C:\Users\jeffz\Desktop\out.txt"
#
#################load markups#################3
#markupfolder = r"C:\Users\jeffz\Desktop\p1\Grid_Planes"
gridplanefiles = os.listdir(markupfolder)


#make a list of the sub-folders of the maindirectory (basedir)
dir_list = os.listdir(base_directory)#list contents of root directory
directories = [item for item in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, item))]#only select folders, not files
print(directories)

# make list of folder names saved as 'full_path'
full_path_folders = []
for folder in directories:
  joinedpth = os.path.join(base_directory, folder)
  full_path_folders.append(joinedpth)

#load file called 'distancd_model.vtk' and 
filename = "diploe.vtk"
danielssondistance = "DanielssonDistanceMapImageFilter Output.nrrd"

  ##make models not-visiible

    #
  #slicer.util.exportNode(segmentationNode,full_path_folders[i]+"\\Segmentation.seg.nrrd")#-
  
modelnodes = getNodesByClass('vtkMRMLModelNode')
for m in range(0,len(modelnodes)):
  modelnodes[m].SetDisplayVisibility(0)



def cleanmodel(inputmodel,outputmodel):
  logic = slicer.util.getModuleLogic('SurfaceToolbox')
  logic.clean(getNode(inputmodel),getNode(outputmodel))

#slice function
def slicemodel(modelnodename,planenodename,positivemodel=None,negativemodel=None):
  """
  Use dynamicmodeler to slice a model. specify model, plane node, and positive and negativemodels
  """
  dynamicModelerNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLDynamicModelerNode")
  dynamicModelerNode.SetToolName("Plane cut")
  model_node = getNode(modelnodename)
  plane_node = getNode(planenodename)
  dynamicModelerNode.SetNodeReferenceID("PlaneCut.InputModel", model_node.GetID())
  dynamicModelerNode.SetNodeReferenceID("PlaneCut.InputPlane", plane_node.GetID())
  
  if positivemodel == None:
    print('no positive model')
  else:
    try:#try to find existing node with same name
      posmodelexisting = getNode(positivemodel)
      newmodel = posmodelexisting
      print(f'used existing model: {newmodel.GetName()}')
    except: #if not found, create new model with that name
      newmodel = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode",positivemodel)
    dynamicModelerNode.SetNodeReferenceID("PlaneCut.OutputPositiveModel", newmodel.GetID())#setpositive model
  if negativemodel == None:
    print('no negative model')  
  else:
    try:#try to find existing node with same name
      negmodelexisting = getNode(negativemodel)
      newmodel = negmodelexisting
      print(f'used existing model: {newmodel.GetName()}')
    except: #if not found, create new model with that name
      newmodel = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode",negativemodel)
    dynamicModelerNode.SetNodeReferenceID("PlaneCut.OutputNegativeModel", newmodel.GetID())#set negative if reauired
  slicer.modules.dynamicmodeler.logic().RunDynamicModelerTool(dynamicModelerNode)
  print(f'Slice complete. model: {str(modelnodename)}, plane: {str(planenodename)}, positive model: {str(positivemodel)}, negative model: {str(negativemodel)}')

def write_to_file(filename, value):
    try:
        with open(filename, 'a') as file:
            # Write the formatted string to the file
            file.write(str(value))  # 
        print(f"Data written successfully to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def createprobevoltomodel(model,outputarrayname):
    """create texture on model  using CLI module"""
    # Set parameters
    parameters = {}
    parameters["InputVolume"] = getNode("DanielssonDistanceMapImageFilter Output")#input volume [image]
    parameters["InputModel"] = getNode(model)
    parameters["OutputArrayName"] = outputarrayname
    outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode",f'{model}_thickness')
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

#createprobevoltomodel('1_1','1_1_array')

def getthickness(gridsection,outputarrayname):
  """
  get thickness values from a model that has previously been probed with the distance volume. Saves to the result file
  """
  gridsectionnode = getNode(gridsection)
  ddist_array = slicer.util.arrayFromModelPointData(gridsectionnode, outputarrayname) 
  distmax = ddist_array.max() 
  thickness_mean = ddist_array.mean() 
  gridsectionname = gridsectionnode.GetName()
  print(f'gridsection: {gridsectionname}')
  print(f'model arraylength: {ddist_array.shape[0]}')
  print(f'max thickness is {distmax}')
  print(f'mean thickness is {thickness_mean}')
  write_to_file(fileout, f'{thickness_mean},')#write mean to file ##########{gridsection},  
  #del gridsectionnode,ddist_array,distmax,thickness_mean,gridsectionname


def allcuts():
  """
  cut the diploe into 18 sections
  """
  slicemodel('diploe','Frankfort_line','Frankfort_positive',None)
  slicemodel('Frankfort_positive','Coronal_plane_center',None,'Coronal_Negative')
  slicemodel('Coronal_Negative','Coronal_plane_P1','strip_3',None)
  slicemodel('Coronal_Negative','Coronal_plane_P1',None,'Coronal_Negative')
  
  slicemodel('Coronal_Negative','Coronal_plane_P2','strip_2',None)
  slicemodel('Coronal_Negative','Coronal_plane_P2',None,'strip_1')
  #— delete model “Coronal_negative” — 
  slicer.mrmlScene.RemoveNode(getNode('Coronal_Negative'))
  ##############################################STRIP 3#############
  slicemodel('strip_3','Sagittal_plane_R2',None,'1_3')
  slicemodel('strip_3','Sagittal_plane_R2','strip_3_positive',None)
  
  slicemodel('strip_3_positive','Sagittal_plane_R1',None,'2_3')
  slicemodel('strip_3_positive','Sagittal_plane_R1','strip_3_positive',None)
  
  slicemodel('strip_3_positive','Sagittal_plane_center',None,'3_3')
  slicemodel('strip_3_positive','Sagittal_plane_center','strip_3_positive',None)
  
  slicemodel('strip_3_positive','Sagittal_plane_L1',None,'4_3')
  slicemodel('strip_3_positive','Sagittal_plane_L1','strip_3_positive',None)
  
  
  slicemodel('strip_3_positive','Sagittal_plane_L2','6_3',None)
  slicemodel('strip_3_positive','Sagittal_plane_L2',None,'5_3')
  #— delete strip_3_positive — 
  slicer.mrmlScene.RemoveNode(getNode('strip_3_positive'))
  #— delete strip_3 — 
  #slicer.mrmlScene.RemoveNode(getNode('strip_3'))
  #################################################Strip 2: ########################################
  slicemodel('strip_2','Sagittal_plane_R2','strip_2_positive',None)
  slicemodel('strip_2','Sagittal_plane_R2',None,'1_2')
  
  slicemodel('strip_2_positive','Sagittal_plane_R1',None,'2_2')
  slicemodel('strip_2_positive','Sagittal_plane_R1','strip_2_positive',None)
  
  slicemodel('strip_2_positive','Sagittal_plane_center',None,'3_2')
  slicemodel('strip_2_positive','Sagittal_plane_center','strip_2_positive',None)
  
  slicemodel('strip_2_positive','Sagittal_plane_L1',None,'4_2')
  slicemodel('strip_2_positive','Sagittal_plane_L1','strip_2_positive',None)
  
  slicemodel('strip_2_positive','Sagittal_plane_L2',None,'5_2')
  slicemodel('strip_2_positive','Sagittal_plane_L2','6_2',None)
  
  #— delete strip_2_positive — 
  slicer.mrmlScene.RemoveNode(getNode('strip_2_positive'))
  #— delete strip_2 — 
  #slicer.mrmlScene.RemoveNode(getNode('strip_2'))
  slicemodel('strip_1','Sagittal_plane_R2','strip_1_positive',None)
  slicemodel('strip_1','Sagittal_plane_R2',None,'1_1')
  
  slicemodel('strip_1_positive','Sagittal_plane_R1',None,'2_1')
  slicemodel('strip_1_positive','Sagittal_plane_R1','strip_1_positive',None)
  
  slicemodel('strip_1_positive','Sagittal_plane_center',None,'3_1')
  slicemodel('strip_1_positive','Sagittal_plane_center','strip_1_positive',None)
  
  slicemodel('strip_1_positive','Sagittal_plane_L1',None,'4_1')
  slicemodel('strip_1_positive','Sagittal_plane_L1','strip_1_positive',None)
  
  slicemodel('strip_1_positive','Sagittal_plane_L2',None,'5_1')
  slicemodel('strip_1_positive','Sagittal_plane_L2','6_1',None)
  
  #— delete strip_1_positive — 
  slicer.mrmlScene.RemoveNode(getNode('strip_1_positive'))
  #— delete strip_1 — 
  #slicer.mrmlScene.RemoveNode(getNode('strip_1'))

def connect():
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
    #segmentationNode.GetSegmentation().AddEmptySegment("skull")
    #segmentationNode.GetSegmentation().AddEmptySegment("diploe")

def modtoseg(modname):
  """
  convert model to segmentation
  """
  modnode = getNode(modname)
  slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modnode, segmentationNode)


#Loop through patient folders
for i in range(0,len(directories)):
  innerfiles = os.listdir(full_path_folders[i])
  #################load diploe.vtk###################
  diploe = [file for file in innerfiles if file == filename]#select only distance_m
  print(diploe)
  diploepath = f'{full_path_folders[i]}\\{diploe[0]}'#get full path
  print(diploepath)
  slicer.util.loadModel(diploepath)
  ####################load distance volume###################3
  danielsson = [file for file in innerfiles if file == danielssondistance]#select only distance_m
  print(danielsson)
  danielssonpath = f'{full_path_folders[i]}\\{danielsson[0]}'#get first nrrd file
  print(danielssonpath)
  slicer.util.loadVolume(danielssonpath)
  print(directories[i])
  write_to_file(fileout, directories[i]+',')#write name of the folder to file

  ################load markups################
  for j in range(0,len(gridplanefiles)):
    e = slicer.util.loadMarkups(markupfolder+'\\'+gridplanefiles[j])
    e.SetDisplayVisibility(0)
  #cut diploe into 18 sections
  allcuts()
  ####################clean all models############################
  modellist = ['1_1','2_1','3_1','4_1','5_1','6_1','1_2','2_2','3_2','4_2','5_2','6_2','1_3','2_3','3_3','4_3','5_3','6_3']
  
  for k in modellist:#clean all models, remove points not in cells, since plane cut keeps unused points
    cleanmodel(k,k)
  ########################write to file##################333
  #if model has no points, then write to file '0', otherwise calculate the mean of the 
  for l in modellist:
    mod = getNode(l)
    numpoints = mod.GetPolyData().GetNumberOfPoints()#inspect model for number of points
    if numpoints == 0:
      print(f'empty model {l}: {numpoints}')
      write_to_file(fileout,str(0)+',')#write '0' to file
    else:
      print(f'non-empty model {l}: {numpoints}')
      createprobevoltomodel(l,f'{l}_array')#probes model to distance volume, and save as an array
      getthickness(f'{l}_thickness',f'{l}_array')#getthickness() funrction writes mean thickness to file
  
  modelnodes = getNodesByClass('vtkMRMLModelNode')#make models non-visible easier to isolate single sections 
  for m in range(0,len(modelnodes)):
    modelnodes[m].SetDisplayVisibility(0)
  #############################convert to segmentation##################33
  connect()#create segmentation 
  modtoseg('diploe')#add diploe model to segmentation
  for n in modellist:#add all grid sections to segmentation
    modtoseg(n)
  slicer.util.exportNode(segmentationNode,full_path_folders[i]+"\\Segmentation.seg.nrrd")#export segmentation
  write_to_file(fileout, '\n')#add new line to file
  slicer.mrmlScene.Clear(0)#clear scent

