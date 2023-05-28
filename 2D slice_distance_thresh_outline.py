#4 functions/steps to generate the closest portions of the 2D outlines for two segmentations in a given axis orientation, and within a given distance threshold.
#1) twoToLabelmap('Segment_3','Segment_4'). Input the names of your segments in quotes. Outputs will be hollowed segmentations, 
#labelmaps (needed for the computation)
#2) get_outlines('yellow'). #Specify the axis. Can be 'red','green', or 'yellow'. 
#3) plot_outlines() This will plot all of the outline as markup points (note, may be a several hundred points). 
  #You can skip this step if not needed - the points are saved as an object and used for the 
  #next plotwithindist function.
#4) plotwithindist(5,10). The first input is the distance 
#threshold (in mm) to select outline coordinates relative to the other segment. 
#The second is the number of points that should be used to represent the outline.




import numpy as np
#1) Function to make hollow segmentations and labelmap volumes for each segmentatione.g.  hollow('segment_1','segment2'), taking the names of the segmentations to compare as input, producing 2 hollow segments and 2 labelmaps volumes, one for each bone structure outline
def connect():
  """
  Connects the segmentation and volume nodes together in preparation for subsequent functions. Adds a segmentation node to the scene
  """
  global masterVolumeNode
  global segmentationNode
  global segmentEditorNode
  global segmentEditorWidget
  #Connect the volumes and segmentation to allow programatic access to model-segmentation conversion and segmentation effects
  masterVolumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')#detects the first scalar volume

  numseg = len(slicer.util.getNodesByClass('vtkMRMLSegmentationNode'))#number of segmentations in scene
  if numseg == 0:
    print("new segmentation created")
    segmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    segmentationNode.CreateDefaultDisplayNodes() # only needed for display
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
    segmentationNode.GetSegmentation().AddEmptySegment("restoration")
    segmentationNode.GetSegmentation().AddEmptySegment("teeth")
    segmentationNode.GetSegmentation().AddEmptySegment("mandible")
    segmentationNode.GetSegmentation().AddEmptySegment("lesion")
  else:
    print("Segment effect widget connected to first segmentation in scene")
    segmentationNode = slicer.util.getNodesByClass('vtkMRMLSegmentationNode')[0]
    segmentationNode.CreateDefaultDisplayNodes() # only needed for display
    segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  # Create segment editor to get access to effects
  segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
  # To show segment editor widget (useful for debugging): segmentEditorWidget.show()
  segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
  segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
  segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
  segmentEditorWidget.setSegmentationNode(segmentationNode)
  segmentEditorWidget.setSourceVolumeNode(masterVolumeNode)

def copyHollowandLabelmap(target):
  """
  Copy segmentation, hollow, and convert to labelmap. Must use connect() beforehand.
  Hollow outline width is default to 2x resolution of scan
  """
  #allow overlap so new hollowed segmentations don't destroy other segments already present
  segmentEditorNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
  #
  segmentationNode.GetSegmentation().AddEmptySegment(f'{target} hollow copy')
  segmentEditorWidget.setActiveEffectByName('Logical operators')
  effect = segmentEditorWidget.activeEffect()
  newnm = f'{target} hollow copy'
  segmentEditorNode.SetSelectedSegmentID(newnm)
  effect.setParameter("Operation", "COPY")
  effect.setParameter("ModifierSegmentID", target)#subtract this selection
  effect.self().onApply()
  #hollow
  segmentEditorWidget.setActiveEffectByName('Hollow')
  effect = segmentEditorWidget.activeEffect()
  segmentEditorNode.SetSelectedSegmentID(newnm)
  effect.setParameter("ShellMode","MEDIAL_SURFACE")#3mm is default
  effect.setParameter("ShellThicknessMm",masterVolumeNode.GetSpacing()[0]*2)# shell thickness mm set here
  effect.self().onApply()
  global labelmapVolumeNode
  lblnm = f'lbl {newnm}'
  labelmapVolumeNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode',lblnm)
  ##make all segment non-visible except seg of interest
  segmentationNode.GetDisplayNode().SetAllSegmentsVisibility(0)#make all
  segmentationNode.GetDisplayNode().SetSegmentVisibility(newnm,1)
  slicer.modules.segmentations.logic().ExportVisibleSegmentsToLabelmapNode(segmentationNode, labelmapVolumeNode, masterVolumeNode)
  print(f'{target} segment hollowed, copied, and exported to labelmap')


