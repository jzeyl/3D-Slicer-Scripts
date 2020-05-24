
spacing = input()
#('Substack (368-749)0000', (MRMLCorePython.vtkMRMLScalarVolumeNode)000001CDEED399A8)
vol_node = slicer.util.getNodesByClass('vtkMRMLScalarVolumeNode')# instead of having to put the name of the volume, it pulls the volume class
import itertools
imagespacing = list(itertools.repeat(spacing, 3))
vol_node[0].SetSpacing(imagespacing)#assign resolution to the volume. Since getNodesbyclass pulls a list, I specify the first instance, 0
