loadedNodeIDs = []  # this list will contain the list of all loaded node IDs


#Imports the necessary libraries and modules for loading DICOM files and creating a surface mesh from a volume node using CLI module.
import argparse
import DICOMLib.DICOMUtils as utils
import DICOMScalarVolumePlugin


#Create command line arguments using argparse module and then parses them using parse_args() method.
parser = argparse.ArgumentParser(description='Load dicom')
parser.add_argument('-f', '--folder', type=str, help='DICOM FOLDER PATH', required=True)
args = parser.parse_args()

#Use DICOMScalarVolumePlugin module to load the scalar volume reader.
from DICOMLib import DICOMUtils
with DICOMUtils.TemporaryDICOMDatabase() as db:
  DICOMUtils.importDicom(args.folder, db)
  patientUIDs = db.patients()
  for patientUID in patientUIDs:
    loadedNodeIDs.extend(DICOMUtils.loadPatientByUID(patientUID))



#Creates a surface mesh from volume node using CLI module grayscale model maker. Threshold is set as a parameter
#Adds ' skull' to the name of the volume as name of model
def modelFromVolume(thresh):
  """Create surface mesh from volume node using CLI module"""
  global volumeNode
  volumeNode = slicer.mrmlScene.GetNthNodeByClass(0,"vtkMRMLScalarVolumeNode")
  # Set parameters
  parameters = {}
  parameters["InputVolume"] = volumeNode
  parameters["Threshold"] = thresh
  global outputModelNode
  outputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode")
  outputModelNode.SetName(volumeNode.GetName()+' skull')
  volumeNode.GetName()
  parameters["OutputGeometry"] = outputModelNode
  # Execute
  grayMaker = slicer.modules.grayscalemodelmaker
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


#get otsu threshold
masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')
import vtkITK
Otsu_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
Otsu_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
Otsu_thresholdCalculator.SetMethodToOtsu()
Otsu_thresholdCalculator.Update()
Otsuval = Otsu_thresholdCalculator.GetThreshold()
#print('Otsu threshold is: ' + Otsuval)
#get max value in volume
otsu_int = int(Otsuval)
print("Otsu threshold is:")
print(otsu_int)

try:
  modelFromVolume(otsu_int)
except:
  print("failed to create model")


