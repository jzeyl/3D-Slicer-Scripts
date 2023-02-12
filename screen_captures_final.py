import os
import ScreenCapture

def create_directory(basepath,id):
    """
    Create directory where snapshots will end up. Specify the path and string with sample ID"
    Example usage:
    create_directory(basepath = 'C:/tmp/', id = "ID_HERE")
    create_directory(basepath = 'C:/Users/jeffz/Desktop/newtest/', id = "ID2_HERE")
    """
    global ID 
    ID = id
    # Set output folder and filename
    global outputScreenshotsFilenamePattern
    outputScreenshotsFilenamePattern = f"{basepath}{id}/"
    #outputGalleryFilename = "/tmp/gallery.png"
    global imagePathPattern
    imagePathPattern = outputScreenshotsFilenamePattern+f"{id}-%03d.png"
    # Create output folders
    filedir = os.path.dirname(outputScreenshotsFilenamePattern)
    if not os.path.exists(filedir):
        os.makedirs(filedir)

def capture_along_axial(slicedistance, frame = False):
    """
    Capture along axial axis at a . Slice disctance is the distance between captures in mm, with or without the control panel above

    Example usage:
    capture_along_axial(slicedistance = 10, frame = False)
    Output:
    Files labelled 'ID_01.png', 'ID_02.png' etc
    """
    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
    layoutName = "Red"
    #slicedistance desired in mm
    #slicedistance = 10 #mm
    widget = slicer.app.layoutManager().sliceWidget(layoutName)
    view = widget.sliceView()
    logic = widget.sliceLogic()
    bounds = [0,]*6
    logic.GetSliceBounds(bounds)
    #get number of slices needed to cover whole range
    rng = bounds[5]-bounds[4]#range of entire
    slices_entire = int(rng/slicedistance)
    #take a slice every 10 mm, starting at beginning of axial slice, i.e., bounds[4]
    for step in range(slices_entire):
        if frame == True:
            slicer.app.layoutManager().threeDWidget(0).threeDController().setVisible(True)
            slicer.app.layoutManager().sliceWidget("Red").sliceController().setVisible(True)
            slicer.app.layoutManager().sliceWidget("Green").sliceController().setVisible(True)
            slicer.app.layoutManager().sliceWidget("Yellow").sliceController().setVisible(True)
        else:
            slicer.app.layoutManager().threeDWidget(0).threeDController().setVisible(False)
            slicer.app.layoutManager().sliceWidget("Red").sliceController().setVisible(False)
            slicer.app.layoutManager().sliceWidget("Green").sliceController().setVisible(False)
            slicer.app.layoutManager().sliceWidget("Yellow").sliceController().setVisible(False)
        offset = bounds[4] + step*slicedistance
        print(f'slice at {offset} captured')
        logic.SetSliceOffset(offset)
        view.forceRender()
        cap = ScreenCapture.ScreenCaptureLogic()
        #cap.showViewControllers(False)
        cap.captureImageFromView(None, imagePathPattern % step)
        cap.showViewControllers(True)
    slicer.app.layoutManager().threeDWidget(0).threeDController().setVisible(True)
    slicer.app.layoutManager().sliceWidget("Red").sliceController().setVisible(True)
    slicer.app.layoutManager().sliceWidget("Green").sliceController().setVisible(True)
    slicer.app.layoutManager().sliceWidget("Yellow").sliceController().setVisible(True)

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

#adjust window size and fill slice to space
def set_windowsize(x,y):
    """Set window size viewer, to set size of screenshot. Can drag and re-maximize windows to reset window size
    Example usage:
    set_windowsize(1500,1500)
    """
    slicer.util.mainWindow().size=qt.QSize(2000,2000)
    reset_views()

