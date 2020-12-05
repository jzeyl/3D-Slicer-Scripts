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
viewNode.SetBackgroundColor2(0,0,0)

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

