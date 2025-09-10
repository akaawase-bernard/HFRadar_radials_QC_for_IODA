#!/bin/bash
#SBATCH --partition=lo-core                    # Name of Partition
#SBATCH --ntasks=90                           # Maximum CPU cores for job
#SBATCH --nodes=1                             # Ensure all cores are from the same node
#SBATCH --time=4:40:60                    # Job should run for up to 2 days (for example)
#SBATCH --constraint='epyc128'                # Target the Skylake node architecture
#SBATCH --mail-type=END                       # Event(s) that triggers email notification (BEGIN,END,FAIL,ALL)
#SBATCH --mail-user=bernard.akaawase@uconn.edu    # Destination email address
#SBATCH --mem=492G                           # Request 500GB of available RAM on an AMD EPYC node with 128 cores
./download_noaa_data.sh   # Replace with your application's commands

