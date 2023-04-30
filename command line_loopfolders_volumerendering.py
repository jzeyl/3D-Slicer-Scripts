import argparse
import os
import ScreenCapture

#Create command line arguments using argparse module and then parses them using parse_args() method.
parser = argparse.ArgumentParser(description='load volumes')
parser.add_argument('-f', '--folder', type=str, help='main volume path', required=True)
args = parser.parse_args()

#set the argument for the folder path
basedir = args.folder
dir_list = os.listdir(basedir)

#print files we're working with
print("Files and directories in '", basedir, "' :")
print(dir_list)

#loop through each of the folders in the base directories to prociess
for i in dir_list:
    #change colours of 3d viewer to be a black-white gradient
    viewNode = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode()
    viewNode.SetBackgroundColor(0,0,0)
    viewNode.SetBackgroundColor2(0,0,0)
    #remove bounding box and orientation axes labels (a,s,r)
    viewNode.SetBoxVisible(0)
    viewNode.SetAxisLabelsVisible(0)
    
    subfolder = f'{basedir}\\{i}'#get info for file naming
    print(subfolder)
    print(i)
    print(subfolder+'\\'+i)
    contents = os.listdir(subfolder)
    volpath = subfolder+'\\'+contents[0]#get 
    print(volpath)
    #load volume
    slicer.util.loadVolume(rf'{volpath}')

    #view the 3d layout only
    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)

    #center 3d view and slice views, to fill background
    def reset_views():
        layoutManager = slicer.app.layoutManager()
        threeDWidget = layoutManager.threeDWidget(0)
        threeDView = threeDWidget.threeDView()
        threeDView.resetFocalPoint()#just resets the focal point, camera might be tilted off still
        threeDView.resetCamera()#reset to snap to face on, anterior position
        #reset slice views
        for col in ["Red","Yellow","Green"]:
            slicer.app.layoutManager().sliceWidget(col).fitSliceToBackground()

    #apply function
    reset_views()

    # Set up volume rendering and display
    volumeNode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLScalarVolumeNode')
    volRenLogic = slicer.modules.volumerendering.logic()

    # Get/create volume rendering display node
    volRenLogic = slicer.modules.volumerendering.logic()
    displayNode = volRenLogic.CreateDefaultVolumeRenderingNodes(volumeNode)
    displayNode.SetVisibility(True)

    # Set up volume rendering preset
    displayNode.GetVolumePropertyNode().Copy(volRenLogic.GetPresetByName('CT-X-ray'))
    volpropertynode = slicer.mrmlScene.GetNthNodeByClass(0, 'vtkMRMLVolumePropertyNode')
    reset_views()

    # Set up scalar opacity mapping. This is a 6 point transfer function copied from settings after manual set to 210 minimum and 
    #ther upper and lower 
    scalarOpacity = vtk.vtkPiecewiseFunction()
    scalarOpacity.AllowDuplicateScalarsOn()
    scalarOpacity.AddPoint(volpropertynode.GetVolumeProperty().GetScalarOpacity().GetRange()[0], 0)#low bound of scalar range
    scalarOpacity.AddPoint(210, 0)#set threshold
    scalarOpacity.AddPoint(210, 0.02)#set threshold
    scalarOpacity.AddPoint(volpropertynode.GetVolumeProperty().GetScalarOpacity().GetRange()[1], 0.02)#upper bound of scalar range
    scalarOpacity.AddPoint(volpropertynode.GetVolumeProperty().GetScalarOpacity().GetRange()[1], 0)#upper bound of scalar range
    scalarOpacity.AddPoint(volpropertynode.GetVolumeProperty().GetScalarOpacity().GetRange()[1], 0)#upper bound of scalar range
    #print(scalarOpacity)
    displayNode.GetVolumePropertyNode().GetVolumeProperty().SetScalarOpacity(scalarOpacity)

    #center view
    reset_views()

    #Rotate the 3D View¶
    layoutManager = slicer.app.layoutManager()
    threeDWidget = layoutManager.threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.yaw()

    axisIndex = [0,#viewfromleft 
        1,#viewfromrightside
        2,#back
        3,#front
        4,#from above
        5]

    #various possible views of the 3d image
    cap = ScreenCapture.ScreenCaptureLogic()
    for screenshotIndex in range(len(axisIndex)):
        threeDView.rotateToViewAxis(axisIndex[screenshotIndex])#loop through views


    #save screenshots to disk
    cap = ScreenCapture.ScreenCaptureLogic()
    threeDView.rotateToViewAxis(3) #rotate to Anterior view
    outputFilename = subfolder+'\\'+i+'_anterior.png'
    outputFilename = rf'{outputFilename}'
    cap.captureImageFromView(threeDView, outputFilename)
    print("Screenshots saved to disk." + outputFilename)

    threeDView.rotateToViewAxis(1) #rotate to lateral view
    outputFilename = subfolder+'\\'+i+'_lateral.png'
    outputFilename = rf'{outputFilename}'
    cap.captureImageFromView(threeDView, outputFilename)
    print("Screenshots saved to disk." + outputFilename)
    
    #clear the scene before opening the next volume (next iteration of the loop)
    slicer.mrmlScene.Clear(0)
    slicer.mrmlScene.Clear(0)
