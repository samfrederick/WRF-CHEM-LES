module load gnu/hdf5-1.10.6-gnu-9.3.0
module load gnu/netcdf4-4.7.4-gnu-9.3.0
module load gnu/openmpi-3.1.6-gnu-9.3.0
export NETCDF=/sw/netcdf4-4.7.4-gnu-9.3.0/
export HDF5PATH=/sw/hdf5-1.10.6-gnu-9.3.0/
export DIR=/data/keeling/a/sf20/b/WRF4_4/Build_WRF/LIBRARIES
export CC=gcc
export CXX=g++
export FC=gfortran
export FCFLAGS=-m64
export F77=gfortran
export FFLAGS=-m64
export JASPERLIB=$DIR/grib2/lib
export JASPERINC=$DIR/grib2/include
export LDFLAGS=-L$DIR/grib2/lib
export CPPFLAGS=-I$DIR/grib2/include
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/data/keeling/a/jamessg3/WRF/Build_WRF/LIBRARIES/grib2/lib:/sw/netcdf4-4.7.4-gnu-9.3.0/

