#script to change background color in 3D slicer

viewNode = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode()
viewNode.SetBackgroundColor(1,1,1)
viewNode.SetBackgroundColor2(0,0,0)

#remove bounding box
viewNode.SetBoxVisible(0)
viewNode.SetAxisLabelsVisible(0)

#CAPTURE VIEWS
#Capture
Capture the full Slicer screen and save it into a file
 img = qt.QPixmap.grabWidget(slicer.util.mainWindow()).toImage()
 img.save('c:/tmp/test.png')
#Capture all the views save it into a file:
import ScreenCapture
cap = ScreenCapture.ScreenCaptureLogic()
cap.showViewControllers(False)
cap.captureImageFromView(None,'c:/tmp/test.png')
cap.showViewControllers(True)
#Capture a single view:
viewNodeID = 'vtkMRMLViewNode1'
import ScreenCapture
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,'c:/tmp/test.png')
#Common values for viewNodeID: vtkMRMLSliceNodeRed, vtkMRMLSliceNodeYellow, vtkMRMLSliceNodeGreen, vtkMRMLViewNode1, vtkMRMLViewNode2. The ScreenCapture module can also create video animations of rotating views, slice sweeps, etc.#

##Capture a slice view sweep into a series of PNG files - for example, Red slice view, 30 images, from position -125.0 to 75.0, into c:/tmp folder, with name image_00001.png, image_00002.png, ...
import ScreenCapture
ScreenCapture.ScreenCaptureLogic().captureSliceSweep(getNode('vtkMRMLSliceNodeRed'), -125.0, 75.0, 30, "c:/tmp", "image_%05d.png")
#Capture 3D view into PNG file with transparent background
renderWindow = slicer.app.layoutManager().threeDWidget(0).threeDView().renderWindow()
renderWindow.SetAlphaBitPlanes(1)
wti = vtk.vtkWindowToImageFilter()
wti.SetInputBufferTypeToRGBA()
wti.SetInput(renderWindow)
writer = vtk.vtkPNGWriter()
writer.SetFileName("c:/tmp/screenshot.png")
writer.SetInputConnection(wti.GetOutputPort())
writer.Write()

string = "run("Image Sequence...", "open=[E:/0backof head analyses/5_Feb7crops/CFranc-01-2019/cfranc-01-2019 backofhead0000.tif] sort")"
