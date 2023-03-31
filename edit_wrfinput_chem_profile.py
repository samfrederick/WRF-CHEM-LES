"""
"""
import os, sys
import numpy as np
from scipy.stats import multivariate_normal
from netCDF4 import Dataset
from emiss_profiles import gauss3d_profile, checkerboard_profile

try:
    profile_type = sys.argv[1]
except IndexError:
    print ("Tracer profile function not specified!")
    sys.exit()
try:
    species = sys.argv[2]
except IndexError:
    print ("Tracer species not specified!")
    sys.exit()

def create_modified_netcdf():
    # Code via 
    # https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    # User Rich Signell

    # Modified by Sam Frederick, October 2022

    # Checkerboard profile variables
    fx = 1
    fy = 1
    min_val = 0.01
    max_val = 100

    # MESH VARIABLES
    xgrid = 99
    ygrid = 99
    zgrid = 199
    
    tracer_profile = profile_func(fx=fx, fy=fy, xgrid=xgrid, ygrid=ygrid, 
                                  zgrid=zgrid, min_val=min_val, max_val=max_val)

    toexclude = [species]

    src = Dataset("wrfinput_d01")
    dst = Dataset("wrfinput_d01_new", "w")

    # copy global attributes all at once via dictionary
    dst.setncatts(src.__dict__)
    # copy dimensions
    for name, dimension in src.dimensions.items():
        dst.createDimension(
            name, (len(dimension) if not dimension.isunlimited() else None))
    
    for name, variable in src.variables.items():
        # copy all file data except for the excluded
        if name not in toexclude:
            x = dst.createVariable(name, variable.datatype, variable.dimensions)
            dst[name][:] = src[name][:]
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(src[name].__dict__)
        else:
            # for excluded variable modify the variable data values with tracer profile
            x = dst.createVariable(name, variable.datatype, variable.dimensions)
            dst[name][:] = tracer_profile
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(src[name].__dict__)
            
    src.close()
    dst.close()
    return

def update_netcdf_names():
    os.rename("wrfinput_d01", "wrfinput_d01_unmodifed")
    os.rename("wrfinput_d01_new", "wrfinput_d01")
    return

if __name__ == '__main__':
    profile_func = globals()[profile_type]
    print(f'\nModifing initial condition {species} tracer gas data\n')
    print(f'Using {profile_type}() method\n')
    create_modified_netcdf()
    update_netcdf_names()