"""
Edit the emission profile for SO2 specified in the 'wrfchemi_00z_d01' file
"""

import numpy as np
import os, shutil
from netCDF4 import Dataset
from emiss_profiles import checkerboard_profile
from json_io import read_emiss_json
import sys

# Access the command-line argument passed from the Bash script
CHEM_OPT = int(sys.argv[1])

def create_modified_netcdf(src_path, output_path):
    # Code via 
    # https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    # User Rich Signell

    # Modified by Sam Frederick, October 2022, January 2023

    # emission rates in mol km^-2 hr^-1
    emiss_species = read_emiss_json(CHEM_OPT)
    variables_to_modify = [species for species in emiss_species.keys()]
                        
    # Make copy of the backup wrfchemi, load that in
    src_filename = os.path.basename(src_path)
    shutil.copy(src_path, f'{src_filename}_temp')
    src = Dataset(f'{src_filename}_temp')
    dst = Dataset(output_path, "w")

    # Mesh grid dimensions
    xgrid = src.dimensions['west_east'].size
    ygrid = src.dimensions['south_north'].size
    zgrid = 1

    print(f'Source file: {src_path}')
    print(f'Destination file: ./{output_path}')

    # copy global attributes all at once via dictionary
    dst.setncatts(src.__dict__)
    # copy dimensions
    for variable_name, dimension in src.dimensions.items():
        dst.createDimension(
            variable_name, (len(dimension) if not dimension.isunlimited() else None))
    # copy all file data except for the excluded
    for variable_name, variable_attribs in src.variables.items():
        if variable_name not in variables_to_modify:
            print(f'..copying over data for {variable_name}')
            x = dst.createVariable(variable_name, variable_attribs.datatype, variable_attribs.dimensions)
            dst[variable_name][:] = src[variable_name][:]
            # copy variable attributes all at once via dictionary
            dst[variable_name].setncatts(src[variable_name].__dict__)
        else:
            emiss_profile_attribs = emiss_species[variable_name]
            #modify variable values for E_SO2
            x = dst.createVariable(variable_name, variable_attribs.datatype, variable_attribs.dimensions)
            if emiss_profile_attribs['profile_type'] == 'checkerboard_profile':
                print(f'..assigning checkboard for {variable_name}')
                emissions_profile = checkerboard_profile(fx=emiss_profile_attribs['profile_fx'], 
                                                         fy=emiss_profile_attribs['profile_fy'], 
                                                         xgrid=xgrid, ygrid=ygrid, zgrid=zgrid, 
                                                         min_val=emiss_profile_attribs['profile_min_val'], 
                                                         max_val=emiss_profile_attribs['profile_max_val'], 
                                                         phase_shift=emiss_profile_attribs['profile_phase_shift'])
            else:
                raise ValueError('invalid profile type')
            # assign the profile for all timesteps (assuming time is first dimension)
            for i in range(dst[variable_name].shape[0]):
                dst[variable_name][i] = emissions_profile 
            # copy variable attributes all at once via dictionary
            dst[variable_name].setncatts(src[variable_name].__dict__)
                        
    src.close()
    dst.close()

    # delete the temporary file
    os.remove(f'{src_filename}_temp')

    return

if __name__ == '__main__':
    print('\nModifing emissions data\n')

    src_dir = f'/data/keeling/a/sf20/b/WRF4_4/WRF/test/em_les/anthro_emis/ANTHRO/wrfchem_files/chemopt-{CHEM_OPT}'
    for item in os.listdir(src_dir):
        if item.startswith('wrfchemi_'):
            src_file = item
            src_path = os.path.join(src_dir, src_file)
            output_path = src_file
            create_modified_netcdf(src_path, output_path)
    #update_netcdf_names()


    