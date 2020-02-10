.. _inputs_and_outputs:

******************
Inputs and Outputs
******************

This chapter provides an overview of the input and output files needed by the components
of the UFS MR Weather App (chgres_cube, the UFS Weather Model, and UPP).  Links to more
detailed documentation for each of the components are provided. 

===========
Input Files
===========

The UFS MR Weather App requires numerous input files.  CIME can copy/link to input files,
run the end-to-end system and write output files to disk.  Depending on the dates requested,
input files can be automatically retrieved by CIME or must be staged by the user.

-----------
chgres_cube
-----------

When a user runs the UFS MR Weather App as described in the quickstart guide, input data for
chgres_cube is linked from a location on disk to your run directory via CIME. The data will
be stored in a hierarchical way in the ``$DIN_LOC_ID`` directory
(see :numref:`Section %s <downloading_input_data>`).  A list of the input files for chgres_cube
can be found here (TODO: add link).

-----------------
UFS Weather Model
-----------------

The input files for the UFS MR Weather Model are located one directory up from the chgres_cube
input files in ``$RUNDIR`` (see :numref:`Section %s <run_the_case>`).   An extensive description
of the input files for the UFS MR Weather Model can be found in the `UFS Weather Model Users Guide
<https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/InputsOutputs.html>`_. 

.. note::
   Due to renaming/linking by CIME, the file names listed in this section differ from the names
   described in the UFS Weather Model Users Guide. 

---------------
UPP Input Files
---------------

Documentation for the input files for UPP are located here (TODO: add link).

============
Output Files
============

The location of the output files written to disk are determined by CIME
(see :numref:`Section %s <run_the_case>`).

-----------
chgres_cube
-----------

The files output by chgres_cube reside in the ``$DIN_LOC_ID`` directory, and are linked by CIME to
files that include the grid name and date in the same directory.  For example:

.. code-block:: console

   sfc_data.tile[1-6].nc -> C96.2019-09-09_00.sfc_data.tile[1-6].nc
   gfs_ctrl.nc -> C96.2019-09-09_00.gfs_ctrl.nc
   gfs_data.tile1.nc -> C96.2019-09-09_00.gfs_data.tile1.nc
 
These output files are used as input for the UFS Weather Model.

-----------------
UFS Weather Model
-----------------

The output files for the UFS Weather Model are described in the `Users Guide
<https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/InputsOutputs.html#output-files>`_.

---------------
UPP Input Files
---------------

Documentation for the Unified Post Processor (UPP) output files can be found here (TODO: add link).

.. _downloading_input_data:

======================
Downloading input data
======================

A set of input datasets (fixed files, initial condition etc.) are needed to run the model and
UFS Medium-Range (MR) Weather Model input data are available through a `FTP data repository
<https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`_. Datasets can be downloaded on a case by case basis
as needed and CIME-CCS provides tools to check and download input data automatically. The detailed
information about the required input datasets to run UFS Medium-Range (MR) Weather Model can be
found in here.

A local input data directory should exist on the local disk, and it also
needs to be set via the variable ``$DIN_LOC_ROOT`` and ``$DIN_LOC_IC``. By default, ``$DIN_LOC_IC``
is set to ``$DIN_LOC_ROOT/prod`` and all the input files are stored in a hierarchical way in the
``$DIN_LOC_ROOT`` directory but user ia also able to store raw input data that is processed in the
pre-processing step throuch the use of ``$DIN_LOC_IC`` variable. This will allow us to keep input data
in the users local space.

.. note::

    If user wants to use exiting data, the files needs to be placed in the directory ``$DIN_LOC_IC`` with 
    pre-defined naming convention such as ``gfs.YYYYMMDD/HH`` (YYYY: year, MM: month, DD: day and HH:hour). 
    Then, user need to set ``RUN_STARTDATE`` and ``START_TOD`` CIME options using ``./xmlchange`` command 
    to use the exiting initial condition. CIME will not attempt the download the raw data from NOMADS server
    once the directory is found.

    The directory must have surface ``gfs.tHHz.sfcanl.nemsio`` and atmospheric conditions 
    ``gfs.tHHz.atmanl.nemsio`` in **nemsio** format to process with pre-processing tool.

For supported machines, these variables are preset and alredy set. For generic machines,
this variables are set via the ``--input-dir`` argument to **create_newcase**.
It is recommended that all users of a given filesystem share the same ``$DIN_LOC_ROOT`` directory but
the user could specialize the ``$DIN_LOC_IC`` variable.

The files in the subdirectories of ``$DIN_LOC_ROOT`` should be write-protected. This prevents these files
from being accidentally modified or deleted. The directories in ``$DIN_LOC_ROOT`` should generally
be group writable, so the directory can be shared among multiple users.

As part of the process of generating the UFS Medium-Range (MR) Weather Application executable,
the utility, **check_input_data** located in each case directory
is called, and it attempts to locate all required input data for the
case based upon file lists generated by components. If the required
static data is not found on local disk in ``$DIN_LOC_ROOT`` and raw initial conditions in ``$DIN_LOC_IC``,
then the data will be downloaded automatically by the scripts or it can be
downloaded by the user by invoking **check_input_data** with the ``--download``
command argument. If you want to download the input data manually you
should do it before you build the UFS Medium-Range (MR) Weather Application.

The UFS Medium-Range (MR) Weather Application currently supports following dataset/s as a raw
input data:

* Global Forecast System (GFS)

  The GFS model is a coupled weather forecast model, composed of four separate models which work
  together to provide an accurate picture of weather conditions. GFS covers the entire globe down
  to a horizontal resolution of 28km.

  The data is distributed through NOAA Operational Model Archive and Distribution System (`NOMADS
  <https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/>`_)

.. note::

    The default input data that belongs to 2019-09-09 00 UTC is also available on `NOAA EMC's FTP data
    repository <https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`_.
