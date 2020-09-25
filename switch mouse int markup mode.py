#switch mouse int markup mode

placeModePersistence = 1
slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)

#go back
placeModePersistence = 0
 slicer.modules.markups.logic().StartPlaceMode(placeModePersistence)