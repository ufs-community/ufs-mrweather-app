.. _inputs_and_outputs:

******************
Inputs and outputs
******************

This chapter provides an overview of the input and output files needed by the components
of the MR Weather App (:term:`chgres_cube`, the UFS :term:`Weather Model`, and :term:`UPP`).  Links to more
detailed documentation for each of the components are provided.

===========
Input files
===========

The MR Weather App requires numerous input files. :term:`CIME` can copy/link to input files,
run the end-to-end system and write output files to disk. Depending on the dates and format
(`GRIB2 <https://www.nco.ncep.noaa.gov/pmb/docs/grib2/>`_,
`NEMSIO <https://github.com/NOAA-EMC/NCEPLIBS-nemsio/wiki/Home-NEMSIO>`_, or 
`netCDF <https://www.unidata.ucar.edu/software/netcdf/>`_)
requested, input files can be automatically retrieved by CIME (:term:`GRIB2`) or must be staged by
the user (:term:`NEMSIO` or :term:`netCDF`).

-----------
chgres_cube
-----------

When a user runs the MR Weather App as described in the quickstart guide, input data for
chgres_cube is linked from a location on disk to your run directory via CIME. The data
is stored in a hierarchical way in the ``$DIN_LOC_IC`` directory
(see :numref:`Section %s <downloading_input_data>`). A list of the input files for chgres_cube
can be found `here <https://ufs-utils.readthedocs.io/en/ufs-v1.0.0/chgres_cube.html#program-inputs-and-outputs>`_.

-----------------
UFS Weather Model
-----------------

The input files for the MR Weather Model are located one directory up from the chgres_cube
input files in ``$RUNDIR`` (see :numref:`Section %s <run_the_case>`). An extensive description
of the input files for the MR Weather Model can be found in the `UFS Weather Model Users Guide
<https://ufs-weather-model.readthedocs.io/en/ufs-v1.0.0>`_.

.. note::
   Due to renaming/linking by CIME, the file names used in the MR Weather App
   differ from the names described in the UFS Weather Model User's Guide.


---------------
UPP input files
---------------

Documentation for the UPP input files can be found `here <https://upp.readthedocs.io/en/ufs-v1.1.0/InputsOutputs.html>`_.

============
Output files
============

The location of the output files written to disk is determined by CIME
(see :numref:`Section %s <run_the_case>`).

-----------
chgres_cube
-----------

The files output by chgres_cube reside in the ``$DIN_LOC_IC`` directory, and are linked by CIME to
files that include the grid name and date in the same directory.  For example:

.. code-block:: console

   sfc_data.tile[1-6].nc -> C96.2019-08-28_00.sfc_data.tile[1-6].nc
   gfs_ctrl.nc -> C96.2019-08-28_00.gfs_ctrl.nc
   gfs_data.tile1.nc -> C96.2019-08-28_00.gfs_data.tile1.nc

These output files are used as input for the UFS Weather Model.

.. note::
   The same input directory could have multiple pre-processed input files for different dates and
   once the run date is changed, CIME is able to link the correct files with the names that model expects.

-----------------
UFS Weather Model
-----------------

The output files for the UFS Weather Model are described in the `Users Guide
<https://ufs-weather-model.readthedocs.io/en/ufs-v1.1.0/InputsOutputs.html>`_.

.. _upp_output_files:

---------------
UPP output files
---------------

Documentation for the UPP output files can be found `here <https://upp.readthedocs.io/en/ufs-v1.1.0/InputsOutputs.html>`_.

If you wish to modify the fields or levels that are output from the UPP, you will need to make modifications to files ``postcntrl_gfs_f00.xml`` (used to post-process model data at the 0-h forecast lead time) and/or ``postcntrl_gfs.xml`` (used to post-process model data at all other forecast lead times), which reside in the UPP repository distributed with the MR Weather App. Specifically, if the code was cloned in the directory ``my_ufs_sandbox``, the files will be located in ``my_ufs_sandbox/src/post/parm``. Please note that this process requires advanced knowledge of which fields can be output for the UFS Weather Model.

