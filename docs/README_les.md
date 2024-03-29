## The ideal em_les test case

This test case produces a large-eddy simulation (LES) of a free
convective boundary layer (CBL).  The environmental wind (or
the initial wind profile) is set to zero in this default case.  
The turbulence of the free CBL is driven/maintained by the surface 
heat flux, which is specified in the namelist as tke_heat_flux=0.24 
(in MKS units).

A random perturbation is imposed initially on the mean temperature 
field at the lowest four grid levels to kick off the
turbulent motion. Double periodic boundary condition
is used in x and y.

The default version uses a grid resolution of
dx=dy=100m and dz=50m, which is considered to be rather coarse 
for an LES of the CBL.  A typical grid mesh for an LES
of the CBL is dx=dy=50m and dz=20m.  An LES flow field is more
accurate when the grid resolution is finer because it resolves
more turbulent scales.  

This LES version uses the Deardorff's TKE scheme to compute the SGS
eddy viscosity and eddy diffusivity for turbulent mixing, that is
diff_opt=2 and km_opt = 2 in the namelist.  The Coriolis parameter
is set to f = 10^-4/s.

It takes at least 30 minutes of simulation time to spin up the
turbulent flow field; only after the spin-up, the turbulence inside
the CBL is considered well established.  A sign of well-established
turbulence is that the total (i.e., the resolved-scale plus the
subgrid-scale) heat flux profile should decrease linearly with height
within the CBL.

To simulate a CBL with a mean wind, change the initial wind
profile in the input sounding.   
When pert_coriolis= true is set in the namelist, there is no need to 
include the geostrophic wind terms in the right-hand sides of
the u and v equations for LESs with non-zero geostrophic wind. 

Note, parameterization constants, c_s and c_k in this namelist are
different from the defaults and are the ones recommended to use with LES.

-----

## Shallow convection case (added in V3.7)

- Copy namelist.input_shalconv to namelist.input
- Copy input_sounding_shalconv to input_sounding
- Re-run ideal.exe
  
As LES case but larger domain (100x100), top still at 2 km.
Differences are sounding 10 K cooler, geostrophic u-wind 10 m/s, isfflx=1 using
input_sounding's surface theta = 295 K as SST, water surface, monotonic
moist and scalar advection, mp_physics =6, no other physics except sf_sfclay_physics=1.
This produces a shallow cloud layer capped by a strong inversion that
grows in response to warmer SST.
