.. _inputs_and_outputs:

******************
Inputs and outputs
******************

This chapter provides an overview of the input and output files needed by the components
of the UFS MR Weather App (:term:`chgres_cube`, the UFS :term:`Weather Model`, and :term:`UPP`).  Links to more
detailed documentation for each of the components are provided.

===========
Input files
===========

The :term:`UFS` MR Weather App requires numerous input files. :term:`CIME` can copy/link to input files,
run the end-to-end system and write output files to disk. Depending on the dates and format
(`GRIB2 <https://www.nco.ncep.noaa.gov/pmb/docs/grib2/>`_ and
`NEMSIO <https://github.com/NOAA-EMC/NCEPLIBS-nemsio/wiki/Home-NEMSIO>`_)
requested, input files can be automatically retrieved by CIME (GRIB2) or must be staged by
the user (:term:`NEMSIO`).

-----------
chgres_cube
-----------

When a user runs the UFS MR Weather App as described in the quickstart guide, input data for
chgres_cube is linked from a location on disk to your run directory via CIME. The data
is stored in a hierarchical way in the ``$DIN_LOC_IC`` directory
(see :numref:`Section %s <downloading_input_data>`). A list of the input files for chgres_cube
can be found `here <https://ufs-utils.readthedocs.io/en/ufs-v1.0.0/chgres_cube.html#program-inputs-and-outputs>`_.

-----------------
UFS Weather Model
-----------------

The input files for the UFS MR Weather Model are located one directory up from the chgres_cube
input files in ``$RUNDIR`` (see :numref:`Section %s <run_the_case>`). An extensive description
of the input files for the UFS MR Weather Model can be found in the `UFS Weather Model Users Guide
<https://ufs-weather-model.readthedocs.io/en/release-public-v1/InputsOutputs.html>`_.

.. note::
   Due to renaming/linking by CIME, the file names used in the UFS MR Weather App
   differ from the names described in the UFS Weather Model User's Guide.

---------------
UPP input files
---------------

Documentation for the input files for UPP are located `here <https://upp.readthedocs.io/en/ufs-v1.0.0/InputsOutputs.html>`_.

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
<https://ufs-weather-model.readthedocs.io/en/release-public-v1/InputsOutputs.html>`_.

---------------
UPP input files
---------------

Documentation for the Unified Post Processor (UPP) output files can be found
`here <https://upp.readthedocs.io/en/ufs-v1.0.0/InputsOutputs.html>`_.

.. _downloading_input_data:

==================================
Downloading and staging input data
==================================

A set of input files, including static (fix) data and raw initial conditions, are needed to run the UFS MR
Weather App. There are two variables that describe the location of the static and initial condition files:
``$DIN_LOC_ROOT`` is the directory where the static files are located and ``$DIN_LOC_IC`` is the
directory where the initial conditions are located. By default, ``$DIN_LOC_ROOT`` is set to
$UFS_INPUT/ufs_inputdata and ``$DIN_LOC_IC`` is set to ``$DIN_LOC_ROOT/icfiles``.
In this directory, the initial conditions are located in subdirectories named ``YYYYMM/YYYYMMDD`` (YYYY: year, MM: month, DD: day).

Variable ``$DIN_LOC_ROOT`` is already set in preconfigured platforms and points
to a centralized location where the fix files are staged.
Similarly, variable $DIN_LOC_IC is by default set to $DIN_LOC_ROOT/icfiles and
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
the fix files from from ``$DIN_LOC_ROOT`` (if available) or from a
`FTP data repository <https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`_. When CIME retrieves
the files from the ftp site, it places them in ``$DIN_LOC_ROOT``.

------------------------------------
Initial condition formats and source
------------------------------------

The UFS MR Weather App currently only supports the use of Global Forecast System
(GFS) data as raw initial conditions (that is, MRF, AVN, ERA5 etc. are not supported).
The GFS data can be provided in two formats: NEMSIO or GRIB2. Both types of files can be obtained
from the `NCEI website <https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs>`_.

- **NEMSIO**

  These files cover the entire globe down to a horizontal resolution of 13 km and
  can be found at `<https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/>`_.

- **GRIB2**

  These files cover the entire globe and resolutions of 0.5, or 1.0 degree are supported.

  - 0.5 deg files are available at `<https://nomads.ncdc.noaa.gov/data/gfs4/>`_
  - 1.0 deg files can be requested from `<https://www.ncdc.noaa.gov/has/HAS.FileAppRouter?datasetname=GFS3&subqueryby=STATION&applname=&outdest=FILE>`_

------------------------------------
Initial conditions naming convention
------------------------------------

The default naming convention for the initial conditions files is described below.