Use the directions in the `UPP Users Guide <https://upp.readthedocs.io/en/ufs-v1.1.0/InputsOutputs.html#control-file>`_ for details on how to make modifications to these xml files and for remaking the flat text files that the UPP reads, which are ``postxconfig-NT-GFS.txt`` and ``postxconfig-NT-GFS-F00.txt``. It is important that you do not rename these flat files or the CIME workflow will not use them.

Once you have created new flat text files reflecting your changes, you will need to copy or link these static files to the ``/SourceMods/src.ufsatm`` directory within the CIME case directory. When running your case, CIME will first look for the ``postxconfig-NT-GFS.txt`` or ``postxconfig-NT-GFS-F00.txt`` in this directory, depending on forecast hour. If they are not present, the workflow will use the default files in a pre-configured location.

You may then setup/build/run your case as usual and the UPP will use the new flat ``*.txt`` files.

.. _downloading_input_data:

==================================
Downloading and staging input data
==================================

A set of input files, including static (fix) data and raw initial conditions, are needed to run the MR
Weather App. There are two variables that describe the location of the static and initial condition files:
``$DIN_LOC_ROOT`` is the directory where the static files are located and ``$DIN_LOC_IC`` is the
directory where the initial conditions are located. By default, ``$DIN_LOC_ROOT`` is set to
$UFS_INPUT/ufs_inputdata and ``$DIN_LOC_IC`` is set to ``$DIN_LOC_ROOT/icfiles``.
In this directory, the initial conditions are located in subdirectories named ``YYYYMM/YYYYMMDD`` (YYYY: year, MM: month, DD: day).

Variable ``$DIN_LOC_ROOT`` is already set in preconfigured platforms and points
to a centralized location where the fix files are staged.
Similarly, variable ``$DIN_LOC_IC`` is by default set to ``$DIN_LOC_ROOT/icfiles`` and
points to the directory with initial conditions for the Hurricane Dorian
initialization in 08-29-2019. In all other platforms, users can customize the
location of the fix files by setting `$UFS_INPUT` to a writable directory and
creating a subdirectory $UFS_INPUT/ufs_inputdata.

A customized location for ``$DIN_LOC_IC`` is necessary when users need to stage new
initial condition files and do not have write permission to ``$DIN_LOC_ROOT``.
Users can customize ``$DIN_LOC_IC`` after creating the case using the commands below.

.. code-block:: console

   cd $CASEROOT
   ./xmlchange DIN_LOC_IC=/path/to/directory

---------------
Static files
---------------

The user does not need to stage the fix files manually because CIME retrieves
the fix files from ``$DIN_LOC_ROOT`` (if available) or from a
`FTP data repository <https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`_. When CIME retrieves
the files from the ftp site, it places them in ``$DIN_LOC_ROOT``.

------------------------------------
Initial condition formats and source
------------------------------------

The MR Weather App currently only supports the use of Global Forecast System
(GFS) data as raw initial conditions (that is, MRF, AVN, ERA5 etc. are not supported).
The GFS data can be provided in three formats: :term:`NEMSIO`, :term:`netCDF`, or :term:`GRIB2`. Files in NEMSIO and GRIB2 format can be obtained
from the `NCEI website <https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs>`_.

- **NEMSIO**

  These files cover the entire globe down to a horizontal resolution of 13 km and
  can be found at `<https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/>`_.  
  
- **NetCDF**

  These files cover the entire globe down to a horizontal resolution of 13 km and
  can be found at the FTP data repository `<https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`_.  
     
- **GRIB2**

  These files cover the entire globe and resolutions of 0.5 and 1.0 degree are supported. There are both current and historic sources of GRIB2 `data available <https://docs.google.com/document/d/1rmQUC-Jn995IphtWx221EcGYBDG_eFA8LXP0LXv-wPQ/edit#>`_, here are two examples:

  - 0.5 deg files are available at `<https://www.ncei.noaa.gov/thredds/catalog/model-gfs-g4-anl-files-old/catalog.html>`_
  - 1.0 deg files can be requested from `<https://www.ncei.noaa.gov/thredds/catalog/model-gfs-g3-anl-files-old/catalog.html>`_

