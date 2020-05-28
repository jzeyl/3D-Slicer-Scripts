threshcol = segmentationNode.GetSegmentation().AddEmptySegment(ID+" thresh col")
#MAX ENTROPY THRESHOLD OF COLUMELLA
#OverwriteMode: OverwriteNone
#SelectedSegmentID: threshcol
#ActiveEffectName: "Threshold"
#MaskMode: PaintAllowedInsideSingleSegment #segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideVisibleSegments)
#MaskSegmentID: paintcol
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorWidget.setActiveEffectByName("Threshold")
segmentEditorNode.SetSelectedSegmentID(ID+" thresh col")
segmentEditorNode.SetMaskSegmentID(ID+" paint col")
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

#quantification table
#resultsTableNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTableNode')# create table node
#import SegmentStatistics
#segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
#segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
#segStatLogic.getParameterNode().SetParameter("ScalarVolume", os.listdir(folder)[0].replace('.tif',''))############change here to the named volume
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.enabled","False")
#segStatLogic.getParameterNode().SetParameter("ScalarVolumeSegmentStatisticsPlugin.voxel_count.enabled","False")
#segStatLogic.computeStatistics()
#segStatLogic.exportToTable(resultsTableNode)
#segStatLogic.showTable(resultsTableNode)

#OR STORE STATS AS DICTIONARY:
import SegmentStatistics
segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_origin_ras.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_diameter_mm.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_x.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_y.enabled",str(True))
#segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_z.enabled",str(True))
segStatLogic.computeStatistics()
stats = segStatLogic.getStatistics()
#x = thisdict["model"]
#stats['BS01-2019 thresh col']
#colvol = stats[ID+" thresh col", 'ClosedSurfaceSegmentStatisticsPlugin.volume_mm3']
colvol = stats[ID+" thresh col",'LabelmapSegmentStatisticsPlugin.volume_mm3']
'KW01 thresh col', 'LabelmapSegmentStatisticsPlugin.volume_mm3'
'KW01 thresh col', 'LabelmapSegmentStatisticsPlugin.volume_mm3'

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

#moments/ISODATA-MAXENT THRESHOLD FOR UMBO
segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
segmentEditorNode.SetMaskMode(slicer.vtkMRMLSegmentEditorNode.PaintAllowedInsideSingleSegment)
segmentEditorNode.SetSelectedSegmentID(ID+" thresh umbo")
segmentEditorNode.SetMaskSegmentID(ID+" paint umbo")
segmentEditorWidget.setActiveEffectByName("Threshold")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MinimumThreshold", str(ISOval))#//str(Momentsval),str(ISOval)
effect.setParameter("MaximumThreshold",str(Maxentval))

effect.self().onApply()#apply separate


####################SAVE#####################