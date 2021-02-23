#these static functions are added to the slicerrc file so they can be used from within 3D slicer

def colthresh():
    threshcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh col")
    segmentationDisplayNode.SetSegmentOpacity3D(ID+" thresh col", 1)
    segmentationNode.GetSegmentation().GetSegment(ID+" thresh col").SetColor(0,0,1)
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
    segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
    segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
    segmentEditorNode.SetMaskSegmentID(ID+" paint col")
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold", str(Maxentval))
    effect.setParameter("MaximumThreshold",str(volumeScalarRange[1]))
    effect.self().onApply()#apply separate

def colkeeplargestisland():
    #run keep largest island on thresholded columella
    segmentEditorWidget.setActiveEffectByName("Islands")
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
    effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
    effect.self().onApply()#apply separate

def writecolvoltofile():
    #OR STORE STATS AS DICTIONARY:
    import SegmentStatistics
    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
    segStatLogic.computeStatistics()
    stats = segStatLogic.getStatistics()
    colvol = stats[ID+" thresh col",'LabelmapSegmentStatisticsPlugin.volume_mm3']
    #Write to text file
    # with is like your try .. finally block in this case
    with open('C:\Users\jeffz\Desktop\Screenshots', 'r') as file:
        # read a list of lines into data
        data = file.readlines()
    data.append(ID+', '+str(colvol)+'\n')
    # and write everything back
    with open('C:\\Users\\jeffzeyl\\Desktop\\Volumes.txt', 'w') as file:
        file.writelines( data )



def ecd():
    #MAX ENTROPY THRESHOLD OF ECD
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
    segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
    segmentEditorNode.SetSelectedSegmentID(ID+" thresh ECD")
    segmentEditorNode.SetMaskSegmentID(ID+" paint ECD")
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    #effect.setParameter("AutoThresholdMode",'SET_MIN_UPPER')
    #effect.setParameter("AutoThresholdMethod","MAXIMUM_ENTROPY")#maximum entropy algorithm
    effect.setParameter("MinimumThreshold", str(0))
    effect.setParameter("MaximumThreshold",str(Maxentval))
    effect.self().onApply()#apply separate
    #run KEEP LARGEST ISLAND on ECD tip
    segmentEditorWidget.setActiveEffectByName("Islands")
    effect = segmentEditorWidget.activeEffect()
    segmentEditorNode.SetSelectedSegmentID(ID+" thresh ECD")
    effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
    effect.self().onApply()#apply separate


def umbo_ME_ISOtest():
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
    segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
    segmentEditorNode.SetSelectedSegmentID(ID+" thresh umbo")
    segmentEditorNode.SetMaskSegmentID(ID+" paint umbo")
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold", str(ISOval))#//str(Momentsval),str(ISOval),str(Otsuval)
    effect.setParameter("MaximumThreshold",str(Maxentval))

def umbo_ME_ISO_apply():
    segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
    segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
    segmentEditorNode.SetSelectedSegmentID(ID+" thresh umbo")
    segmentEditorNode.SetMaskSegmentID(ID+" paint umbo")
    segmentEditorWidget.setActiveEffectByName("Threshold")
    effect = segmentEditorWidget.activeEffect()
    effect.setParameter("MinimumThreshold", str(ISOval))#//str(Momentsval),str(ISOval),str(Otsuval)
    effect.setParameter("MaximumThreshold",str(Maxentval))
    effect.self().onApply()#apply separate

def computedEC_TMmarkup():
    import numpy as np
    #Extracolumella
    numberfiducialpoints = FIDNode4.GetNumberOfFiducials()#g
    points = np.zeros([numberfiducialpoints,3])#4 rows, 3 columns (i.e., 4 points, each with x,y,z)
    FIDNode4.GetNthFiducialPosition(0,points[0,:])#get first point of EC markup (umbo)
    umbo = points[0,]
    FIDNode4.GetNthFiducialPosition(1,points[1,:])#get second point from first row of numpy array
    coltip = points[1,]
    #add the columella and umbo point to the new "ECandTMmrk_outline" node
    FIDNode5.AddFiducial(umbo[0],umbo[1],umbo[2])#add umbo
    FIDNode5.AddFiducial(coltip[0],coltip[1],coltip[2])#add coltip point
    #add TM markup points to an array, and add from array to 
    numberfiducialpoints = FIDNode1.GetNumberOfFiducials()
    points = np.zeros([numberfiducialpoints,3])#array to populate with TM fiducial points
    for i in range(0, numberfiducialpoints):#put the TM points into the 'points' array
      FIDNode1.GetNthFiducialPosition(i, points[i,:])
    #add the fiducial nodes from the 'points array' to the "ECandTMmrk_outline" node
    for i in range(0,numberfiducialpoints):
      FIDNode5.AddFiducial(points[i,][0],points[i,][1],points[i,][2])