------------------------------------
Initial condition naming convention
------------------------------------

The default naming convention for the initial condition files is described below. The user must stage the files on disk following this convention so they can be recognized by the MR Weather App workflow.

- **NEMSIO**

  - Two-dimensional surface variables ``sfc.input.ic.nemsio``
  - Three-dimensional atmosphere state ``atm.input.ic.nemsio`` 

- **NetCDF**

  - Two-dimensional surface variables ``sfc.input.ic.nc``
  - Three-dimensional atmosphere state ``atm.input.ic.nc`` 
 
- **GRIB2**

  - Surface variables and atmosphere state ``atm.input.ic.grb2``

--------------------------
Default initial conditions
--------------------------

All supported CompSets use the Hurricane Dorian initialization of 08-29-2019.
In preconfigured platforms, the 08-29-2019 initial conditions are pre-staged in
``$DIN_LOC_IC``. Those are GRIB2 files with 0.5 deg resolution.

The default input data for the Hurricane Dorian initialization of 08-29-2019 is also available
on the `FTP data repository <https://ftp.emc.ncep.noaa.gov/EIB/UFS/inputdata/201908/20190829/>`_.

-----------------------------------
Running the App for different dates
-----------------------------------

If users want to
run the MR Weather App for dates other than 08-29-2019, they need to make a change in the case to
specify the desired data.  This is done by setting the ``RUN_STARTDATE`` and
``START_TOD`` CIME options using ``./xmlchange``.

CIME will look for the following directory containing initial conditions: ``$DIN_LOC_IC/YYMMMM/YYYYMMDD``.
Starting with the v1.1.0 release, the MR Weather App workflow no longer auot-downloads datasets. The data must be present in the centralized location (for preconfigured platforms) or downloaded manually.

---------------------------------------------------------
About the automatic stating of initial conditions by CIME
---------------------------------------------------------

CIME can be used to automatically download GRIB2 initial conditions in 0.5 deg format for the dates
available in the NOMADS server at `<https://nomads.ncdc.noaa.gov/data/gfs4/>`_.
NOMADS has GFS 0.5 deg GRIB2 datasets for the last twelve months. The data will be
retrieved from the server when case.submit command is issued.
Therefore, if users want to start the model from the 0.5 deg GRIB2 data available through
NOMADS, the users do not need to stage the data manually.

As part of the process of generating the MR Weather App executable,
CIME calls the utility **check_input_data** located in each case directory
to attempt to locate all required input data for the
case based upon file lists generated by components. If the required
static data is not found on local disk in ``$DIN_LOC_ROOT`` and raw initial conditions are not found in ``$DIN_LOC_IC``,
then CIME will attempt to download the data.

----------------------------------------------
Staging initial conditions manually using CIME
----------------------------------------------

GRIB2 data available in the NOMADS server can be automatically downloaded by CIME
when running the case. Conversely, the user can download the data in advance by
invoking script **check_input_data** with the ``--download`` argument.

------------------------------------------------
Staging initial conditions manually without CIME
------------------------------------------------


If users want to run the MR Weather App with initial conditions other than
what is currently available in preconfigured platforms, they need to stage the data manually.
The data should be placed in ``$DIN_LOC_IC``.

