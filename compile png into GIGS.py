
#make list of imagepaths
imgpaths = []
for i in range(0,len(os.listdir(gifdir))):
    imgpaths.append(gifdir+'\\'+os.listdir(gifdir)[i])

import subprocess
subprocess.run(imgpaths, universal_newlines=True, input=data)

imgpaths = ['D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif0.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif1.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif2.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif3.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif4.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif5.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif6.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif7.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif8.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif9.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif10.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif11.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif12.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif13.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif14.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif15.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif16.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif17.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif18.png', 'D:\\Analysis_plots\\3dslicerscreenshots\\BO-02-2019\\BO-02-2019gif\\BO-02-2019gif19.png']
gifdir

from PIL import Image, ImageDraw
# save to GIF in here
images = []#make list of image objects

for n in imgpaths: #populat the list
    frame = Image.open(n)
    images.append(frame)

# Save the frames as an animated GIF
images[0].save('E:\\Analysis_plots\\3dslicerscreenshots\\ADP-01-2019\\ADP-01-2019gif'+'\\ID.gif',
               save_all=True,
               append_images=images[1:],
               duration=100,
               loop=0)



# Disable slice annotations immediately
slicer.modules.DataProbeInstance.infoWidget.sliceAnnotations.sliceViewAnnotationsEnabled=False
slicer.modules.DataProbeInstance.infoWidget.sliceAnnotations.updateSliceViewFromGUI()
# Disable slice annotations persistently (after Slicer restarts)
settings = qt.QSettings()
settings.setValue('DataProbe/sliceViewAnnotations.enabled', 0)


#views nodes:
#3d 'vtkMRMLViewNode1'
#'vtkMRMLSliceNodeRed'
#'vtkMRMLSliceNodeYellow'
#'vtkMRMLSliceNodeGreen'

#Capture a single slice view:
#create directory for pics
import os
slicedir = 'D:\\Analysis_plots\\3dslicerscreenshots\\'+ID
os.mkdir(slicedir)

import ScreenCapture
viewNodeID = 'vtkMRMLSliceNodeRed'
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,slicedir+'\\'+ID+'redslice.tif')

import ScreenCapture
viewNodeID = 'vtkMRMLSliceNodeRed'
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,slicedir+'\\'+ID+'redslice2.tif')

#ScreenCapture.ScreenCaptureLogic().viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID)).createVideo()



threeDView.yaw()#rotate thre 3D
cap.captureImageFromView(view,'c:/tmp/testj.png')


os.listdir(gifdir)[0]

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

listdir_fullpath(d)

#slice sweep
import ScreenCapture
ScreenCapture.ScreenCaptureLogic().captureSliceSweep(getNode('vtkMRMLSliceNodeRed'), -125.0, 75.0, 30, "c:/tmp", "image_%05d.png")

