#this script imports a tif stack file from a folder

folder = r'C:\Users\jeffzeyl\Desktop\copyoutput\Sept 27\EMU01'
ID = "EMU01"
spacing = 0.05500000
#folder = 'C:\\Users\\jeffzeyl\\Desktop\\copyoutput\\Jun17 batch\\CC209_2019'
filesinfolder = slicer.util.getFilesInDirectory(folder)

vol = "tif"
volfile = [i for i in filesinfolder if vol in i] 
volfile

#load volume
slicer.util.loadVolume(volfile[0])

#SET ID AND SPACING
#set up volume resolution
masterVolumeNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLScalarVolumeNode")
import itertools
imagespacing = [spacing]*3
masterVolumeNode.SetSpacing(imagespacing)#assign resolution to the volume
volumeScalarRange = masterVolumeNode.GetImageData().GetScalarRange()


#set slice to match footplate

#Set slice position and orientation from a normal vector and position
#This code snippet shows how to display a slice view defined by a normal vector and position in an anatomically sensible way: rotating slice view so that "up" direction (or "right" direction) is towards an anatomical axis.

def setSlicePoseFromSliceNormalAndPosition(sliceNode, sliceNormal, slicePosition, defaultViewUpDirection=None, backupViewRightDirection=None):
    """
    Set slice pose from the provided plane normal and position. View up direction is determined automatically,
    to make view up point towards defaultViewUpDirection.
    :param defaultViewUpDirection Slice view will be spinned in-plane to match point approximately this up direction. Default: patient superior.
    :param backupViewRightDirection Slice view will be spinned in-plane to match point approximately this right direction
        if defaultViewUpDirection is too similar to sliceNormal. Default: patient left.
    """
    # Fix up input directions
    if defaultViewUpDirection is None:
        defaultViewUpDirection = [0,0,1]
    if backupViewRightDirection is None:
        backupViewRightDirection = [-1,0,0]
    if sliceNormal[1]>=0:
        sliceNormalStandardized = sliceNormal
    else:
        sliceNormalStandardized = [-sliceNormal[0], -sliceNormal[1], -sliceNormal[2]]
    # Compute slice axes
    sliceNormalViewUpAngle = vtk.vtkMath.AngleBetweenVectors(sliceNormalStandardized, defaultViewUpDirection)
    angleTooSmallThresholdRad = 0.25 # about 15 degrees
    if sliceNormalViewUpAngle > angleTooSmallThresholdRad and sliceNormalViewUpAngle < vtk.vtkMath.Pi() - angleTooSmallThresholdRad:
        viewUpDirection = defaultViewUpDirection
        sliceAxisY = viewUpDirection
        sliceAxisX = [0, 0, 0]
        vtk.vtkMath.Cross(sliceAxisY, sliceNormalStandardized, sliceAxisX)
    else:
        sliceAxisX = backupViewRightDirection
    # Set slice axes
    sliceNode.SetSliceToRASByNTP(sliceNormalStandardized[0], sliceNormalStandardized[1], sliceNormalStandardized[2],
        sliceAxisX[0], sliceAxisX[1], sliceAxisX[2],
        slicePosition[0], slicePosition[1], slicePosition[2], 0)


sliceNode = getNode('vtkMRMLSliceNodeRed')

#file_input = open("C:\\Users\\jeffzeyl\\Desktop\\copyoutput\\Jun5 batch\\DCSB\\FPslice_normalsandpsotion.txt",'r')
file_input = open(folder+'\\FPslice_normalsandpsotion.txt','r')

list = file_input.readlines(0)
print(list)
list[0]

exec(list[0])#assign slicenormal
exec(list[1])#assign sliceposition

setSlicePoseFromSliceNormalAndPosition(sliceNode, sliceNormal, slicePosition)

#slicer.mrmlScene.GetNodeByID('vtkMRMLSliceNodeRed').SetRulerType(2)# add thick ruler

import os
slicedir = 'D:\\Analysis_plots\\3dslicerscreenshots\\'+ID
os.mkdir(slicedir)

import ScreenCapture
viewNodeID = 'vtkMRMLSliceNodeRed'
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,slicedir+'\\'+ID+'redsliceFP.tif')

#now select points along columella

slicer.modules.markups.logic().StartPlaceMode(1)


#3 points
def UpdateSlicePlane(param1=None, param2=None):
  # Get point positions as numpy array
  import numpy as np
  nOfFiduciallPoints = markups.GetNumberOfFiducials()
  if nOfFiduciallPoints < 3:
    return  # not enough points
  points = np.zeros([3,nOfFiduciallPoints])
  for i in range(0, nOfFiduciallPoints):
    markups.GetNthFiducialPosition(i, points[:,i])
  # Compute plane position and normal
  planePosition = points.mean(axis=1)
  planeNormal = np.cross(points[:,1] - points[:,0], points[:,2] - points[:,0])
  planeX = points[:,1] - points[:,0]
  sliceNode.SetSliceToRASByNTP(planeNormal[0], planeNormal[1], planeNormal[2],
    planeX[0], planeX[1], planeX[2],
    planePosition[0], planePosition[1], planePosition[2], 0)

# Get markup node AND MARKUPS
sliceNode = slicer.app.layoutManager().sliceWidget('Red').mrmlSliceNode()
markups = slicer.util.getNode('F')

# Update slice plane manually
UpdateSlicePlane()

import ScreenCapture
viewNodeID = 'vtkMRMLSliceNodeRed'
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,slicedir+'\\'+ID+'redslicethroughcol.tif')

#CA
viewNodeID = 'vtkMRMLSliceNodeRed'
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,slicedir+'\\'+ID+'redslicethroughCA.tif')
