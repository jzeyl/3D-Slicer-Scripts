#now run the markups model in GUI to create a model. 
# 
# Then need to import as a segmentation
modeloutlinenode = slicer.util.getNode('EC_TM_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'EC_TM_mod' model and 
modeloutlinenode.SetDisplayVisibility(0)

#now run the thresholding on the EC_TM_mod area
#create maxent segment, isodata segment, and subtract the two
thresh_EC_TMseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" ECplusTM")#create new segmentation ID

#momentsISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" ECplusTM")#
#segmentEditorNode.SetSelectedSegmentID(EC_TM_modthresh)#
segmentEditorNode.SetMaskSegmentID('EC_TM_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(ISOval))#str(ISOval)
effect.setParameter("MaximumThreshold",str(Maxentval))
effect.self().onApply()#apply separate


############MAKE RW curve markup to model
#############RW################3# Then need to import as a segmentation
RWmodeloutlinenode = slicer.util.getNode('RW_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(RWmodeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'RW' model and 
RWmodeloutlinenode.SetDisplayVisibility(0)

#MAX ENTROPY THRESHOLD OF RW
RW_modthreshseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" RW_modthresh")#create new segmentation ID
#
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" RW_modthresh")
segmentEditorNode.SetMaskSegmentID('RW_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
#effect.setParameter("AutoThresholdMode",'SET_MIN_UPPER')
#effect.setParameter("AutoThresholdMethod","MAXIMUM_ENTROPY")#maximum entropy algorithm
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))

effect.self().onApply()#apply separate

############MAKE CA curve markup to model


#############  CA   ################3# Then need to import as a segmentation
CAmodeloutlinenode = slicer.util.getNode('CA_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(CAmodeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'EC_TM_mod' model and 
CAmodeloutlinenode.SetDisplayVisibility(0)

#MAX ENTROPY THRESHOLD OF ECD
CA_modthreshseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" CA_modthresh")#create new segmentation ID
#
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" CA_modthresh")
segmentEditorNode.SetMaskSegmentID('CA_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
#effect.setParameter("AutoThresholdMode",'SET_MIN_UPPER')
#effect.setParameter("AutoThresholdMethod","MAXIMUM_ENTROPY")#maximum entropy algorithm
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))

effect.self().onApply()#apply separate

##################


#To generate the contours from your own module, you just need to add a vtkMRMLMarkupsToModelNode in your scene and set up its inputs and outputs. 
# At minimum, call SetAndObserveMarkupsNodeID and SetAndObserveModelNodeID. 
# 
# See all methods and options at:
#https://github.com/SlicerIGT/SlicerIGT/blob/master/MarkupsToModel/MRML/vtkMRMLMarkupsToModelNode.h 20
#MarkupsToModel/MRML/vtkMRMLMarkupsToModelNode.h 21

inputMarkups = getNode('_TM')

outputModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())
outputModel.CreateDefaultDisplayNodes()
outputModel.GetDisplayNode().SetSliceIntersectionVisibility(True)
outputModel.GetDisplayNode().SetColor(1,0,0)

markupsToModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
markupsToModel.SetAutoUpdateOutput(True)
markupsToModel.SetAndObserveModelNodeID(outputModel.GetID())#output
markupsToModel.SetAndObserveMarkupsNodeID(inputMarkups.GetID())

#model typ3 (closed)
#set tube radius
#set colour


#InputMarkups [InputMarkups]: vtkMRMLMarkupsFiducialNode1
#OutputModel [OutputModel]: vtkMRMLModelNode5
#ModelType: curve
#PolynomialFitType: globalLeastSquares
#TubeRadius: 0.2

layoutManager = slicer.app.layoutManager()
threeDWidget = layoutManager.threeDWidget(0)
threeDView = threeDWidget.threeDView()
threeDView.yaw()

import ScreenCapture
ScreenCapture.ScreenCaptureLogic().captureSliceSweep(getNode('vtkMRMLSliceNodeRed'), -125.0, 75.0, 30, "c:/tmp", "image_%05d.png")
