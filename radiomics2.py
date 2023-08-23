#rBatch-run radiomics module inside Slicer using a parameter file
#Usage: Set variables in slicer console according to local file paths and execute python file. For example:
#base_directory = r"C:\Users\urs\Desktop\hoedha_radiomics\test"
#paramfilepath = r"C:\urs\urs\Desktop\hoedha_radiomics\Params_radiomics.yaml"
#pythonfile = r"C:\Users\urs\Desktop\hoedha_radiomics\radiomics.py"
#exec(open(pythonfile).read())

import SlicerRadiomics
import re
import pandas as pd
import openpyxl
import os

################################SET PARAMETERS###########################################
#define regex patterns to find correct volumes in scene
pattern_T1C = r'^(?=.*(?:T1|t1|T1W))(?=.*CE)' #T1C works
pattern_ADC = r'^\d+:\s.*ADC.*' #works ADC
pattern_T1 = r'^\d+:\s(T1|t1|T1W)(?!.*CE)' #works T1
pattern_T2 = r'^\d+:\s(?!(.*FLAIR.*|.*dark-fluid.*))(T2|t2|T2W)'
pattern_FLAIR = r'^\d+:\s(FLAIR|.*dark-fluid.*)' #works FLAIR


################# Get a list of subfolders in the base directory####################
#'base_directory' path is set in the slicer python console
subfolders = [os.path.join(base_directory, folder) for folder in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, folder))]

# Print the full paths of the subfolders
print('Processing the following folders:') 
for folder in subfolders:
    print(folder)

##############################FUNCTIONS################################
#function to find first mrb files in each patient folder
def find_file_with_extension(directory, extension):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                return os.path.join(root, file)
    return None  # If no file with the given extension is found

##########################export table to csv##############################
def savecsvandxlsx(nodename,outname):
  result = getNode(nodename)
  rad_outputFilename = subfolders[Index]+'\\Tables\\'+outname+'.csv'   #TAKES i from index of mainloop!
  print(rad_outputFilename)
  delayDisplay("Export results to CSV file: "+rad_outputFilename,3000)
  slicer.util.exportNode(result,rad_outputFilename)
  # Read the csv file into a pandas DataFrame for export to xlsx
  df = pd.read_csv(rad_outputFilename, sep=',')
  excel_file_path =re.sub(r'\.csv$', '.xlsx', rad_outputFilename)# Define the Excel file path where you want to save the data
  # Write the DataFrame to an Excel file
  df.to_excel(excel_file_path, index=False) 
  os.remove(rad_outputFilename)#remove original csv file if desired

#savecsvandxlsx('ADC_radiomics','ADC_radiomics')

#################PROCESS ADC VOLUME - find volume using regex#################
def process_ADC():
  volnames_original = []
  #loop through names of volumes in original volume folder and test regex rules:
  children = vtk.vtkIdList()
  shNode.GetItemChildren(originalvols, children) # 
  for j in range(children.GetNumberOfIds()):
    child = children.GetId(j)
    #print(child)
    print(shNode.GetItemDataNode(child).GetName())# print items in folder
    volnames_original.append(shNode.GetItemDataNode(child).GetName())
  for k in range(0,len(volnames_original)):
    if re.search(pattern_ADC, volnames_original[k]):
      print(f'matched volume at {volnames_original[k]} ')
      refvol = getNode(volnames_original[k])#if match is found
    else:
      print('not target volume...')
  #################################RUN RADIOMICS for ADC Original######################33
  segmentation = getNode('Segmentation')
  table = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTableNode',f'{refvol.GetName()}_radiomics')
  print(f'applying radiomics to following volume: {refvol.GetName()}')
  delayDisplay(f"applying radiomics to following volume: {refvol.GetName()}")
  logic = SlicerRadiomics.SlicerRadiomicsLogic()
  logic.__init__()
  logic.runSync = True
  logic.runCLIWithParameterFile(refvol,segmentation,table,paramfilepath,callback=lambda: savecsvandxlsx(f'{refvol.GetName()}_radiomics','ADC_radiomics'))

##############RADIOMICS - coreg-skullstripped volumes- isolate relevent volume using regex###################
def process_coregskullstripped():
  volnames_skullstripped = []
  #loop through names of volumes in 'skullstripped' folder and test regex rules:
  children = vtk.vtkIdList()
  shNode.GetItemChildren(subjectItemID, children) # Add a third argument with value True for recursive query
  for L in range(children.GetNumberOfIds()):
    child = children.GetId(L)
    print(child)
    print(shNode.GetItemDataNode(child).GetName())# print items in folder
    volnames_skullstripped.append(shNode.GetItemDataNode(child).GetName())
  patterns_skullstripped = [pattern_FLAIR,pattern_T1,pattern_T2,pattern_T1C]#list of regext patterns to find volumes   #,pattern_T2
  #################3MAKE TABLES FOR RADIOMICS
  for pattern in patterns_skullstripped:#go through and match each of the patterns to obtain correct reference volume
    for M in range(0,len(volnames_skullstripped)):
      if re.search(pattern, volnames_skullstripped[M]):
         print(f'matched volume at {volnames_skullstripped[M]} ')
         refvol = getNode(volnames_skullstripped[M])#if match is found
         #skullstripvolnamelist.append(volnames_skullstripped[M])
         global table
         table = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTableNode',f'{volnames_skullstripped[M]}_radiomics' )
         logic = SlicerRadiomics.SlicerRadiomicsLogic()
         logic.__init__()
         logic.runSync = True
         logic.runCLIWithParameterFile(refvol,segmentation,table,paramfilepath, callback = exportskullstriptable)
         #tablenames.append(table.GetName())
      else:
         print('not target volume...')


