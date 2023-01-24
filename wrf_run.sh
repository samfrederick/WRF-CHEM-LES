#!/bin/bash
#SBATCH --job-name=wrf
#SBATCH --nodes=2-2
#SBATCH -n 64
#SBATCH --partition=sesempi
#SBATCH --time=6:00:00
#SBATCH --mem-per-cpu=2000
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END
#SBATCH --mail-user=sf20@illinois.edu

now=$(date +"%T")
echo "Start time : $now"
echo ${run}
source ~/.bashrc
#free the system to have unlimited memory requests
ulimit -s -S unlimited
#make permissions group readable on output files
umask 022
#load libraries that you compiled with
module purge
module load gnu/hdf5-1.10.6-gnu-9.3.0
module load gnu/netcdf4-4.7.4-gnu-9.3.0
module load gnu/openmpi-3.1.6-gnu-9.3.0
#path to WRF simulation
cd /data/keeling/a/sf20/b/WRF4_4/WRF/test/em_les

# Make sure there is a copy of makekeelingloads.csh in your em_real directory
source makekeelingloads.csh
export MKL_DEBUG_CPU_TYPE=5
export MKL_CBWR=COMPATIBLE

time mpirun -np 16 ./ideal.exe 
# modifying emissions data in wrfinput_d01 
python edit_wrfinput_chem_profile.py checkerboard_profile
time mpirun -np 64 ./wrf.exe
python create_move_output_files.py
now=$(date +"%T") echo "End time : $now"
