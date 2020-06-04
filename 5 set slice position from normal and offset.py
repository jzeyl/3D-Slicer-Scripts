Set slice position and orientation from a normal vector and position
This code snippet shows how to display a slice view defined by a normal vector and position in an anatomically sensible way: rotating slice view so that "up" direction (or "right" direction) is towards an anatomical axis.

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