def capture_single(pane, frame = False):
    """
    Capture single slice view or 3D view as "axial", "coronal", "saggital", or "3D"
    Example usage:
    capture_single(pane = "axial", frame = False)
    Example output:
    File labelled 'ID_saggital.png'
    """
    cap = ScreenCapture.ScreenCaptureLogic()
    if pane =="all":
        widget = slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutFourUpView)
        view = None
        view.forceRender()
        cap.captureImageFromView(None, f'{outputScreenshotsFilenamePattern}{ID}_{pane}.png')
    elif pane == "axial":
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpRedSliceView)
        reset_views()
        widget = slicer.app.layoutManager().sliceWidget("Red")        
        view = widget.sliceView()
        if frame ==True:
            slicer.app.layoutManager().sliceWidget("Red").sliceController().setVisible(True)
        else:
            slicer.app.layoutManager().sliceWidget("Red").sliceController().setVisible(False)
        cap.captureImageFromView(None, f'{outputScreenshotsFilenamePattern}{ID}_{pane}.png')
    elif pane == "coronal":
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpGreenSliceView)
        reset_views()
        widget = slicer.app.layoutManager().sliceWidget("Green")        
        view = widget.sliceView()
        if frame ==True:
            slicer.app.layoutManager().sliceWidget("Green").sliceController().setVisible(True)
        else:
            slicer.app.layoutManager().sliceWidget("Green").sliceController().setVisible(False)
        cap.captureImageFromView(None, f'{outputScreenshotsFilenamePattern}{ID}_{pane}.png')
    elif pane == "saggital":
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUpYellowSliceView)
        reset_views()
        widget = slicer.app.layoutManager().sliceWidget("Yellow")        
        view = widget.sliceView()
        if frame ==True:
            slicer.app.layoutManager().sliceWidget("Yellow").sliceController().setVisible(True)
        else:
            slicer.app.layoutManager().sliceWidget("Yellow").sliceController().setVisible(False)
        cap.captureImageFromView(None, f'{outputScreenshotsFilenamePattern}{ID}_{pane}.png')
    elif pane == "3D":
        slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
        reset_views()
        widget = slicer.app.layoutManager().threeDWidget(0)      
        #view = widget.threeDWidget(0)
        if frame ==True:
            slicer.app.layoutManager().threeDWidget(0).threeDController().setVisible(True)
        else:
            slicer.app.layoutManager().threeDWidget(0).threeDController().setVisible(False)
        cap.captureImageFromView(None, f'{outputScreenshotsFilenamePattern}{ID}_{pane}.png')
    slicer.app.layoutManager().threeDWidget(0).threeDController().setVisible(True)
    slicer.app.layoutManager().sliceWidget("Red").sliceController().setVisible(True)
    slicer.app.layoutManager().sliceWidget("Green").sliceController().setVisible(True)
    slicer.app.layoutManager().sliceWidget("Yellow").sliceController().setVisible(True)

# Capture 6 screenshots 
def capture_all3D():
    """
    Capture 3D views of at 6 set axes (front, back, top, bottom, left, right). No frames.
    Example usage:
    capture_all3D()

    Output:
    File labelled 'ID_front_view.png', 'ID_back_view.png' etc...
    """
    slicer.app.layoutManager().setLayout(slicer.vtkMRMLLayoutNode.SlicerLayoutOneUp3DView)
    threeDWidget = slicer.app.layoutManager().threeDWidget(0)
    threeDView = threeDWidget.threeDView()
    threeDView.resetCamera()
    originalZoomFactor = threeDView.zoomFactor
    threeDView.zoomFactor = 0.25
    threeDView.zoomIn()
    threeDView.setZoomFactor(originalZoomFactor)
    threeDViewNode = threeDWidget.mrmlViewNode()
    #below you can comment these 5 lines below if don't wnat to adjust 3D background, bounding box, etc.
    threeDViewNode.SetBackgroundColor(0,0,0)
    threeDViewNode.SetBackgroundColor2(0,0,0)
    threeDViewNode.SetAxisLabelsVisible(False)
    threeDViewNode.SetBoxVisible(False)
    threeDViewNode.SetOrientationMarkerType(threeDViewNode.OrientationMarkerTypeAxes)
    #
    axisIndex = [0,#viewfromleft 
    1,#viewfromrightside
    2,#back
    3,#front
    4,#from above
    5] #from below
    #rotate through 3D axes
    axisIndex2 = ["view_from_left",#viewfromleft 
    "view_from_right",#viewfromrightside
    "back_view",#back
    "front_view",#front
    "view_from_above",#from above
    "view_from_below"] #from below
    #
    cap = ScreenCapture.ScreenCaptureLogic()
    for screenshotIndex in range(len(axisIndex)):
        threeDView.rotateToViewAxis(axisIndex[screenshotIndex])#loop through views
        slicer.util.forceRenderAllViews()
        outputFilename = f'{outputScreenshotsFilenamePattern}{ID}_{axisIndex2[screenshotIndex]}.png' 
        cap.captureImageFromView(threeDView, outputFilename)

