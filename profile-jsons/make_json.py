from netCDF4 import Dataset
import json
import os, sys

# Access the command-line argument passed from the Bash script
CHEM_OPT = sys.argv[1]
CHEM_OPT = int(CHEM_OPT)

data = Dataset(f'/data/keeling/a/sf20/b/WRF4_4/WRF/test/em_les/anthro_emis/ANTHRO/wrfchem_files/chemopt-{CHEM_OPT}/wrfchemi_00z_d01')

variables = [var for var in list(data.variables.keys()) if var.startswith('E_')]

emiss_dict = {}
initcond_dict = {}
for var in variables:
    emiss_dict[var] = {
        "profile_type": "checkerboard_profile",
        "profile_fx": 1,
        "profile_fy": 1,
        "profile_min_val": 0.0,
        "profile_max_val": 10.0,
        "profile_phase_shift": False
    }

    initcond_dict[var.replace('E_', '').lower()] = {
                                "profile_type": "checkerboard_profile",
                                "profile_fx": 1,
                                "profile_fy": 1,
                                "profile_min_val": 0.0,
                                "profile_max_val": 100.0,
                                "profile_phase_shift": False
                            }

directory_name = f'chemopt{CHEM_OPT}'
if not os.path.exists(directory_name):
    os.makedirs(directory_name)

with open(f'{directory_name}/species_emiss_profile_data.json', 'w') as outfile:
        json.dump(emiss_dict, outfile, indent=4)
with open(f'{directory_name}/species_initcond_profile_data.json', 'w') as outfile:
        json.dump(initcond_dict, outfile, indent=4)
