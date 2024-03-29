`anthro_emis` Readme - Table of Contents
-----------------

- [Namelist variable notes](#namelist-variable-notes)
  - [wrf\_dir (optional)](#wrf_dir-optional)
  - [anthro\_dir (optional)](#anthro_dir-optional)
  - [src\_file\_prefix, src\_file\_suffix (optional)](#src_file_prefix-src_file_suffix-optional)
  - [src\_names (mandatory)](#src_names-mandatory)
  - [sub\_categories (optional)](#sub_categories-optional)
  - [cat\_var\_prefix, cat\_var\_suffix (optional)](#cat_var_prefix-cat_var_suffix-optional)
  - [emis\_map (mandatory)](#emis_map-mandatory)
    - [Example #1](#example-1)
    - [Example #2](#example-2)
  - [serial\_output (optional)](#serial_output-optional)
  - [start\_output\_time, stop\_output\_time, output\_interval (optional)](#start_output_time-stop_output_time-output_interval-optional)
  - [output\_interval](#output_interval)
  - [data\_yrs\_offset (optional)](#data_yrs_offset-optional)
  - [domains](#domains)
- [Namelist Input File Examples](#namelist-input-file-examples)
  - [Example 1](#example-1-1)
  - [Example 2](#example-2-1)
  - [Example 3](#example-3)
- [Running anthro\_emis](#running-anthro_emis)
- [Contacts](#contacts)

----
If you require assistance with compiler and/or netcdf issues please use the
discussion forum at https://www2.acom.ucar.edu/wrf-chem/discussion-forum to post
messages. You will will need to register before you use a specific forum.

The `anthro_emis` utility, a single cpu executable, creates WRF gridded
anthropogenic emissions files from lat-lon gridded input anthropogenic
emission files.  The resulting WRF files can be two types; (a) diurnal and 
(b) serial.  There are two datasets with file names of the form 
`wrfchemi_00z_d<nn>` and `wrfchemi_12z_d<nn>` for the diurnal case
and `wrfchemi_d<nn>_<date>` for the serial case.

Throughout this note the following definitions pertain:

* `<nn>`   is a two digit integer representing a WRF domain
* `<date>` is a WRF date of the form `yyyy-mm-dd_hh:mm:ss`

----

Input anthropogenic datasets
----------------------------

The input lat-lon anthropogenic emission files must be netcdf
conforming datasets and have the following structure:

1. Each input dataset is for one input species

2. Lon and lat one dimensional variables containg the longitudes
    and latitudes in degrees about which each input grid cell is
    centered.  The lon and lat variables must be monotonically
    increasing.

3. One of the following:
    -  Date and datesec variables containing the date and seconds
	 in day. The date is an integer encoding the date `yyyymmdd`.
    - A time variable representing the time since a given date.
	 The base date must be contained in the time variable units
	 attribute and be of the form `yyyy-mm-dd`.

4. One or more variables containing the actual anthropogenic
   emissions, designated as sub categories, which must be dimensioned
   as `(lon,lat,time)`.

Additionally the input anthropogenic dataset may have the molecular
weight of the input species in g/mole as either:

  * A variable with the name `molecular_weight`
  * A global attribute with the name `molecular_weight`
  * A sub category variable attribute with the name `molecular_weight`

If the input dataset does not specify the species molecular weight
then the user may specify the input species molecular weight in the
`src_names` namelist variable (see below).  

If the molecular weight is specified via the `src_names` namelist variable
then any molecular weight information in the input dataset is ignored.

Input WRF datasets
-----------------

There must be a WRF initial condition file per WRF domain.  Standard WRF
initial condition files are denoted:

```console
wrfinput_d<nn>
```

Building anthro_emis
-----------------
	
In the anthro_emis source code directory, `src`, issue the command:
	
```console
csh make_anthro
```
	
That's it.  If all goes well you will have the executable file `anthro_emis`
in the `anthro_emis` source directory.  The `make_anthro` script is presently
setup to compile on either Linux systems using the Portland Group Fortan90
compiler, pgf90, or on AIX systems using the xlf90 compiler.  If you need
to use another compiler such as the Intel Fortran90 compiler, ifort, you 
can set the environment variable

```console	
FC
```
	
before invoking `make_anthro`.  As an example you would issue
the command:

```console	
export FC=ifort 
```
	
in the sh, bash, or ksh Linux shells or

```console	
setenv FC ifort
```
	
in the csh or tcsh shells.

The `anthro_emis` utility requires the netcdf library and `make_anthro`
will attempt to locate the `libnetcdf.a` library.  However, this is
not a foolproof process and thus you may need to set the environment variable

```console
NETCDF_DIR
```

to the directory containing the file `lib/libnetcdf.a`.  As an example
in the ksh shell, if you issued the command:

```console
export NETCDF_DIR=/usr/local/netcdf-4.1.2
```
	
then `make_anthro` would look for the file `libnetcdf.a` in the
directory `/usr/local/netcdf-4.1.2/lib` (`make_anthro` automatically
appends the `/lib` string to the `NETCDF_DIR` string.

`anthro_emis` reads a namelist input file (`anthro_emis.inp`) that specifies 
all aspects of the mapping of source lat-lon datasets to WRF emission 
datasets and checks key namelist control variables for validity.  Below 
is a complete listing of all namelist control variables grouped by 
functionality. (*Examples for anthro_emis.inp are given below the 
following listing*).

Directory
-----------------

| Variable name | Variable type             | default value             |
|---------------|---------------------------|---------------------------|
| anthro_dir    | character(len=132),scalar | present working directory |
| wrf_dir       | character(len=132),scalar | present working directory |

Filename
-----------------

| Variable name | Variable type             | default value             |
|---------------|---------------------------|---------------------------| 
| src_file_prefix       |    character(len=132),scalar             |      blank string |
| src_file_suffix        |   character(len=132),scalar              |     blank string |

Timing
-----------------

| Variable name     |        Variable type                   |     default value| Units/Notes |
| ------------ |------------  | ------------| -------------- |
| start_output_time      |    character(len=19),scalar       |                 (None)           |          <date> | 
| stop_output_time        |   character(len=19),scalar       |                 (None)           |          <date> | 
| output_interval        |    integer,scalar                 |                 3600            |           seconds | 
| serial_output          |    logical,scalar                |                  .false.     |    | 
| data_yrs_offset       |     integer,scalar                |                  0             |             years| 

Mapping
-----------------
	
| Variable name | Variable type             | default value             |
|---------------|---------------------------|---------------------------| 
| emis_map     |             character(len=132),array(500)        |          (None)                    |

Input File Variable Names
-----------------
	
| Variable name | Variable type             | default value             |
|---------------|---------------------------|---------------------------|
| src_names            |     character(len=32),array(50)           |      See note below |
| sub_categories        |    character(len=32),array(50)            |     See note below |
| cat_var_prefix         |   character(len=132),scalar               |    blank_string |
| cat_var_suffix          |  character(len=132),scalar                |   blank string |

WRF Parameters
-----------------
	
| Variable name | Variable type             | default value             |
|---------------|---------------------------|---------------------------|
| domains                |    integer,scalar         |                         1 |
| emissions_zdim_stag     |  integer,scalar             |                      10 |


**The following variables must be set in the input namelist file or anthro_emis will error halt.**
	
```console
src_names
emis_map
```
	
Although none of the remaining namelist variables need be set it is most likely that some of the
remaining variables will be set.

**Formatting Note:**
> **From this point forward the `{}` pair is used to mark optional input.**   
> The actual input comprises the characters enclosed by the `{}` pair. The `{}` 
> pair is *NOT* part of the namelist input. **Similarly the `<>` pair denotes a 
> generic input** and the `<>` pair is NOT part of the namelist input.                                       

Namelist variable notes
=======================

wrf_dir (optional)
------------------

Specifies the directory where anthro_emis expects to find the WRF input
files wrfinput_d<nn>.  Note that wrf_directory must NOT end with a "/"
as in:

```console
/myhome/WRF_data/
```

the correct setting is:

```console
wrf_dir = '/myhome/WRF_data'
```
	
Defaults to the present working directory.

anthro_dir (optional)
----------

Specifies the directory where anthro_emis expects to find the lat-lon
anthropogenic emission datasets.  Again note that anthro_dir must NOT 
end with a "/" as in:

```console
/myhome/ANTHRO_data/
```
	
the correct setting is:

```console
anthro_dir = '/myhome/ANTHRO_data'
```
	
Defaults to the present working directory.

src_file_prefix, src_file_suffix (optional)
------------------------------

Used to form the fully anotated source emission dataset filename.  If we
have set the following namelist settings:

```console
src_names       = 'CH3'
src_file_prefix = 'POET_anthro_emissions_'
src_file_prefix = '2003.nc'
```

then the anthro_emis utility will look for the the input emission dataset

```console
POET_anthro_emissions_CH3_2003.nc
```
	
and will error halt if it does not exist.


src_names (mandatory)
---------

Specifies a list of up to 50 source anthropogenic species.  Each name must be
must be <= 32 characters and have the form:

```console
<name>{(mol_wght)}
```
	
Where

- mol_wght is the molecular weight (g/mole) for the source species

These names are used to:

*  map source anthropogenic emissions to WRF species anthropogenic emissions
   via the emis_map namelist variable
*  construct the full file specification for the source anthropogenic emission files

Each source file has a full file specification of the form:

```console
anthro_dir/filename
```
	
where `filename = src_file_prefix // src_name // src_file_suffix`

For example if:
	
```console
anthro_dir = '/myhome/ANTHRO_data'
src_name   = 'CO(28)'
src_file_prefix = ' '
src_file_suffix = '.nc'
```
	
then the full file specification would be:
	
```console
/myhome/ANTHRO_data/CO.nc
```
	
Note that CO is assigned a molecular weight of 28 g/mole.  Additionally
note that only the <name> portion of a src_name entry is used for file
name construcution and species mapping.

sub_categories (optional)
--------------

Specifies a list of up to 50 source anthropogenic species.  Each name must be
<= 32 characters. The `sub_categories` list members are used to construct the
full name of the source emission variables in the input emission datasets.

Each source emission variable name is of the form:

```console
cat_var_prefix // sub_category // cat_var_suffix
```

For example if:

```console
sub_category   = 'industrial'
cat_var_suffix = '_emissions'
```

then the sub category emission variable name would be:

```console
industrial_emissions
```

since cat_var_prefix and cat_var_suffix default to the blank
string the default sub category emission variable name would
have simply been:

```console
industrial
```

The sub_categories list defaults to the following 9 names:

`'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'tra', 'wst', 'ship'`

Note that by default cat_var_prefix and cat_var_suffix are blank strings.
Thus by default all the sub category variables in all input datasets must
be one of the following names:

`'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'tra', 'wst', 'ship'`

The sub categories actually used in all the source emission datasets
must be specified in the sub_categories list.  The sub category variables
in each input dataset may vary from input dataset to input dataset.

As an example suppose we had the following namelist settings:

```console
src_file_suffix  = '.nc'
src_names        = 'CH4', 'H2CO'
sub_categories   = 'Transport', 'Burning', 'Urban'
emis_map         = 'CH4 -> CH4', 'H2CO -> H2CO(Burning)'
```

In this case anthro_emis will look for:

- the variables Transport, Burning, and Urban in the file `CO.nc`

- the variable  Burning in the file `H2CO.nc`

Note that the file `H2CO.nc` does not have to have Transport or Urban
variables in this case.


cat_var_prefix, cat_var_suffix (optional)
------------------------------

Used to form the fully anotated source emission variable name.  If we
have set the following namelist definitions:

```console
cat_subcategories = 'industrial'
cat_var_prefix = 'automobile_'
```

then the `anthro_emis` utility will look for the the input emission variable

`automobile_industrial`

and will error halt if it does not exist.

emis_map (mandatory)
--------

Specifies the mapping between WRF species anthropogenic emissions and source lat-lon
emission datasets.  The `emis_map` namelist variable is a character array of size 500
with each array element 132 characters long.  

Each entry in the is of the form:


`<WRF_emis> -> spc_mult * <emis_name>{ + spc_mult * <emis_name> + ... }`

Where

`<WRF_emis>` is of the form:

`<name>{(a)}`

wherein `<name>` will be used to construct the actual name of the WRF species
anthropogenic emission in the output dataset.  The actual name in the output
dataset is of the form `E_<name>`.  

If present the "(a)" string denotes the WRF output species to be an aerosol.
If no "(a)" string is present the WRF output species is understood to be a gas.
WRF gas phase and aerosol species have different emission units:

```console
gas     == mole/km^2/hr   (moles per kilometer squared per hour)
aerosol == ug/m^2/s       (micro gram per meter squared per second)
```

`spc_mult` is any legal, positive fortran real or integer number.  `spc_mult` defaults
to `1.` and may vary from source emission species to source emission species.

`<emis_name>` is of the form:

`<src_name{(cat_mult * <cat_name>){ + <cat_mult * <cat_name> + ... }})}`

where:

- `<src_name>` matches one of the entries in the src_names list
defined by src_name
- `cat_mult` has the same definition as `spc_mult`
- `<cat_name>` matches one of the entries in the sub_categories list

**The following are two examples of `emis_map` specification:**

### Example #1

```console
src_names       = 'CO'
src_file_suffix = '.nc'
cat_var_suffix  = '_emiss
emis_map = 'CO -> CO(ship)'
```

maps the source sub category emission variable `ship_emiss` in the source file `CO.nc`
to the WRF emission variable `E_CO`. Note this assumes the following defaults:

```console
src_file_prefix = ' '
cat_var_prefix  = ' '
```

are being used.  Additionally note:

- the output emission, `E_CO`, is assumed to be for a gas phase species
- the input species, `CO`, molecular weight is assumed to be contained
  in the input file `CO.nc`

### Example #2

```console
src_names       = 'ALK'
src_file_prefix = 'anthro_'
src_file_suffix = '_2012.nc'
sub_categories  = 'forest', 'airplane'
emis_map = 'PAR(a) -> ALK(.5*airplane+.25*forest)'
```

maps the source sub category emission variables forest and airplane with respective
weighting of .25 and .5 in the source file `anthro_ALK_2012.nc` to the WRF emission
variable `E_PAR`. Note this assumes the following defaults:

```console
cat_var_prefix  = ' '
cat_var_suffix  = ' '
```

are being used.  Additionally note:

- the output emission, `E_PAR`, is assumed to be for an aerosol species

serial_output (optional)
-------------

Specifies whether or not the output WRF dataset(s) are diurnal
or serial.  The default value is `.false`. which means the `anthro_emis`
will output two diurnal datasets per domain:

`wrfchemi_00z_d<nn> and wrfchemi_12z_d<nn>`

each dataset will have 12 hourly values.  Presently ALL 12 hourly
values are identical.

If on the other hand you have specified:

```console
serial_output = .true.
```

in the namelist file then `anthro_emis` will produce a series of
WRF emission datasets per domain:

```console
wrfchemi_d<nn>_<date>
```

each dataset containing a single time point.  The exact number of datasets
produced depends on the:

`start_output_time, stop_output_time, and output_interval`

namelist settings. (See examples directly below)

start_output_time, stop_output_time, output_interval (optional)
--------------------------------------

For the case `serial_output = .false.` the start_output_time variable is
optional and the stop_output_time and output_interval variables are ignored.

For the case `serial_output = .true.` all the namelist variables are
optional.

If the start_output_time variable is not specified in the input namelist file
then `start_output_time` is taken from the `wrfinput_d<nn>` file(s).

If the `stop_output_time` variable is not specified in the input namelist file
then `stop_output_time` is assigned the value `start_output_time` on a per domain basis.

If `start_output_time` and stop_output_time are assigned and `serial_output = .true.`
then `stop_output_time` must be >= `start_output_time`.  If this is not the case then
`anthro_emis` will error halt. 

As an example suppose the `wrfinput_d01` dataset has the WRF_time:

`2005-05-22_00:00:00  (zero hundred hours on May 22, 2005)`

then by default either diurnal or serial emission output dataset(s)
will start at:

`2005-05-22_00:00:00`

Furthermore, `anthro_emis` will try to perform time interpolation on any
input datasets for the time `2005-05-22_00:00:00`.  If the time `2005-05-22_00:00:00`
is outside the times in the input dataset then `anthro_emis` will error halt.

If we have `serial_output = .true.` then:

- `stop_output_time` will be set to `2005-05-22_00:00:00`
- a single output emissions dataset, `wrfchemi_d01_2005-05-22_00:00:00`, will
be produced

output_interval
---------------

For the case `serial_output = .true.`, `output_interval` defines the frequency at
which WRF output emission datasets are produced.  This namelist variable is
understood to be in seconds and defaults to value 3600 (one hour).

Thus for the following namelist assignments:

```
serial_output = .true.
start_output_time  = '2010-01-01_00:00:00'
stop_output_time   = '2010-01-02_00:00:00'
output_interval = 21600
```

anthro_emis will attempt to output five WRF emission datasets, starting
on `2010-01-01_00:00:00` and ending on `2010-01-02_00:00:00`, one every 6 hours
between the start and stop dates.  Bear in mind that `anthro_emis` will
attemp to do time interpolation on the input dataset(s) for the following times:

```
2010-01-01_00:00:00
2010-01-01_06:00:00
2010-01-01_12:00:00
2010-01-01_18:00:00
2010-01-02_00:00:00
```
	  
and produce the following output datasets:
	  
```
wrfchemi_d01_2010-01-01_00:00:00
wrfchemi_d01_2010-01-01_06:00:00
wrfchemi_d01_2010-01-01_12:00:00
wrfchemi_d01_2010-01-01_18:00:00
wrfchemi_d01_2010-01-02_00:00:00
```
	  
each dataset containing emissions at one time.

data_yrs_offset (optional)
---------------

If for any reason the WRF emission output times are outside the input
emissions datasets times then anthro_emis will error halt.  And there are cases
where the year of the input and the year of the output datasets do not match.

For these situations you can use the `data_yrs_offset` variable to "align" the
year of the output times with the span of the input times.  The `data_yrs_offset`
variable defaults to 0.

It is best to illustrate the use of `data_yrs_offset` with the following example:

```
serial_output = .true.
start_output_time  = '2013-01-01_00:00:00'
stop_output_time   = '2013-01-02_00:00:00'
output_interval = 21600
data_yrs_offset = -3
```

This is similar to the above example except the output year is 2013.  If you still
want to use data for the year 2010 the above `data_yrs_offset` setting will do the job.
Output at the first time point `2013-01-01_00:00:00` will attempt to interpolate the
input dataset at time `2010-01-01_00:00:00`; not `2013-01-01_00:00:00`.

domains
-------

Specifies the total number of WRF domains.  Defaults to `1.`  Remember, if you set:

```console
domains = 2
```

then `anthro_emis` will expect to find files:

`wrfinput_d01`, `wrfinput_d02` in the directory indicated by the `wrf_dir` variable.

-------------------------------------------------------------------------------------------------

Namelist Input File Examples
============================

Following are a few examples of complete namelist input files.  As such they do NOT
represent any particular WRF-Chem chemical option.  Rather they are only for purposes
of illustrating how to set variables in the `anthro_emis` namelist file.

Example 1
---------

```console
&CONTROL
anthro_dir = '/myhome/ANTHRO_data'
src_file_prefix = 'IPCC_emissions_'
src_file_suffix = '_anthropogenic_2000_0.1x0.1_v1_jan2012_gridscaling.nc'
src_names = 'CO'
cat_var_suffix = '_emiss'
emis_map  = 'CO -> CO(awb)'
/
```

Relevant defaults:

- `wrf_dir = present working directory`
- `domains = 1`
- `serial_output = .false.`
- `cat_var_prefix = ' '`
- `cat_subcategories = 'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'tra', 'wst', 'ship'`
- the time in the `wrfinput_d01` file is `2000-01-01_00:00:00`

Anthro_emis will attemp to:

  - read the `wrfinput_d01` file in the present working directory
- read the variable `awb_emiss` from the input source file:
  `/myhome/ANTHRO_data/IPCC_emissions_CO_anthropogenic_2000_0.1x0.1_v1_jan2012.nc`
- interpolate the input file to the time `2000-01-01_00:00:00`
- output files `wrfchemi_00z_d01`, `wrfchemi_12z_d01` with the gas phase
  emission variable `E_CO`

Key assumptions:

- the input source file times bracket the time `2000-01-01_00:00:00`

What if:

1. I want serial output for the time `2000-01-01_00:00:00`

    - add the following line to the namelist input file:

      `serial_output = .true.`

    - this will output the file:

      `wrfchemi_d01_2000-01-01_00:00:00`

2. I want the serial output file to be setup for the time `2012-01-01_00:00:00`

    - add the following lines to the namelist input file:

      ```console
      serial_output = .true.
      start_output_time  = 2012-01-01_00:00:00
      data_yrs_offset = -12
      ```

    - this will output the file:

      `wrfchemi_d01_2012-01-01_00:00:00`

      > NOTE: you are still using input data from the year 2000 but setting up a WRF emission file for the time `2012-01-01_00:00:00`

3. I want the output variable E_CO to use all the sub categories with equal
    weight of 1

    - change the following line in the namelist input file:

      `emis_map  = 'CO -> CO(awb)'`

      to

      `emis_map  = 'CO -> CO'`

Example 2
---------

```console
&CONTROL
anthro_dir = '/myhome/ANTHRO_data'
src_file_prefix = 'IPCC_emissions_'
src_file_suffix = '_anthro_2000.nc'
src_names = 'OC', 'CO', 'NO', 'NH3', 'SO2', 'CH2O'
emis_map = 'OC(a) -> OC',
    'CO->.23*CO(agr+ship)','NO->NO(ene+ind+slv)+1.5*NH3(awb+2.*wst)+SO2',
    'BIGALK -> .5 * CO(.2*awb+.3*dom+.4*ene+.6*slv+.7*tra+.8*wst+ship)',
    ' + 1.3*CH2O'
/
```

Rather than go through all the defaults, conditions, whatifs lets skip
right to the results:

`Anthro_emis` will attemp to:

- read and time interpolate the following input files and sub categories:

    ```console
    IPCC_emissions_OC_anthro_2000.nc
    'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'tra', 'wst', 'ship'
    IPCC_emissions_CO_anthro_2000.nc
    'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'wst', 'ship'
    IPCC_emissions_NO_anthro_2000.nc
    'ene', 'ind', 'slv'
    IPCC_emissions_NH3_anthro_2000.nc
    'awb', 'wst'
    IPCC_emissions_SO2_anthro_2000.nc
    'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'tra', 'wst', 'ship'
    IPCC_emissions_CH2O_anthro_2000.nc
    'agr', 'awb', 'dom', 'ene', 'ind', 'slv', 'tra', 'wst', 'ship'
    ```

    > NOTE: the CO sub categories are used to form both the CO and BIGALK output emissions except for the tra sub category.

    > NOTE: both the source species and sub categories have non-unity weight factors

- output files `wrfchemi_00z_d01`, `wrfchemi_12z_d01` with the emission variables
  `E_OC`, `E_CO`, and `E_BIGALK`

- `OC` output will have aerosol units, `CO` and `BIGALK` gas units

Example 3
---------

Suppose I want, as in Example #1 above, to map input emissions to
the WRF variable `CO` but I want to use two datasets whose emissions
will be combined to produce the final WRF CO anthropogenic emissions.

In this case the namelist file would be:

```
&CONTROL
anthro_dir = '/myhome/ANTHRO_data'
src_file_prefix = 'IPCC_emissions_'
src_file_suffix = '_anthropogenic_2000_0.1x0.1_v1_jan2012_gridscaling.nc'
src_names = 'CO', 'XCO'
cat_var_suffix = '_emiss'
emis_map  = 'CO -> CO(awb)+XCO(awb)'
/
```
	
The defaults are the same as in Example #1.  And the output files are the same
as in example #1.  However for this example `anthro_emis` will attempt to:

- read the `awb_emiss` variable in the file
  `/myhome/ANTHRO_data/IPCC_emissions_CO_anthropogenic_2000_0.1x0.1_v1_jan2012.nc`

- read the `awb_emiss` variable in the file
  `/myhome/ANTHRO_data/IPCC_emissions_XCO_anthropogenic_2000_0.1x0.1_v1_jan2012.nc`

- combine the two inputs with equal weight of `1.`, the defaults, to produce the
  `E_CO` output variable

Note that the `src_names` variable had to be modified to include a second source
which has been given the name `XCO`.

*******************************************************************************************
**For an input namelist file you can use with the MOZCART_KPP WRF chem option 
please see the mozcart.inp and README.mozcart.inp files**                     
*******************************************************************************************

Running anthro_emis
==================

To run anthro_emis issue the command:

```console
anthro_emis < anthro_emis.inp {> anthro_emis.out}
```

(Redirected input is required. Redirected output to anthro_emis.out is optional.
 The anthro_emis.inp and anthro_emis.out filenames are for illustration only; you
 may use any valid filename in place of anthro_emis.inp, anthro_emis.out)

Contacts
========

For questions or comments please send email to:

Stacy Walters (stacy@ucar.edu),  Gabriele Pfister (pfister@ucar.edu)
