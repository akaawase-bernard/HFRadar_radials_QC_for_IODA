"""
Coverts the ascii to IODA convension
"""


import os
import sys

if os.environ.get('LIBDIR') is not None:
    sys.path.append(os.environ['LIBDIR'])

import ioda
import numpy as np
import numpy.matlib
import pandas as pd
from hfradarpy.radials import Radial


#tools
def ascii2arrays(radial_files):
    '''
    convert the noaa hfradar ascii to arrays for operations
    '''

    r = Radial(radial_files)
    df = pd.DataFrame(r.data)
    
    # List of columns to keep
    columns_to_keep = ['LOND', 'LATD', 'VELU', 'VELV', 'ESPC', 'ETMP', 'ERSC', 'ERTC']
    
    # Create a new DataFrame with only the desired columns
    qc_df = df[columns_to_keep]
    diagnostic = pd.DataFrame(r.diagnostics_hardware)
    
    LOND, LATD, VELU, VELV, ESPC, ETMP, ERSC, ERTC = qc_df.iloc[:, 0:8].values.T
    diagnostic = pd.DataFrame(r.diagnostics_hardware)
    timestamp = diagnostic['datetime'] [len(diagnostic['datetime'])//2] #extract the time 
    
    time0 = np.array([np.datetime64(timestamp)], dtype='datetime64[ns]')
    return LOND, LATD, VELU, VELV, ESPC, ETMP, ERSC, ERTC, time0


# # run high frequency radar qartod tests on open radial file

# qc_values = dict(
#     qc_qartod_avg_radial_bearing=dict(reference_bearing=151, warning_threshold=15, failure_threshold=30),
#     qc_qartod_radial_count=dict(min_count=75.0, low_count=225.0),
#     qc_qartod_maximum_velocity=dict(max_speed=300.0, high_speed=100.0),
#     qc_qartod_spatial_median=dict(smed_range_cell_limit=2.1, smed_angular_limit=10, smed_current_difference=30),
#     qc_qartod_temporal_gradient=dict(gradient_temp_fail=32, gradient_temp_warn=25),
#     qc_qartod_primary_flag=dict(include=['qc_qartod_syntax', 'qc_qartod_valid_location', 'qc_qartod_radial_count',
#                                          'qc_qartod_maximum_velocity', 'qc_qartod_spatial_median'])
# )
# r.initialize_qc()
# r.qc_qartod_syntax()
# r.qc_qartod_maximum_velocity(**qc_values['qc_qartod_maximum_velocity'])
# r.qc_qartod_valid_location()
# r.qc_qartod_radial_count(**qc_values['qc_qartod_radial_count'])
# r.qc_qartod_spatial_median(**qc_values['qc_qartod_spatial_median'])
# r.qc_qartod_temporal_gradient(files[1]) #pass the previous hourly radial to this one
# r.qc_qartod_avg_radial_bearing(**qc_values['qc_qartod_avg_radial_bearing'])
# r.qc_qartod_primary_flag(**qc_values['qc_qartod_primary_flag'])

# tds = r.to_xarray('gridded', enhance=True).squeeze()


#set paths
ascii_path = "data/hfradar_ascii/" #path to where ascii lives
hdf5_root = "data/ioda_hdf5_files/" #where to save hdf5 files


file_list = [filename for filename in os.listdir(ascii_path) if "RDL" in filename]
print('starting task ...')
for item in range(len(file_list)) :

    radial_files = [os.path.join(ascii_path, file) for file in os.listdir(ascii_path) if file.startswith("RDL")]
    hfd5_name = file_list[item].split('.')[0] + '.hdf5'
    hdf5_path = hdf5_root + hfd5_name #where the data is saved

    g = ioda.Engines.HH.createFile(name = hdf5_path,
                                   mode = ioda.Engines.BackendCreateModes.Truncate_If_Exists)


    #read the data (1d arrrays)
    LOND, LATD, VELU, VELV, ESPC, ETMP, ERSC, ERTC, timestamp = ascii2arrays(radial_files[item])
    time = np.matlib.repmat(timestamp, len(LOND), 1)






    
    # We have opened the file, but now we want to turn it into an ObsGroup.
    numLocs = len(LOND)
    numChans = 1

    # This is a list of the dimensions that we want in our ObsGroup.
    newDims = [ioda.NewDimensionScale.int32('nlocs', numLocs, ioda.Unlimited, numLocs),
               ioda.NewDimensionScale.int32('nchans', numChans, numChans, numChans)]

    # ObsGroup.generate takes a Group argument 
    og = ioda.ObsGroup.generate(g, newDims)

    # NewDimensionScale calls.
    nlocsVar = og.vars.open('nlocs')
    nchansVar = og.vars.open('nchans')

    # Just setting some sensible defaults: compress the stored data and use
    p1 = ioda.VariableCreationParameters()
    p1.compressWithGZIP()
    p1.setFillValue.float(-32767)

    #  Next let's create the variables. 
    veluName = "ObsValue/waterZonalVelocity"
    velvName = "ObsValue/waterMeridionalVelocity"
    espcName = "ObsError/spatialQuality"
    etmpName = "ObsError/temporalQuality"
    erscName = "ObsError/spatialCount"
    ertcName = "ObsError/temporalCount"

    timeName = "MetaData/time"
    latName = "MetaData/latitude"
    lonName = "MetaData/longitude"

    # We attach the appropriate scales with the scales option.
    veluVar = g.vars.create(veluName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)
    velvVar = g.vars.create(velvName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)
    espcVar = g.vars.create(espcName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)
    etmpVar = g.vars.create(etmpName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)
    erscVar = g.vars.create(erscName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)
    ertcVar = g.vars.create(ertcName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)
    timeVar = g.vars.create(timeName, ioda.Types.float, scales=[nlocsVar, nchansVar], params=p1)

    latVar = g.vars.create(latName, ioda.Types.float, scales=[nlocsVar], params=p1)
    lonVar = g.vars.create(lonName, ioda.Types.float, scales=[nlocsVar], params=p1)

    # Let's set some attributes on the variables
    veluVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    veluVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("waterZonalVelocity")
    veluVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str("m s-1")
    veluVar.atts.create("valid_range", ioda.Types.float, [2]).writeVector.float([-3.0, 3.0])

    velvVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    velvVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("waterMeridionalVelocity")
    velvVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str("m s-1")
    velvVar.atts.create("valid_range", ioda.Types.float, [2]).writeVector.float([-3.0, 3.0])

    espcVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    espcVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("spatialQuality")
    espcVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str(" std")
    espcVar.atts.create("valid_range", ioda.Types.float, [2]).writeVector.float([-100.0, 100.0])

    etmpVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    etmpVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("temporalQuality")
    etmpVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str(" std")
    etmpVar.atts.create("valid_range", ioda.Types.float, [2]).writeVector.float([-100.0, 100.0])

    erscVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    erscVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("spatialCount")
    erscVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str(" ")
    erscVar.atts.create("valid_range", ioda.Types.int, [2]).writeVector.float([0, 100])

    ertcVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    ertcVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("temporalCount")
    ertcVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str(" ")
    espcVar.atts.create("valid_range", ioda.Types.int, [2]).writeVector.float([0, 100])

    timeVar.atts.create("coordinates", ioda.Types.str, [1]).writeDatum.str("longitude latitude time nchans")
    timeVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("dateTime")
    timeVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str("seconds since 1970-01-01T00:00:00Z ")

    latVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("latitude")
    latVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str("degrees_north")
    latVar.atts.create("valid_range", ioda.Types.float, [2]).writeVector.float([-90, 90])

    lonVar.atts.create("long_name", ioda.Types.str, [1]).writeDatum.str("degrees_east")
    lonVar.atts.create("units", ioda.Types.str, [1]).writeDatum.str("degrees_north")
    lonVar.atts.create("valid_range", ioda.Types.float, [2]).writeVector.float([-360, 360])

    # Write the data into the variables.
    lonVar.writeNPArray.float(LOND)
    latVar.writeNPArray.float(LATD)
    veluVar.writeNPArray.float(VELU)
    velvVar.writeNPArray.float(VELV)
    espcVar.writeNPArray.float(ESPC)
    etmpVar.writeNPArray.float(ETMP)
    erscVar.writeNPArray.float(ERSC)
    ertcVar.writeNPArray.float(ERTC)
    timeVar.writeNPArray.float(timestamp)
    print('Done working with file', str(hfd5_name))
