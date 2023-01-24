"""
"""
import os, sys
import numpy as np
from scipy.stats import multivariate_normal
from netCDF4 import Dataset

try:
    profile_type = sys.argv[1]
except IndexError:
    "Emission profile function not specified!"
    exit()

# MESH VARIABLES
xgrid = 100
ygrid = 100
zgrid = 200

def create_mesh_grid():
    xmax = xgrid - 1
    ymax = ygrid - 1
    zmax = zgrid - 1
    x, y, z = np.mgrid[0:1:(xmax*1j), 0:1:(ymax*1j), 0:1:(zmax*1j)]

    return x, y, z

def gauss3d_o3_profile():
    x, y, z = create_mesh_grid()
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

    print(val.shape)

    new_o3_vals = np.ma.array(np.array([val]), mask=False, dtype='float32')

    return new_o3_vals

def checkerboard_profile():
    xrange, yrange = xgrid-1, ygrid-1
    epsilon = 0.001
    Ax, Ay = 1, 1
    fx, fy = 1, 1
    k = fx*2*np.pi/xrange #wavenumber 2pi / L
    m = fy*2*np.pi/yrange
    x=np.arange(xrange)
    y=np.arange(yrange)
    X,Y=np.meshgrid(x,y)
    phi=Ax*np.sin(k*X+epsilon)*Ay*np.sin(m*Y+epsilon)

    phi_star = phi.copy()

    phi_star[phi_star > 0] = 1
    phi_star[phi_star <= 0] = 0

    mesh = np.zeros((xgrid-1, ygrid-1, zgrid-1))
    mesh[:, :, 0] = phi_star

    # transpose so z, y, x
    mesh = mesh.T

    mesh = np.ma.array(np.array([mesh]), mask=False, dtype='float32')

    return mesh

def create_modified_netcdf():
    # Code via 
    # https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    # User Rich Signell
    
    new_o3_vals = profile_func()

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

if __name__ == '__main__':
    profile_func = globals()[profile_type]
    print('\nModifing emissions input data\n')
    print(f'Using {profile_type}() method\n')
    create_modified_netcdf()
    update_netcdf_names()