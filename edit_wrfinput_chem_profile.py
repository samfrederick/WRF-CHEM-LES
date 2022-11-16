"""
"""
import os
import numpy as np
from scipy.stats import multivariate_normal
from netCDF4 import Dataset

def gauss3d_o3_profile():
    x, y, z = np.mgrid[0:1:99j, 0:1:99j, 0:1:199j]
    # Need an (N, 2) array of (x, y) pairs.
    xyz = np.column_stack([x.flat, y.flat, z.flat])

    mu = np.array([.5, .5, 0])

    sigma = np.array([.25, .25, .15])
    covariance = np.diag(sigma**2)

    val = multivariate_normal.pdf(xyz, mean=mu, cov=covariance)

    # Reshape back to a (30, 30) grid.
    val = val.reshape(x.shape)

    # Normalize max to 100 (ppmv) and transpose so orientation is correct (z up)
    val = val.T*(100/val.max())

    # Assign minimum value via ambient concentration populated in array by WRF-Chem
    # prior to modification
    val[val<0.03] = 0.03

    new_o3_vals = np.ma.array(np.array([val]), mask=False, dtype='float32')

    return new_o3_vals


def create_modified_netcdf():
    # Code via 
    # https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    # User Rich Signell
    
    new_o3_vals = gauss3d_o3_profile()

    toexclude = ['o3']

    src = Dataset("wrfinput_d01")
    dst = Dataset("wrfinput_d01_new", "w")

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
            dst[name][:] = new_o3_vals
            # copy variable attributes all at once via dictionary
            dst[name].setncatts(src[name].__dict__)
            
    src.close()
    dst.close()
    return

def update_netcdf_names():
    os.rename("wrfinput_d01", "wrfinput_d01_unmodifed")
    os.rename("wrfinput_d01_new", "wrfinput_d01")
    return

print('\nModifing Ozone input data\n')
create_modified_netcdf()
update_netcdf_names()