- **NEMSIO**

  - Two-dimensional surface variables ``gfs.tHHz.sfcanl.nemsio``
  - Three-dimensional atmosphere state ``gfs.tHHz.atmanl.nemsio``

- **GRIB2**

  - Surface variables and atmosphere state ``gfsanl_4_YYYYMMDD_HH00_000.grb2``


  If the user is initializing from 1.0-degree GRIB2 format data, which on
  NOMADS uses the gfs_3_YYYYMMDD_00HH_000.grb2 naming convention, the user
  needs to change variable ``grib2_file_input_grid`` in the chgres_cube namelist.
  This is done by editing file ``user_nl_ufsatm``, which resides in the ``$CASEROOT``
  directory as follows. The example below is for the Dorian case initialized on
  08-29-2019.

  .. code-block:: console

      !----------------------------------------------------------------------------------
      ! This file can be used to change namelist options for:
      ! - Chgres
      ! - UFS MR-Weather Model
      ! - NCEP Post
      !
      ! Users should add all user-specific namelist changes below in the form of
      !  namelist_var = new_namelist_value
      !
      ! To change the namelist variables that are defined as multiple times under
      ! different namelist groups
      !  namelist_var@namelist_group = new_namelist_value
      !
      ! Following is the list of namelist variables that need to be accessed by
      ! specifying the namelist groups:
      !
      ! alpha@nam_physics_nml
      ! alpha@test_case_nml
      ! avg_max_length@atmos_model_nml
      ! avg_max_length@gfs_physics_nml
      ! debug@atmos_model_nml
      ! debug@gfs_physics_nml
      ! icliq_sw@gfs_physics_nml
      ! icliq_sw@nam_physics_nml
      ! iospec_ieee32@fms_nml
      ! iospec_ieee32@fms_io_nml
      ! ntiles@fv_core_nml
      ! ntiles@nest_nml
      ! read_all_pe@fms_io_nml
      ! read_all_pe@fms_nml
      ! regional@chgres
      ! regional@fv_core_nml
      !----------------------------------------------------------------------------------
      grib2_file_input_grid = gfs_3_20190829_0000_000.grb2

--------------------------
Default initial conditions
--------------------------

All supported CompSets use the Hurricane Dorian initialization of 08-29-2019.
In preconfigured platforms, the 08-29-2019 initial conditions are pre-staged in
``$DIN_LOC_IC``. Those are GRIB2 files with 0.5 deg resolution.

The default input data for the Hurricane Dorian initialization of 08-29-2019 is also available
on `NOAA EMC's FTP data repository <https://ftp.emc.ncep.noaa.gov/EIB/UFS/inputdata/canned_winds/201908/20190829/>`_.

-----------------------------------
Running the App for different dates
-----------------------------------

If users want to
run the MR Weather App for dates other than 08-29-2019, they need to make a change in the case to
specify the desired data.  This is done by setting the ``RUN_STARTDATE`` and
``START_TOD`` CIME options using ``./xmlchange``.

CIME will look for the following directory containing initial conditions: ``$DIN_LOC_IC/YYMMMM/YYYYMMDD``.
If the directory is not found, CIME will attempt to retrieve the initial conditions from NOMADS.

---------------------------------------------------------
About the automatic stating of initial conditions by CIME
---------------------------------------------------------

CIME can be used to automatically download GRIB2 initial conditions in 0.5 deg format for the dates
available in the NOMADS server at `<https://nomads.ncdc.noaa.gov/data/gfs4/>`_.
NOMADS has GFS 0.5 deg GRIB2 datasets for the last twelve months. The data will be
retrieved from the server when case.submit command is issued.
Therefore, if users want to start the model from the 0.5 deg GRIB2 data available through
NOMADS, the users do not need to stage the data manually.

As part of the process of generating the UFS MR Weather App executable,
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


If users want to run the UFS MR Weather App with initial conditions other than
0.5 deg GRIB2 data available through NOMADS, they need to stage the data manually.
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

-------------------
Order of operations
-------------------

If you want to download the input data manually, you should do it before you build the UFS MR Weather App.

-----------------------------------------------
Coexistence of multiple files for the same date
-----------------------------------------------

Directory `$DIN_LOC_IC/YYMMMM/YYYYMMDD`` can have both GRIB2 and NEMSIO files for
a given initialization hour and can have files for multiple initialization hours
(00, 06, 12, and 18 UTC).

If a directory has both GRIB2 and NEMSIO files for the same initialization date and time,
CIME will use the GRIB2 files. If the user wants to change this behavior so CIME uses the
NEMSIO files, the user should edit file ``user_nl_ufsatm``
and add

.. code-block:: console

    input_type = "gaussian"

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