def twoToLabelmap(seg1,seg2):
  connect()
  copyHollowandLabelmap(seg1)
  copyHollowandLabelmap(seg2)
  global lbl
  lbl = slicer.mrmlScene.GetNthNodeByClass(0,'vtkMRMLLabelMapVolumeNode')
  global lbl2
  lbl2 = slicer.mrmlScene.GetNthNodeByClass(1,'vtkMRMLLabelMapVolumeNode')
  global seg_1
  seg_1 = seg1
  global seg_2
  seg_2 = seg2

#2) Function to get coordinates in a current slice view, for one of the two segmentation/e.g. getsliceoutline(labelmap1, 'red')
def getsliceindex(axis = 'red'):
  ###############################################get slice location
  #convert between volume and RAS (slicer anatomical) coordinates
  if axis == 'red':
    print('red axis')
    widget = slicer.app.layoutManager().sliceWidget("Red")
    logic = widget.sliceLogic()
    sliceoffset = logic.GetSliceOffset()
    print(f'red slice offset: {sliceoffset}')
    point_Ras = [0,0,sliceoffset]
  if axis == 'green':
    print('green axis')
    widget = slicer.app.layoutManager().sliceWidget("Green")
    logic = widget.sliceLogic()
    sliceoffset = logic.GetSliceOffset()
    print(f'green slice offset: {sliceoffset}')
    point_Ras = [0,sliceoffset,0]
  if axis == 'yellow':
    print('yellow axis')
    widget = slicer.app.layoutManager().sliceWidget("Yellow")
    logic = widget.sliceLogic()
    sliceoffset = logic.GetSliceOffset()
    print(f'yellow slice offset: {sliceoffset}')
    point_Ras = [-sliceoffset,0,0]  #zeros are placeholders. Used to test that the coordinate systems are working
  print(f'ras coordinates: {point_Ras}')
  #pointListNode = getNode("F")
  #pointListNode.AddControlPoint(point_Ras)
  # If volume node is transformed, apply that transform to get volume's RAS coordinates
  transformRasToVolumeRas = vtk.vtkGeneralTransform()
  slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(None, masterVolumeNode.GetParentTransformNode(), transformRasToVolumeRas)
  point_VolumeRas = transformRasToVolumeRas.TransformPoint(point_Ras)
  # Get voxel coordinates from physical coordinates
  volumeRasToIjk = vtk.vtkMatrix4x4()
  masterVolumeNode.GetRASToIJKMatrix(volumeRasToIjk)
  global point_Ijk
  point_Ijk = [0, 0, 0, 1]
  volumeRasToIjk.MultiplyPoint(np.append(point_VolumeRas,1.0), point_Ijk)
  point_Ijk = [ int(round(c)) for c in point_Ijk[0:3] ]
  # Print output
  print(f'ijk coordinates: {point_Ijk}')


#2) Function to get coordinates in a current slice view, for one of the two segmentation/e.g. getsliceoutline(labelmap1, 'red')
################RESAMPLE ARRAY TO MANAGEABLE NUMBER OF COORDINATES
def resample_array(array, target_length):
    current_length = len(array)
    if current_length == target_length:
        return array
    # Calculate the indices of the original array for the resampled array
    indices = np.linspace(0, current_length - 1, target_length, dtype=int)
    # Resample the array based on the calculated indices
    resampled_array = array[indices]
    return resampled_array

