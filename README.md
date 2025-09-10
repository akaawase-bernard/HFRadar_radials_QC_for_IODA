# High-Frequency Radar – Surface Current Observations


This repository contains scripts and documentation related to the code we developed for downloading public HFRadar data, performing data quality control, and writing the data into the IODA format (HDF5).
The data quality control (QC) is performed using the open-source HFRadarPy toolbox.

The QC involves:
1. Checks for file corruption
2. Land masking
3. Bounds check filter
4. Temporal rate of change information and spatial median filtering to remove outliers

The final HDF5 files contain position, radial velocities, and uncertainty information.
The quality-controlled files are written using the Python API JEDI library within the Singularity Container.


## Usage

First, enter the singularity container after logging into HPC. NB: the image is called `jedi-tutorial_latest.sif`. You can pull the JEDI tutorial from the [JEDI Website](https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/1.1.0/learning/tutorials/level2/dev-container.html) or use the file available in the current working directory. You might also have the right permission to copy it to your home directory??!. 


Run the `./enter_singularity.sh` script to enter the container, followed by `./go_ioda.sh` which sets the paths. You might need to first make the shell scripts executables by granting proper permissions (e.g `chmod 700 enter_singularity.sh`). 

The `./download_noaa_data.sh` downloads all available data while maintaining the online directory trees. Kindly edit the portion of the code that corresponds to `directory-prefix= YOUR_PATH_HERE` to point to your scratch space before running this script. 

If using Storrs HPC, you may also want to request multiple processors before running this job, [how to submit batch jobs on storrs HPC](https://kb.uconn.edu/space/SH/26032963685/SLURM+Guide) A sample script for requesting and downloading the data in batch is also provided `request_pullHFradar_data.sh`

### Other important scripts:

To download just a few data files from public archives use the `fetch_HFRadar_ascii.py` 

To convert the downloaded ASCII files to IODA format (HDF5) use the `noaa_hfradar2ioda.py`

To read the created IODA compliant file use `read_ioda_outputFile.py`

You can access these scripts in the `./src` directory.
To run them you need to do something along the lines:
`>> python fetch_HFRadar_ascii.py`

## Test

In the `./test_qc` directory, you will find an example notebook that runs QC on the HFRadial data, the plots made during this exercise can be found in the `./src/figs` directory. This is a handy script for visual inspections (i.e. the before and after QC).