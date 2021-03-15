#MARKUPS TO MODELS

# 1 TYMPANIC MEMBRANE AND EXTRACOLUMELLA

#markups fiducial node
inputMarkups = getNode(ID+'ECandTMmrk_outline')
#create model node
ECTMModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
ECTMModel.SetName(ID+'EC_TM_mod')
ECTMModel.CreateDefaultDisplayNodes()
ECTMModel.GetDisplayNode().SetSliceIntersectionVisibility(True)
#ECTMModel.GetDisplayNode().SetColor(0,1,0)
#
##create markups to model node
markupsToModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
markupsToModel.SetAutoUpdateOutput(True)
markupsToModel.SetAndObserveMarkupsNodeID(inputMarkups.GetID())#set input node
markupsToModel.SetAndObserveModelNodeID(ECTMModel.GetID())#set model node (only needed for the first one)
markupsToModel.SetModelType(0)#closed surface
#####check the coverage of the model in 4d view



# CONVERT TO segmentation
modeloutlinenode = slicer.util.getNode(ID+'EC_TM_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'EC_TM_mod' model and 
modeloutlinenode.SetDisplayVisibility(0)

#now run the thresholding on the EC_TM_mod area
#create maxent segment, isodata segment, and subtract the two
thresh_EC_TMseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" ECplusTM")#create new segmentation ID
segmentationNode.GetSegmentation().GetSegment(ID+" ECplusTM").SetColor(1,0,0)


#momentsISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" ECplusTM")#
#segmentEditorNode.SetSelectedSegmentID(EC_TM_modthresh)#
segmentEditorNode.SetMaskSegmentID(ID+'EC_TM_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(ISOval))#str(ISOval)
effect.setParameter("MaximumThreshold",str(Maxentval))
effect.self().onApply()#apply separate

#set mod region segment visibility off
#segmentationDisplayNode.SetSegmentVisibility(ID+'EC_TM_mod',0)
#
# ###########2 RW curve markup to model
#name markups fiducial node
RWmarkup = getNode(ID+" RW")

#create model node
RWmodeloutlinenode = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
RWmodeloutlinenode.SetName(ID+'RW_mod')
RWmodeloutlinenode.CreateDefaultDisplayNodes()
RWmodeloutlinenode.GetDisplayNode().SetSliceIntersectionVisibility(True)
RWmodeloutlinenode.GetDisplayNode().SetColor(1,0,0)

#new markups to model node
markupsToModel2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
markupsToModel2.SetAutoUpdateOutput(True)
markupsToModel2.SetAndObserveMarkupsNodeID(RWmarkup.GetID())#set input node
markupsToModel2.SetAndObserveModelNodeID(RWmodeloutlinenode.GetID())#set model node (only needed for the first one)
markupsToModel2.SetModelType(1)#curve
markupsToModel2.SetTubeRadius(0.2)
markupsToModel2.SetTubeLoop(1)#1 = curve is a loop
markupsToModel2.SetCurveType(2)#polynomial least squares

#markupsToModel.SetAndObserveModelNodeID(outputMode2.GetID())#set model node
#CONVERT RW MODEL TO SEGMENTATION
RWmodeloutlinenode = slicer.util.getNode(ID+'RW_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(RWmodeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'RW' model and 
RWmodeloutlinenode.SetDisplayVisibility(0)

#MAX ENTROPY THRESHOLD OF RW
RW_modthreshseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" RW_modthresh")#create new segmentation ID
segmentationNode.GetSegmentation().GetSegment(ID+" RW_modthresh").SetColor(1,1,1)

segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" RW_modthresh")
segmentEditorNode.SetMaskSegmentID(ID+'RW_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
effect.self().onApply()#apply separate

############MAKE CA curve markup to model
CAmarkup = getNode(ID+" CA")

#create model node
CAmodeloutlinenode = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
CAmodeloutlinenode.SetName(ID+'CA_mod')
CAmodeloutlinenode.CreateDefaultDisplayNodes()
CAmodeloutlinenode.GetDisplayNode().SetSliceIntersectionVisibility(True)
CAmodeloutlinenode.GetDisplayNode().SetColor(1,0,0)

#new markups to model node
markupsToModel2 = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
markupsToModel2.SetAutoUpdateOutput(True)
markupsToModel2.SetAndObserveMarkupsNodeID(CAmarkup.GetID())#set input node
markupsToModel2.SetAndObserveModelNodeID(CAmodeloutlinenode.GetID())#set model node (only needed for the first one)
markupsToModel2.SetModelType(1)#curve
markupsToModel2.SetTubeRadius(0.2)
markupsToModel2.SetTubeLoop(1)#1 = curve is a loop
markupsToModel2.SetCurveType(2)#polynomial least squares


#############  CA   ################3# Then need to import as a segmentation
CAmodeloutlinenode = slicer.util.getNode(ID+'CA_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(CAmodeloutlinenode,segmentationNode,"tosegment")

#remove visibility of model
CAmodeloutlinenode.SetDisplayVisibility(0)

#MAX ENTROPY THRESHOLD OF ECD
CA_modthreshseg = segmentationNode.GetSegmentation().AddEmptySegment(ID+" CA_modthresh")#create new segmentation ID
segmentationNode.GetSegmentation().GetSegment(ID+" CA_modthresh").SetColor(1,1,1)

#
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" CA_modthresh")
segmentEditorNode.SetMaskSegmentID(ID+'CA_mod')
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
#effect.setParameter("AutoThresholdMode",'SET_MIN_UPPER')
#effect.setParameter("AutoThresholdMethod","MAXIMUM_ENTROPY")#maximum entropy algorithm
effect.setParameter("MinimumThreshold", str(Maxentval))
effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
effect.self().onApply()#apply separate

#set mod region segment visibility off
segmentationDisplayNode.SetSegmentVisibility(ID+"CA_mod",0)
segmentationDisplayNode.SetSegmentVisibility(ID+"EC_TM_mod",0)

#set mod region segment visibility off
segmentationDisplayNode.SetSegmentVisibility(ID+"RW_mod",0)
##################









