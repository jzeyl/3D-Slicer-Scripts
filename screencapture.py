#Capture a single view:
viewNodeID = 'vtkMRMLViewNode1'
import ScreenCapture
cap = ScreenCapture.ScreenCaptureLogic()
view = cap.viewFromNode(slicer.mrmlScene.GetNodeByID(viewNodeID))
cap.captureImageFromView(view,'c:/tmp/testj.png')

layoutManager = slicer.app.layoutManager()
threeDWidget = layoutManager.threeDWidget(0)
threeDView = threeDWidget.threeDView()

threeDView.yaw()#rotate thre 3D
cap.captureImageFromView(view,'c:/tmp/testj.png')

for i in range(20):
    threeDView.yaw()#rotate thre 3D
    threeDView.yaw()#rotate thre 3D
    cap.captureImageFromView(view,'c:/tmp/test'+'/'+ID+str(i)+'.png')#slicer.mrmlScene.GetRootDirectory()

import imageio
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('/path/to/movie.gif', images)

print('c:/tmp/test'+str(i)+'.png')

import ScreenCapture
ScreenCapture.ScreenCaptureLogic().captureSliceSweep(getNode('vtkMRMLSliceNodeRed'), -125.0, 75.0, 30, "c:/tmp", "image_%05d.png")