#export tables from the coreg-skullstrip group
def exportskullstriptable():
  nm = table.GetName()
  if re.search(pattern_T1, nm):############export tables that match the correct 
      savecsvandxlsx(nm,'T1_radiomics')
      print(f'exported {nm} as T1_radiomics')
  elif re.search(pattern_T2, nm):
      savecsvandxlsx(nm,'T2_radiomics')
      print(f'exported {nm} as T2_radiomics')
  elif re.search(pattern_FLAIR, nm):
      savecsvandxlsx(nm,'FLAIR_radiomics')
      print(f'exported {nm} as FLAIR_radiomics')
  elif re.search(pattern_T1C, nm):
      savecsvandxlsx(nm,'T1C_radiomics')
      print(f'exported {nm} as T1C_radiomics')
  else:
      print("No match")

##############################LOOP THROUGH PATIENT FILES#############
def mainloop():
  for i in range(0,len(subfolders)):
    global Index
    Index = i #used in savecsvandxlsx() function
    # Construct the complete path to the new subfolder
    table_folder = os.path.join(subfolders[i], "Tables")
    # Create the subfolder
    if not os.path.exists(table_folder):
      os.mkdir(table_folder)
    #find_first mrb file
    scenefile = find_file_with_extension(subfolders[i],'mrb')
    print(f'searching for scene file in {subfolders[i]}')
    #print(i)
    print(f'opening scenefile: {scenefile}')
    #load scene file
    slicer.util.loadScene(scenefile)
    print(f'opened {scenefile}')
    ###################################################Segment statistics export#####################################################################
    import SegmentStatistics
    segmentationNode = getNode('Segmentation')
    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
    segStatLogic.computeStatistics()
    #stats = segStatLogic.getStatistics()
    resultsTableNode = slicer.vtkMRMLTableNode()
    slicer.mrmlScene.AddNode(resultsTableNode)
    resultsTableNode.SetName('Segment_statistics')
    segStatLogic.exportToTable(resultsTableNode)
    segStatLogic.showTable(resultsTableNode)
    outputFilename = subfolders[i]+'\\Tables\\'+'CalcVolumes.csv'
    delayDisplay("Export results to CSV file: "+outputFilename)
    segStatLogic.exportToCSVFile(outputFilename)
    # Read the csv file into a pandas DataFrame
    df = pd.read_csv(outputFilename, sep=',')
    excel_file_path =re.sub(r'\.csv$', '.xlsx', outputFilename)# Define the Excel file path where you want to save the data
    # Write the DataFrame to an Excel file
    df.to_excel(excel_file_path, index=False)  # Set index=False if you don't want to save the row indices
    os.remove(outputFilename)#remove original csv file if desired
    ################RADIOMICS##########################################################################################
    #For Radiomics: We will employ the "Radiomics" module.
    #Input Image Volumes are as follows:
    #a. Original ADC
    #b. Coregistered-skullstripped T1
    #c. Coregistered-skullstripped T2
    #d. Coregistered-skullstripped FLAIR
    #e. Coregistered-skullstripped T1C
    #access segmentation node (should be the only segmentation, named 'Segmentation' across all mrb files)
    global segmentation
    segmentation = getNode('Segmentation')
    ##################access folder hierarchy###############################
    global shNode
    shNode = slicer.mrmlScene.GetSubjectHierarchyNode()
    # Get folder named 'skullstripped'
    global sceneItemID
    sceneItemID = shNode.GetSceneItemID()
    global subjectItemID
    subjectItemID = shNode.GetItemChildWithName(sceneItemID, "skullstripped")#################coreg-skullstripped volumes
    #for access to original ADC:
    global levelunderscened
    levelunderscened = shNode.GetItemByPositionUnderParent(sceneItemID,0)
    global originalvols
    originalvols = shNode.GetItemByPositionUnderParent(levelunderscened,0)######################original volumes
    process_ADC()
    process_coregskullstripped()
    sceneSaveFilename = subfolders[i] + "\\saved-scene-AIAA segmentation_Tables" + time.strftime("%Y%m%d-%H%M%S") + ".mrb"
    if slicer.util.saveScene(sceneSaveFilename):
      logging.info("Scene saved to: {0}".format(sceneSaveFilename))
      print(f'scene file exported: {sceneSaveFilename}')
    else:
      logging.error("Scene saving failed")
    os.remove(scenefile)
    slicer.mrmlScene.Clear (0)#clear scene
    del Index


mainloop()






