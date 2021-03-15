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



######################################################################################3
#import empty fiducial markups
def fcsv_template():
    global FIDNode1
    FIDNode1 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
    FIDNode1.SetName(ID+" TM")#creates a new segmentation
    global FIDNode2
    FIDNode2 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
    FIDNode2.SetName(ID+" RW")#creates a new segmentation
    global FIDNode3
    FIDNode3 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
    FIDNode3.SetName(ID+" CA")#creates a new segmentation
    global FIDNode4 
    FIDNode4 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
    FIDNode4.SetName(ID+" EC")#creates a new segmentation
    global FIDNode5
    FIDNode5 = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode")
    FIDNode5.SetName(ID+"ECandTMmrk_outline")#creates a new segmentation


####SELECT POINTS in GUI###
#CLICK TM FIRST!


#set ficudial display nodes
def fcsv_display_smaller():
  global FIDNode1DisplayNode
  FIDNode1DisplayNode = FIDNode1.GetDisplayNode()
  FIDNode1DisplayNode.SetGlyphScale(0.15)
  FIDNode1DisplayNode.SetTextScale(0.1)
  FIDNode1DisplayNode.SetSelectedColor(1,0,0)#red
  global FIDNode1DisplayNode2
  FIDNode2DisplayNode = FIDNode2.GetDisplayNode()
  FIDNode2DisplayNode.SetGlyphScale(0.15)
  FIDNode2DisplayNode.SetTextScale(0.1)
  FIDNode2DisplayNode.SetSelectedColor(0,1,0)#green
  global FIDNode1DisplayNode3
  FIDNode3DisplayNode = FIDNode3.GetDisplayNode()
  FIDNode3DisplayNode.SetGlyphScale(0.15)
  FIDNode3DisplayNode.SetTextScale(0.1)
  FIDNode3DisplayNode.SetSelectedColor(1,1,0)#green
  global FIDNode1DisplayNode4
  FIDNode4DisplayNode = FIDNode4.GetDisplayNode()
  FIDNode4DisplayNode.SetGlyphScale(0.15)
  FIDNode4DisplayNode.SetTextScale(0.1)
  global FIDNode1DisplayNode5
  FIDNode5DisplayNode = FIDNode5.GetDisplayNode()
  FIDNode5DisplayNode.SetGlyphScale(0.15)
  FIDNode5DisplayNode.SetTextScale(0.1)
  FIDNode5DisplayNode.SetSelectedColor(0,0,0)#black
  FIDNode1.SetLocked(1)
  FIDNode2.SetLocked(1)
  FIDNode3.SetLocked(1)
  FIDNode4.SetLocked(1)
  FIDNode5.SetLocked(1) #keep this one open



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


