
#displaynodelist = slicer.mrmlScene.GetNodesByClass('vtkMRMLMarkupsDisplayNode')
#for i in range(len(displaynodelist)):
#    print(displaynodelist[i])
#slicer.mrmlScene.GetNthNodeByClass(1,'vtkMRMLMarkupsDisplayNode').

#displaynodelist[0]

masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()

#set up segmentatin node
segmentationNode = slicer.util.getNode('Segmentation')

#set appropriate display of fiducials
displaynodelist = slicer.util.getNodesByClass('vtkMRMLMarkupsDisplayNode')
for i in range(len(displaynodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetGlyphScale(0.15)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetTextScale(0.15)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetSelectedColor(0,0,0)#black

#get names of marksup
markupfiducials = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')

#get the names of all the markups
for i in range(len(markupfiducials)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').GetName()

#Set lock all of the markupfiducials
for i in range(len(markupfiducials)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').SetLocked(1)

#setcolor of models to all the same colour
modelnodelist = slicer.util.getNodesByClass('vtkMRMLModelNode')

#get the names of all the models
for i in range(len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetName()

#set colour of all to red
for i in range(3,len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetDisplayNode().SetColor(1,0,0)
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').GetDisplayNode().SetOpacity(0.5)
    
#make all models visible or not:
for i in range(3,len(modelnodelist)):
    slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLModelNode').SetDisplayVisibility(0)
#convert models to markups
#markups fiducial node

for i in range(len(displaynodelist)):
    inputMarkups = slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode')
    #create model node
    ECTMModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
    ECTMModel.SetName('_newmm')
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


####check the coverage of the model in 4d view
# CONVERT TO segmentation
modeloutlinenode = slicer.util.getNode(ID+'EC_TM_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'EC_TM_mod' model and 
modeloutlinenode.SetDisplayVisibility(0)

