# Python commands in this file are executed on Slicer startup

# Examples:
#
# Load a scene file
# slicer.util.loadScene('c:/Users/SomeUser/Documents/SlicerScenes/SomeScene.mrb')
#
# Open a module (overrides default startup module in application settings / modules)
#slicer.util.mainWindow().moduleSelector().selectModule('SegmentEditor')
#
slicer.util.findChild(slicer.util.mainWindow(), 'LogoLabel').visible = False#remove logo to make space

#change colours of 3d viewer to be a black-white gradient
viewNode = slicer.app.layoutManager().threeDWidget(0).mrmlViewNode()
viewNode.SetBackgroundColor(1,1,1)
viewNode.SetBackgroundColor2(1,1,1)


slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
threeDWidget = slicer.app.layoutManager().threeDWidget(0)
threeDView = threeDWidget.threeDView()
threeDView.resetCamera()
originalZoomFactor = threeDView.zoomFactor
threeDView.zoomFactor = 0.25
threeDView.zoomIn()
threeDView.setZoomFactor(originalZoomFactor)
threeDViewNode = threeDWidget.mrmlViewNode()
threeDViewNode.SetBackgroundColor(0,0,0)
threeDViewNode.SetBackgroundColor2(0,0,0)
threeDViewNode.SetAxisLabelsVisible(False)
threeDViewNode.SetBoxVisible(False)
threeDViewNode.SetOrientationMarkerType(threeDViewNode.OrientationMarkerTypeAxes)
#

#remove bounding box and orientation axes (a,s,r)
viewNode.SetBoxVisible(0)
viewNode.SetAxisLabelsVisible(0)


#Customize keyboard shortcuts
#Keyboard shortcuts can be specified for activating any Slicer feature by adding a couple of lines to your .slicerrc file.
#For example, this script registers Ctrl+b, Ctrl+n, Ctrl+m, Ctrl+, keyboard shortcuts to switch between red, yellow, green, and 4-up view layouts.

shortcuts = [
    ('Ctrl+b', lambda: slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)),
    ('Ctrl+n', lambda: slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpYellowSliceView)),
    ('Ctrl+m', lambda: slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpGreenSliceView)),
    ('Ctrl+,', lambda: slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView))
    ]

for (shortcutKey, callback) in shortcuts:
    shortcut = qt.QShortcut(slicer.util.mainWindow())
    shortcut.setKey(qt.QKeySequence(shortcutKey))
    shortcut.connect( 'activated()', callback)


import os
import SampleData
import ScreenCapture

def lightbox(basedir):
    baseScreenshotsFilenamePattern = basedir+"/screenshots/screenshot_%d.png"# Set output folder and filename pattern
    baseGalleryFilename = basedir+"/screenshots/gallery.png"
    # Create output folders
    filedir = os.path.dirname(baseScreenshotsFilenamePattern)
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    # Capture screenshots
    numberOfScreenshots = 6
    axisIndex = [0, 1,2,3,4,5]  # order of views in the gallery image
    cap = ScreenCapture.ScreenCaptureLogic()
    for screenshotIndex in range(numberOfScreenshots):
        threeDView.rotateToViewAxis(axisIndex[screenshotIndex])#loop through w
        slicer.util.forceRenderAllViews()
        outputFilename = baseScreenshotsFilenamePattern % screenshotIndex
        cap.captureImageFromView(threeDView, outputFilename)
    # Create gallery view of all images
    cap.createLightboxImage(2,  # number of columns
        os.path.dirname(baseScreenshotsFilenamePattern),
        os.path.basename(baseScreenshotsFilenamePattern),
        numberOfScreenshots,
        baseGalleryFilename)