# Get voxel position in IJK coordinate system
def getsliceoutline(lbl,axis, numpts):#,num_pts
  #get non-zero labelmap coordinates from slice of interest
  volumeArray = slicer.util.arrayFromVolume(lbl)
  #IF SLICE = "RED"
  if axis == 'red':
    getsliceindex('red')
    slice = volumeArray[point_Ijk[2],:,:]#get RED slice. IF STATEMENT HERE
  if axis == 'green':
    getsliceindex('green')
    slice = volumeArray[:,point_Ijk[1],:]#get RED slice. IF STATEMENT HERE
  if axis == 'yellow':
    getsliceindex('yellow')
    slice = volumeArray[:,:,point_Ijk[0]]#get RED slice. IF STATEMENT HERE
  #print(slice.max())
  #
  only1s = np.where(slice > 0)#tuple of 2 arrays, missing slice it's taken from
  #print(only1s)
  if axis == 'red':
    my_array = np.full(len(only1s[0]), fill_value=point_Ijk[2])#constant slice index slice plane redpts is take from
    tup3 = (my_array,only1s[0], only1s[1])#add this slice to the index so it is a 3d tuple
  if axis == 'green':
    my_array = np.full(len(only1s[0]), fill_value=point_Ijk[1])#constant slice index slice plane redpts is take from
    tup3 = (only1s[0], my_array, only1s[1])#add this slice to the index so it is a 3d tuple
  if axis == 'yellow':
    my_array = np.full(len(only1s[0]), fill_value=point_Ijk[0])#constant slice index slice plane redpts is take from
    tup3 = (only1s[0], only1s[1],my_array)#add this slice to the index so it is a 3d tuple
  point_Kji =tup3 #coordinates of non-zero voxels in slice to be passed on
  #print(point_Kji)
  if numpts == 'max':
    return point_Kji
  else:
    point_Kji_short = []
    for i in range(0,len(point_Kji)):
        shor = resample_array(point_Kji[i],numpts)
        point_Kji_short.append(shor)
    point_Kji_short = tuple(point_Kji_short)
    return point_Kji_short

def get_outlines(axis):
  #get outlines from two segmentations (ones created into labelmaps)
  #outlines can be 'red', 'green', or 'yellow' 
  global seg1outline
  seg1outline = np.array(getsliceoutline(lbl,axis,'max'))
  global seg2outline
  seg2outline = np.array(getsliceoutline(lbl2,axis,'max'))
  print(f'{axis} slice outline arrays stored as "seg1outline" and "seg2outline"')


#3) Function to plot markups of segmentationvolumeNodepof/labelmap outlines from current slice view e.e. plotmarkups(labelmap1, numer of points)
##############convert each point to RAS and add to markup node########################

def plotfulloutline(outline, fidnode):#specify fiducial node
  for i in range(0,len(outline[0])):
    point_Ijk = [outline[2][i], outline[1][i], outline[0][i]]
    #print(point_Ijk)
    #print(point_Ijk)
    # Get physical coordinates from voxel coordinates
    volumeIjkToRas = vtk.vtkMatrix4x4()
    masterVolumeNode.GetIJKToRASMatrix(volumeIjkToRas)
    point_VolumeRas = [0, 0, 0, 1]
    volumeIjkToRas.MultiplyPoint(np.append(point_Ijk,1.0), point_VolumeRas)
    # If volume node is transformed, apply that transform to get volume's RAS coordinates
    transformVolumeRasToRas = vtk.vtkGeneralTransform()
    slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(masterVolumeNode.GetParentTransformNode(), None, transformVolumeRasToRas)
    point_Ras = transformVolumeRasToRas.TransformPoint(point_VolumeRas[0:3])
    # Add a markup at the computed position and print its coordinates
    fidnode.AddControlPoint((point_Ras[0], point_Ras[1], point_Ras[2]))#kji reversed in numpy
    #print(point_Ras)


def adjmarkupdisplayandlock():
  #SET DISPLAY OF ALL FIDUCIALS (color, size) AND LOCK
  displaynodelist = slicer.util.getNodesByClass('vtkMRMLMarkupsDisplayNode')
  for i in range(len(displaynodelist)):
      slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetGlyphScale(2)
      slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetTextScale(0)
      #slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsDisplayNode').SetSelectedColor(0,0,0)#black
  #lock marksup
  markupfiducials = slicer.util.getNodesByClass('vtkMRMLMarkupsFiducialNode')
  for i in range(len(markupfiducials)):
      slicer.mrmlScene.GetNthNodeByClass(i,'vtkMRMLMarkupsFiducialNode').SetLocked(1)