.. note::

     The following example script, ``get.sh`` can be used as a
     reference to download the NEMSIO file from the NOMADS server for
     a sample date, which in this case is 24-12-2018. **Note that NEMSIO
     files in NOMADS are only available for the last 10-days.**

     .. code-block:: console

         #!/bin/bash

         # Command line arguments
         if [ -z "$1" -o -z "$2" ]; then
            echo "Usage: $0 yyyymmdd hh"
            exit
         fi
         yyyymmdd=$1 #i.e. "20191224"
         hh=$2 #i.e. "12"

         # Get the data (do not need to edit anything after this point!)
         yyyymm=$((yyyymmdd/100))
         din_loc_ic=`./xmlquery DIN_LOC_IC --value`
         mkdir -p $din_loc_ic/$yyyymm/$yyyymmdd
         echo "Download files to $din_loc_ic/$yyyymm/$yyyymmdd ..."
         cd $din_loc_ic/$yyyymm/$yyyymmdd
         wget -c https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.$yyyymmdd/$hh/gfs.t${hh}z.atmanl.nemsio
         wget -c https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.$yyyymmdd/$hh/gfs.t${hh}z.sfcanl.nemsio
         cd -

     Script ``get.sh`` should be placed in **$CASEROOT** and used as follows:

     .. code-block:: console

         chmod 755 get.sh
         ./get.sh 20191224 12

     After downloading the nemsio files, the downloaded files need to be linked to the names expected by the App:

     .. code-block:: console

         ln -s gfs.t${hh}z.atmanl.nemsio atm.input.ic.nemsio
         ln -s gfs.t${hh}z.sfcanl.nemsio sfc.input.ic.nemsio

     For downloading files in GRIB2 format with 0.5 degree grid spacing, the same code ``get.sh`` can be used except the wget command should be replaced with the following line: 

     .. code-block:: console

         wget -c https://www.ncei.noaa.gov/thredds/catalog/model-gfs-g4-anl-files/$yyyymmdd/gfs_4_${yyyymmdd}_${hh}00_000.grb2

     For downloading files in GRIB2 format with 1.0 degree grid spacing, the same code ``get.sh`` can be used except the wget command should be replaced with the following line: 


     .. code-block:: console

         wget -c https://www.ncei.noaa.gov/thredds/catalog/model-gfs-g3-anl-files/$yyyymmdd/gfs_3_${yyyymmdd}_${hh}00_000.grb2

     After downloading the file, the user must link the new file to the name expected by the App. For example, 

     .. code-block:: console

         ln -s gfs_3_20190829_0000_000.grb2 atm.input.ic.grb2

     For downloading files in netCDF format, the wget commands in ``get.sh`` need to be changed to:

     .. code-block:: console

         wget -c https://ftp.emc.ncep.noaa.gov/EIB/UFS/inputdata/$yyyymm/gfs.$yyyymmdd/$hh/gfs.t${hh}z.atmf000.nc
         wget -c https://ftp.emc.ncep.noaa.gov/EIB/UFS/inputdata/$yyyymm/gfs.$yyyymmdd/$hh/gfs.t${hh}z.sfcf000.nc

     Currently, only two sample netCDF files are available for testing at the FTP data repository. Similarly, the downloaded files need to be linked to the names expected by the App. For example,

     .. code-block:: console

         ln -s gfs.t${hh}z.atmf000.nc atm.input.ic.nc
         ln -s gfs.t${hh}z.sfcf000.nc sfc.input.ic.nc

-------------------
Order of operations
-------------------

If you want to download the input data manually, you should do it before you build the MR Weather App.

-----------------------------------------------
Coexistence of multiple files for the same date
-----------------------------------------------

Directory `$DIN_LOC_IC/YYMMMM/YYYYMMDD` can have GRIB2, NEMSIO, and netCDF files for
a given initialization hour and can have files for multiple initialization hours
(00, 06, 12, and 18 UTC).

If a directory has files in more than one format for the same initialization date and time,
CIME will use the GRIB2 files. If the user wants to change this behavior so CIME uses the
NEMSIO or netCDF files, the user should edit file ``user_nl_ufsatm``
and add

.. code-block:: console

    input_type = "gaussian_nemsio" for NEMSIO
    input_type = "gaussian_netcdf" for netCDF

---------------------------------------------------------------
Best practices for conserving disk space and keeping files safe
---------------------------------------------------------------

Initial condition files are large and can occupy a significant amount of disk space.
If various users will employ a common file system to conduct runs, it is
recommended that these users share the same ``$DIN_LOC_ROOT``. That way, if
initial conditions are already on disk for a given date, they do not needed to be replicated.

The files in the subdirectories of ``$DIN_LOC_ROOT`` should be write-protected. This prevents these files
from being accidentally modified or deleted. The directories in ``$DIN_LOC_ROOT`` should generally
be group writable, so the directory can be shared among multiple users.
