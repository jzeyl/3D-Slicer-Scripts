#This file loads a segmentation and a danielssondistance volume to create thickness maps for segments, and then saves to a file

#########SET 'base_directory', fileout and 'python file in slicer interpreter, and run exec()
#base_directory = r"C:\Users\jeffz\Desktop\p1\data\seg2thickness"
#fileout = r"C:\Users\jeffz\Desktop\p1\seg2thick_out.txt"
#pythonfile = r"C:\Users\jeffz\Desktop\p1\seg2thickness.py"
#exec(open(pythonfile).read())

#make a list of the sub-folders of the maindirectory (basedir)
dir_list = os.listdir(base_directory)#list contents of root directory
directories = [item for item in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, item))]#only select folders, not files
print(directories)

# make list of folder names saved as 'full_path'
full_path_folders = []
for folder in directories:
  joinedpth = os.path.join(base_directory, folder)
  full_path_folders.append(joinedpth)

#name of segmentation and distance volume filesto load
filename = "Segmentation.seg.nrrd"
distancevolume = "DanielssonDistanceMapImageFilter Output.nrrd"

#########FUNCTIONS############
def write_to_file(filename, value):
    """
    write a value to the results file
    """
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
      #parameters of CLI module
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

#Loop through patient folders
for i in range(0,len(directories)):
  innerfiles = os.listdir(full_path_folders[i])#list files inside each patient folder
  #print(innerfiles)
    #################load distancemap###################
  distfile = [file for file in innerfiles if file == distancevolume]#select only distance_m
  print(distfile)
  distpath = f'{full_path_folders[i]}\\{distfile[0]}'#get full path
  print(distpath)
  slicer.util.loadVolume(distpath)
    #################load segmentation file###################
  segfile = [file for file in innerfiles if file == filename]#select only distance_m
  print(segfile)
  segpath = f'{full_path_folders[i]}\\{segfile[0]}'#get full path
  print(segpath)
  slicer.util.loadSegmentation(segpath)
  write_to_file(fileout, directories[i]+',')#write name of the folder to file
  #export all segmentations to models
  segmentationNode = getNode("Segmentation")
  shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
  exportFolderItemId = shNode.CreateFolderItem(shNode.GetSceneItemID(), "Segments")
  slicer.modules.segmentations.logic().ExportAllSegmentsToModels(segmentationNode, exportFolderItemId)
  modellist = ["Occipital", "R_Parietal", "L_Parietal", "R_Frontal", "L_Frontal"]
  for l in modellist:
    mod = getNode(l)
    numpoints = mod.GetPolyData().GetNumberOfPoints()#inspect model for number of points
    if numpoints == 0:
      print(f'empty model {l}: {numpoints}')
      write_to_file(fileout,str(0)+',')#write '0' to file
    else:
      print(f'non-empty model {l}: {numpoints}')
      createprobevoltomodel(l,f'{l}_array')#probes model to distance volume, and save as an array
      getthickness(f'{l}_thickness',f'{l}_array')#getthickness() function writes mean thickness to file
  write_to_file(fileout, '\n')#add new line to file
  slicer.mrmlScene.Clear(0)#clear scent