#4) Function to plot markups within a short distance of another:e.g. plotfilteredmarkups()

def pairwise_distances(X, Y):
    # Calculate Euclidean distances between all pairs of points in X and Y
    X_squared = np.sum(X**2, axis=1)
    Y_squared = np.sum(Y**2, axis=1)
    XY = np.dot(X, Y.T)
    distances = np.sqrt(X_squared[:, np.newaxis] + Y_squared - 2 * XY)
    return distances

def pointswithindist(array1, array2, maxdist):
    # Find points within threshold distance
    threshold_distance = maxdist/masterVolumeNode.GetSpacing()[0]# distance in scan units
    # Calculate pairwise distances between all points in array1_resampled and array2_resampled
    distances = pairwise_distances(array1, array2)
    #return distances
    
    # Find the indices of points within the threshold distance
    valid_indices = np.where(distances <= threshold_distance)
    #return valid_indices
    
    # Get the corresponding points from array1_resampled and array2_resampled
    array1_filtered = array1[valid_indices[0]]
    array2_filtered = array2[valid_indices[1]]
    
    # Remove duplicate points
    array1_filtered =np.unique(array1_filtered, axis = 0)
    array2_filtered =np.unique(array2_filtered, axis = 0)
    
    return array1_filtered, array2_filtered

#convert back to RAS
def plotfiltered(filtered,fiducnode):
  for i in range(0,len(filtered)):
    point_Ijk = [filtered[i][2], filtered[i][1], filtered[i][0]]
    #print(point_Ijk)
    # Get physical coordinates from voxel coordinates
    volumeIjkToRas = vtk.vtkMatrix4x4()
    masterVolumeNode.GetIJKToRASMatrix(volumeIjkToRas)
    point_VolumeRas = [0, 0, 0, 1]
    volumeIjkToRas.MultiplyPoint(np.append(point_Ijk,1.0), point_VolumeRas)
    # If volume node is transformed, apply that transform to get volume's RAS coordinates
    transformVolumeRasToRas = vtk.vtkGeneralTransform()
    slicer.vtkMRMLTransformNode.GetTransformBetweenNodes(masterVolumeNode.GetParentTransformNode(), None, transformVolumeRasToRas)
    point_Ras = transformVolumeRasToRas.TransformPoint(point_VolumeRas[0:3])
    # Add a markup at the computed position and print its coordinates
    fiducnode.AddControlPoint((point_Ras[0], point_Ras[1], point_Ras[2]))
    #print(point_Ras)
    #print(i)

def plotwithindist(dist,numpts):
  d1 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode',f'{pointListNode.GetName()}_within_{dist}_mm')
  d2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode',f'{pointListNode2.GetName()}_within_{dist}_mm')
  #reshape array for distance analysis
  seg1c = np.column_stack((seg1outline[0],seg1outline[1],seg1outline[2]))
  seg2c = np.column_stack((seg2outline[0],seg2outline[1],seg2outline[2]))
  #run function with set distance of interest
  filterseg1,filterseg2 = pointswithindist(seg1c,seg2c,dist)
  #plot unique point fitting the distance
  plotfiltered(resample_array(filterseg1,numpts),d1)
  d1.GetDisplayNode().SetSelectedColor(0,0,0)
  plotfiltered(resample_array(filterseg2,numpts),d2)
  d2.GetDisplayNode().SetSelectedColor(0,1.0,1)
  adjmarkupdisplayandlock()

#plot full contours
def plot_outlines():
  global pointListNode
  pointListNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode',f'{seg_1}_outline')
  global pointListNode2
  pointListNode2 = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode',f'{seg_2}_outline')
  plotfulloutline(seg1outline,pointListNode)
  adjmarkupdisplayandlock()
  plotfulloutline(seg2outline,pointListNode2)
  adjmarkupdisplayandlock()
