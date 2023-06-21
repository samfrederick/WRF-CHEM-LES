"""
"""
import os#, sys
import numpy as np
from scipy.stats import multivariate_normal
from netCDF4 import Dataset
from emiss_profiles import gauss3d_profile, checkerboard_profile
from json_io import read_initcond_json
import sys

# Access the command-line argument passed from the Bash script
CHEM_OPT = int(sys.argv[1])

def create_modified_netcdf():
    # Code via 
    # https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    # User Rich Signell

    # Modified by Sam Frederick, October 2022

    species_initcond = read_initcond_json(CHEM_OPT)
    variables_to_modify = [species for species in species_initcond.keys()]

    src = Dataset("wrfinput_d01")
    dst = Dataset("wrfinput_d01_new", "w")

    # Mesh grid dimensions
    xgrid = src.dimensions['west_east'].size
    ygrid = src.dimensions['south_north'].size
    zgrid = src.dimensions['bottom_top'].size

    # copy global attributes all at once via dictionary
    dst.setncatts(src.__dict__)
    # copy dimensions
    for variable_name, dimension in src.dimensions.items():
        dst.createDimension(
            variable_name, (len(dimension) if not dimension.isunlimited() else None))
    
    for variable_name, variable_attribs in src.variables.items():
        # copy all file data except for the excluded
        if variable_name not in variables_to_modify:
            x = dst.createVariable(variable_name, variable_attribs.datatype, variable_attribs.dimensions)
            dst[variable_name][:] = src[variable_name][:]
            # copy variable attributes all at once via dictionary
            dst[variable_name].setncatts(src[variable_name].__dict__)
        else:
            initcond_profile_attribs = species_initcond[variable_name]
            # for excluded variable modify the variable data values with tracer profile
            x = dst.createVariable(variable_name, variable_attribs.datatype, variable_attribs.dimensions)

            if initcond_profile_attribs['profile_type'] == 'checkerboard_profile':
                print(f'..assigning checkboard for {variable_name}')
                initcond_profile = checkerboard_profile(fx=initcond_profile_attribs['profile_fx'], 
                                                         fy=initcond_profile_attribs['profile_fy'], 
                                                         xgrid=xgrid, ygrid=ygrid, zgrid=zgrid, 
                                                         min_val=initcond_profile_attribs['profile_min_val'], 
                                                         max_val=initcond_profile_attribs['profile_max_val'], 
                                                         phase_shift=initcond_profile_attribs['profile_phase_shift'])
            else:
                raise ValueError('invalid profile type')

            dst[variable_name][:] = initcond_profile
            # copy variable attributes all at once via dictionary
            dst[variable_name].setncatts(src[variable_name].__dict__)
            
    src.close()
    dst.close()
    return

def update_netcdf_names():
    os.rename("wrfinput_d01", "wrfinput_d01_unmodifed")
    os.rename("wrfinput_d01_new", "wrfinput_d01")
    return

if __name__ == '__main__':
    print('\nModifing variable initial condition data\n')
    create_modified_netcdf()
    update_netcdf_names()
