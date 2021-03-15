#This scripts imports all the stl files from a folder

#filesinfolder = slicer.util.getFilesInDirectory(folder)

#find all files with 'stl' in the folder to load stl files
stlregex = "stl"
stlfiles = [i for i in filesinfolder if stlregex in i] 

#load models
for i in range(0,len(stlfiles)):
    slicer.util.loadModel(stlfiles[i])

#setcolor of models to all the same colour
modelnodelist = slicer.util.getNodesByClass('vtkMRMLModelNode')

#get the names of all the models and put in a list
modelnamelist = []
for i in range(len(modelnodelist)):
    modelnamelist.append(slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetName())

#set colour of all models to white
for i in range(3,len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetDisplayNode().SetColor(1,1,1)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetDisplayNode().SetOpacity(0.5)

#set color specific models to another colour if desired:
#slicer.mrmlScene.GetNthNodeByClass(4,'vtkMRMLModelNode').GetDisplayNode().SetColor(1,0,0)
#slicer.mrmlScene.GetNthNodeByClass(7,'vtkMRMLModelNode').GetDisplayNode().SetColor(1,0,0)

#get model node by name to change colour
#slicer.util.getNode('Segment_6').GetDisplayNode().SetColor(1,0,0)

#make all models invisible:
for i in range(3,len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').SetDisplayVisibility(0)

#convert models to markups
#import ScreenCapture
#viewNodeID = 'vtkMRMLSliceNodeRed'
#cap = ScreenCapture.ScreenCaptureLogic()
#view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
#cap.captureImageFromView(view,slicedir+'\\'+ID+'redslice2.tif')
#
#
##change display of specific model
#modeloutlinenode = slicer.util.getNode(ID+'EC_TM_mod')#create model node from the just created model
#slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")


