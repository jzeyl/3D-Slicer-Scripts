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

#run keep largest island on thresholded columella
segmentEditorWidget.setActiveEffectByName("Islands")
effect = segmentEditorWidget.activeEffect()
segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
effect.setParameterDefault("Operation", "KEEP_LARGEST_ISLAND")
effect.self().onApply()#apply separate

#OR STORE STATS AS DICTIONARY:
import SegmentStatistics
segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
segStatLogic.computeStatistics()
stats = segStatLogic.getStatistics()
colvol = stats[ID+" thresh col",'LabelmapSegmentStatisticsPlugin.volume_mm3']

#Write to text file
# with is like your try .. finally block in this case
with open('C:\\Users\\jeffzeyl\\Desktop\\Volumes.txt', 'r') as file:
    # read a list of lines into data
    data = file.readlines()

data.append(ID+', '+str(colvol)+'\n')

# and write everything back
with open('C:\\Users\\jeffzeyl\\Desktop\\Volumes.txt', 'w') as file:
    file.writelines( data )


#
#
##############put effect on 'none in GUI'

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


###DESELECT 'paint
#moments/ISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh umbo")
segmentEditorNode.SetMaskSegmentID(ID+" paint umbo")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(ISOval))#//str(Momentsval),str(ISOval),str(Otsuval)
effect.setParameter("MaximumThreshold",str(Maxentval))
effect.self().onApply()#apply separate

####################SAVE#####################
####################SAVE#####################

# Change one segment display properties
segmentId = segmentation.GetSegmentIdBySegmentName("Segment_1")
segmentationDisplayNode.SetSegmentOpacity2DOutline(segmentId, 0.0)
segmentation.GetSegment(segmentId).SetColor(1,0,0)  # color should be set in segmentation node