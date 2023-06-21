import os, sys
from datetime import datetime
import shutil
import fnmatch

wrk_dir = r"/data/keeling/a/sf20/b/WRF4_4/WRF/test/em_les"
output_dir = r"/data/nriemer/d/sf20/les_output"
now = datetime.now()
datestamp = now.strftime('%Y-%m-%d')
timestamp = datetime.now().strftime('%H%M%S')
output_path = os.path.join(output_dir, datestamp, timestamp)
if not os.path.isdir(output_path):
    os.makedirs(output_path)
    print(f'{output_path}')

error_files = fnmatch.filter(os.listdir('.'), "rsl.error.*")
out_files = fnmatch.filter(os.listdir('.'), "rsl.out.*")
slurm_files = fnmatch.filter(os.listdir('.'), "slurm-*.out*")
wrfinput_files = fnmatch.filter(os.listdir('.'), "wrfinput_*")
wrfoutput_files = fnmatch.filter(os.listdir('.'), "wrfout_*")
wrfrst_files = fnmatch.filter(os.listdir('.'), "wrfrst_*")
namelist_output = fnmatch.filter(os.listdir('.'), "namelist.output")
species_config_files = fnmatch.filter(os.listdir('.'), "species_*data.json")

move_files = (error_files + out_files + slurm_files + wrfinput_files 
              + wrfoutput_files + wrfrst_files + namelist_output 
              + species_config_files)

if len(move_files) == 0:
    print('No files to move, exiting')
    sys.exit()

print('Moving simulation files')
for file in move_files:
    shutil.move(f"{wrk_dir}/{file}", f"{output_path}/{file}")

# TODO: could also move wrfchemi files