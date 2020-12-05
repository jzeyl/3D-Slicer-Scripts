#script taken from the nightly script repositoy of 3D Slicer

#Set slice position and orientation from 3 markup fiducials
#Drop 3 markup points in the scene and copy-paste the code below into the Python console. After this, as you move the markups you’ll see the red slice view position and orientation will be set to make it fit to the 3 points.

# Update plane from fiducial points ###################FUNCTION
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

# Update slice plane automatically whenever points are changed
markupObservation = [markups, markups.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, UpdateSlicePlane, 2)]
