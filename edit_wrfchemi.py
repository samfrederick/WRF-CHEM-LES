"""
Edit the emission profile for SO2 specified in the 'wrfchemi_00z_d01' file
"""

import numpy as np
import os, sys
from netCDF4 import Dataset
from emiss_profiles import checkerboard_profile


def create_modified_netcdf():
    # Code via 
    # https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    # User Rich Signell

    # Modified by Sam Frederick, October 2022, January 2023
    
    emissions_profile = checkerboard_profile(fx=1, fy=1, xgrid=99, ygrid=99, 
                                             zgrid=1, max_val=100, min_val=0.01)

    toexclude = ['E_SO2']

    src = Dataset("wrfchemi_00z_d01")
    dst = Dataset("wrfchemi_00z_d01_modified", "w")

    # copy global attributes all at once via dictionary
    dst.setncatts(src.__dict__)
    # copy dimensions
    for name, dimension in src.dimensions.items():
        dst.createDimension(
            name, (len(dimension) if not dimension.isunlimited() else None))
    # copy all file data except for the excluded
    for name, variable in src.variables.items():
        if name not in toexclude:
            x = dst.createVariable(name, variable.datatype, variable.dimensions)
            dst[name][:] = src[name][:]
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(src[name].__dict__)
        else:
            x = dst.createVariable(name, variable.datatype, variable.dimensions)

            # assign the profile for all timesteps (assuming time is first dimension)
            for i in range(dst[name].shape[0]):
                dst[name][i] = emissions_profile 
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(src[name].__dict__)
            
    src.close()
    dst.close()
    return

def update_netcdf_names():
    os.rename("wrfchemi_00z_d01", "wrfchemi_00z_d01_unmodified")
    os.rename("wrfchemi_00z_d01_modified", "wrfchemi_00z_d01")
    return

if __name__ == '__main__':
    print('\nModifing emissions data\n')
    create_modified_netcdf()
    update_netcdf_names()