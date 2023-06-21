import os
from datetime import datetime
import shutil
import fnmatch

wrk_dir = r"/data/nriemer/d/sf20/les_output/output" 
dest_dir = r"/data/nriemer/d/sf20/les_output"

for dir_name in os.listdir(wrk_dir):
    print(dir_name)
    shutil.move(f"{wrk_dir}/{dir_name}", f"{dest_dir}/{dir_name}")