def ETmarkuptomodel():
    #markups fiducial node
    inputMarkups = getNode(ID+'ECandTMmrk_outline')
    #create model node
    ECTMModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLModelNode())#adding a node to scene
    ECTMModel.SetName(ID+'EC_TM_mod')
    ECTMModel.CreateDefaultDisplayNodes()
    ECTMModel.GetDisplayNode().SetSliceIntersectionVisibility(True)
    #ECTMModel.GetDisplayNode().SetColor(0,1,0)
    #create markups to model node
    markupsToModel = slicer.mrmlScene.AddNode(slicer.vtkMRMLMarkupsToModelNode())
    markupsToModel.SetAutoUpdateOutput(True)
    markupsToModel.SetAndObserveMarkupsNodeID(inputMarkups.GetID())#set input node
    markupsToModel.SetAndObserveModelNodeID(ECTMModel.GetID())#set model node (only needed for the first one)
    markupsToModel.SetModelType(0)#closed surface
    ####check the coverage of the model in 4d view



#MARKUPS TO MODELS
# CONVERT TO segmentation
modeloutlinenode = slicer.util.getNode(ID+'EC_TM_mod')#create model node from the just created model
slicer.modules.segmentations.logic().ImportModelToSegmentationNode(modeloutlinenode,segmentationNode,"tosegment")

#remove visibility of 'EC_TM_mod' model and 
modeloutlinenode.SetDisplayVisibility(0)
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


def opennewvolume():
    global filesinfolder
    filesinfolder = slicer.util.getFilesInDirectory(folder)
    slicer.mrmlScene.SetRootDirectory(folder)
    global vol
    vol = "tif"
    global volfile
    volfile = [i for i in filesinfolder if vol in i] 
    volfile
    #load volume
    slicer.util.loadVolume(volfile[0])
    #SET ID AND SPACING
    #set up volume resolution
    global masterVolumeNode
    masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
    import itertools
    global imagespacing
    imagespacing = [spacing]*3
    masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
    global volumeScalarRange
    volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()


#set up segmentatin node

#if previously saved
#segmentationNode = slicer.util.getNode('Segmentation')
#segmentEditorNode = slicer.util.getNode('SegmentEditor')


# Create SEGMENTATION NODE AND LINK TO VOLUME (if there isn't one already existing! otherwise, node can be named using the preceding command)
segmentationNode = slicer.vtkMRMLSegmentationNode()#name segmentation node
slicer.mrmlScene.AddNode(segmentationNode)#add the node to the scene
segmentationNode.CreateDefaultDisplayNodes() # only needed for display
segmentationDisplayNode=segmentationNode.GetDisplayNode()

segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)#link the segmentation to the volume
#CREATE EMPTY SEGMENTS
paintcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint col")
paintumbo = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint umbo")
threshumbo = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh umbo")
paintecd = segmentationNode.GetSegmentation().AddEmptySegment(ID+" paint ECD")

threshecd = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh ECD")

#threshcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh col")
#add segment editor node

segmentEditorNode = slicer.vtkMRMLSegmentEditorNode()
slicer.mrmlScene.AddNode(segmentEditorNode)#add segment editor node to scene
#if previously saved
#segmentEditorNode = slicer.util.getNode('SegmentEditor')
# Create segment editor to get access to effects
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)#connect widget to scene
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)#connect segment editor to editor widget
segmentEditorWidget.setSegmentationNode(segmentationNode)#connect segmentation node
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)#connect master node
# Compute bone threshold value automatically
import vtkITK

ME_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
ME_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
ME_thresholdCalculator.SetMethodToMaximumEntropy()
ME_thresholdCalculator.Update()
Maxentval = ME_thresholdCalculator.GetThreshold()

ISO_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
ISO_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
ISO_thresholdCalculator.SetMethodToIsoData()
ISO_thresholdCalculator.Update()
ISOval = ISO_thresholdCalculator.GetThreshold()

Moments_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
Moments_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
Moments_thresholdCalculator.SetMethodToMoments()
Moments_thresholdCalculator.Update()
Momentsval = Moments_thresholdCalculator.GetThreshold()

Otsu_thresholdCalculator = vtkITK.vtkITKImageThresholdCalculator()
Otsu_thresholdCalculator.SetInputData(masterVolumeNode.GetImageData())
Otsu_thresholdCalculator.SetMethodToOtsu()
Otsu_thresholdCalculator.Update()
Otsuval = Otsu_thresholdCalculator.GetThreshold()

