#shell
1. enter_singularity.sh takes you into the container
2. The go_ioda.sh sets paths needed to use ioda. This must must be ran first so as to use teh ioda package.
3. request_pullHFradar_data.sh is used to request processors from storrs hpc to download the hfradardata... it maintains the tree as on noaa site

#preview data using 
3. To view the data use h5dump --contents filename

you can run the python script using: 
>> python noaa_hfradar2ioda.py

edit with:
>> nano noaa_hfradar2ioda.py

place the ascii into the data file. 
my code on the hpc lives here:
/home/bernard/jedi/tutorials/ioda_python_api/my_code

