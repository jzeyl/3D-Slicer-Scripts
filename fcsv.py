#this script imports the fcsv files form the folder and changes the formatting settings
#filesinfolder = slicer.util.getFilesInDirectory('C:\\Users\\jeffzeyl\\Desktop\\copyoutput\\Jun17 batch\\Acrake01_2020')

#find all files with 'fcsv' in the folder to load fcsv files

fcsvregex = "fcsv"
fcsvfiles = [i for i in filesinfolder if fcsvregex in i] 

#load fiducial files
for i in range(0,len(fcsvfiles)):
    slicer.util.loadMarkupsFiducialList(fcsvfiles[i])

#SET DISPLAY OF ALL FIDUCIALS (color, size) AND LOCK
displaynodelist = slicer.util.getNodesByClass('vtkMRMLMarkupsDisplayNode')
for i in range(len(displaynodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetGlyphScale(0.15)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetTextScale(0)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetSelectedColor(0,0,0)#black

#get names of marksup
markupfiducials = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')

for i in range(len(markupfiducials)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').SetLocked(1)

#get names
fiducialnames = []
for i in range(len(markupfiducials)):
    fiducialnames.append(slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').GetName())

#USE the markup-to-models to create a model connecting points for all models:
for i in range(len(displaynodelist)):
    inputMarkups = slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode')
    #create model node
    ECTMModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
    ECTMModel.SetName(fiducialnames[i]+'mm')
    ECTMModel.CreateDefaultDisplayNodes()
    ECTMModel.GetDisplayNode().SetSliceIntersectionVisibility(True)
    ECTMModel.GetDisplayNode().SetColor(0,0,0)
    #create markups to model node
    markupsToModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
    markupsToModel.SetAutoUpdateOutput(True)
    markupsToModel.SetAndObserveMarkupsNodeID(inputMarkups.GetID())#set input node
    markupsToModel.SetAndObserveModelNodeID(ECTMModel.GetID())#set model node (only needed for the first one)
    markupsToModel.SetModelType(1)#curve
    markupsToModel.SetTubeRadius(0.05)
    markupsToModel.SetTubeLoop(1)#1 = curve is a loop
    markupsToModel.SetCurveType(0)#polynomial least squares
#

