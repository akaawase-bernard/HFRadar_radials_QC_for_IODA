
# This script opens and reads a sample ioda output file.

import os
import sys
import numpy as np
import time

if os.environ.get('LIBDIR') is not None:
    sys.path.append(os.environ['LIBDIR'])
    
import ioda

# grab arguments
#print(sys.argv)
#InFile = sys.argv[1]

InFile = 'data/ioda_hdf5_files/RDL_i_Rutgers_MVCO_2023_07_01_0100.hdf5'

# First task is to open the ioda file for reading. This is accomplished by constructing
g = ioda.Engines.HH.openFile(
    name = InFile,
    mode = ioda.Engines.BackendOpenModes.Read_Only)
og = ioda.ObsGroup(g)


# You can access the dimension variables to get coordinate values
locsDimName = "nlocs"
chansDimName = "nchans"

locsDimVar = og.vars.open(locsDimName)
chansDimVar = og.vars.open(chansDimName)

locsCoords = locsDimVar.readVector.int()
chansCoords = chansDimVar.readVector.int()

numLocs = len(locsCoords)
numChans = len(chansCoords)

print("INFO: locations dimension: ", locsDimName, " (", numLocs, ")")
time.sleep(1)
print("INFO:     coordinates: ")
for i in range(numLocs):
    print("INFO:        ", i, " --> ", locsCoords[i])
print("")

time.sleep(2)
print('Now getting ready for saved values checks')
time.sleep(1)
# We are interested in the following variables for diagnostics:


veluName = "ObsValue/waterZonalVelocity"
velvName = "ObsValue/waterMeridionalVelocity"

timeName = "MetaData/time"
latName = "MetaData/latitude"
lonName = "MetaData/longitude"

velvVar = og.vars.open(velvName)
timeVar = og.vars.open(timeName)
latVar = og.vars.open(latName)
lonVar = og.vars.open(lonName)

latData = latVar.readVector.float()      # produces a python list
lonData = lonVar.readVector.float()
timeData = timeVar.readVector.float()
velvData = velvVar.readVector.float()

print("INFO: input waterMeridionalVelocity variable: ", velvName, " (", np.shape(velvData), ")")
time.sleep(1)
print('')
print(velvData[:5])
print('')

print("INFO: timestamp : ", timeName, " (", np.shape(timeData), ")")
print('Sample of the timestamps', timeData[:5])
print('')

time.sleep(1)
print("INFO: latitude variable: ", latName, " (", len(latData), ")")
time.sleep(1)
print(latData[:5])

print('')

print("INFO: longitude variable: ", lonName, " (", len(lonData), ")")
print('')
print(lonData[:5])
print('')

