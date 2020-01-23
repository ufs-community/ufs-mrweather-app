.. _overview:

============
Overview
============

What is the UFS Medium-Range Weather Application
================================================

The Unified Forecast System (UFS) can be configured into multiple
applications. The first of these to be released to the community is
the UFS Medium-Range (MR) Weather Application, which targets
predictions of atmospheric behavior out to about two weeks.  The MR
Weather Application 1.0 includes a prognostic atmospheric model, pre-
and post-processing, and a community workflow, but does not include
data assimilation.

The release is available on `GitHub <https://github.com/ufs-community/ufs-mrweather-app/>`__
and is designed to be a code that the research community can
run and improve. It is portable to a set of commonly used
platforms. Specific configurations of the release (e.g. specific model
resolutions and physics options) are documented and supported.

More information about the UFS Medium-Range Weather Model can be found
in `here <https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/>`_.


How To Use This Document
========================

This guide instructs both novice and experienced users on downloading,
building and running the MR Weather Application.

If you are a new user, we recommend reading the first few sections of
the `CIME`_ documentation which is written so that, as much as
possible, individual sections stand on their own and the `CIME`_
documentation guide can be scanned and sections read in a relatively
ad hoc order.

.. code-block:: console

    Throughout the guide, this presentation style indicates shell
    commands and options, fragments of code, namelist variables, etc.

.. note::

   Variables presented as ``$VAR`` in this guide typically refer to variables in XML files
   in a MR Weather experimental case. From within a case directory, you can determine the value of such a
   variable with ``./xmlquery VAR``. In some instances, ``$VAR`` refers to a shell
   variable or some other variable; we try to make these exceptions clear.

Software/Operating System Prerequisites
---------------------------------------

The following are the external system and software requirements for
installing and running MR Weather Application.

-  UNIX style operating system such as CNL, AIX, Linux, Mac

-  python >= 2.7

-  perl 5

-  git client (1.8 or greater)

-  Fortran compiler with support for Fortran 2003

-  C compiler

-  MPI

-  NCEPLIBS

-  `CMake 2.8.6 or newer <http://www.cmake.org/>`_

.. _CIME: http://esmci.github.io/cime

Workflow and Build System
=========================

The MR Weather Application has a user-friendly workflow and a portable
build system.  The workflow leverages the Common Infrastructure for
Modeling Earth (CIME) Case Control System (CCS) `CIME framework
<http://github.com/ESMCI/cime>`_. This established community workflow
is familiar to many through its use in the Community Earth System
Model (CESM). CIME generates a default namelist for the atmospheric
model and provides a way to change namelist options, such as history
file frequency. It also allows for configuration of other elements of
the workflow; for example, whether to run some or all of the
pre-processing, forecast model, and post-processing steps.

In this release, the CIME-CCS only builds the forecast model using
pre-existing `NCEPLIBS <https://github.com/NOAA-EMC/NCEPLIBS/tree/ufs_release_v1.0>`_ package
that includes the prerequisite libraries for the application, along with pre-
and post-processing softwares. There is a small set of system libraries
that are assumed to be present on the target computer: the cmake build
software, compiler, and MPI library.

The MR Weather Application can be run on both Linux and Mac operating systems with
Intel and GNU compilers. The application can be run out of the box on a number of
different hardware platforms such as the National Oceanic and Atmospheric Administration (NOAA)
research `HERA <https://www.dev.noaa.gov/organization/information-technology/hera>`_,
the National Center for Atmospheric Research (NCAR) `Cheyenne
<https://www2.cisl.ucar.edu/resources/computational-systems/cheyenne>`_,
Texas Advanced Computing Center (TACC), The University of Texas at Austin `Stampede
<https://www.tacc.utexas.edu/systems/stampede>`_ systems, Mac and Linux laptops and desktops.

See the :ref:`platforms` , :ref:`supported-compsets`, and
:ref:`supported-grids` for currently supported platforms, model
configurations and resolutions.

.. _downloading:

Downloading the UFS Medium-Range (MR) Weather Application code and scripts
==========================================================================

Access to the code requires git. You will need access to the command line clients, ``git``
(v1.8 or greater). You can download the latest version of the release
code:

.. code-block::

    git clone -b release-ufs.1.0 https://github.com/ufs-community/ufs-mrweather-app.git my_ufs_sandbox
    cd my_ufs_sandbox

To checkout a previous version of application, first view the available versions:

.. code-block:: console

    git tag --list 'release-ufs*'

To checkout a specific release tag type, for example 0.1:

.. code-block:: console

    git checkout release-ufs.0.1

Finally, to checkout UFS Medium-Range (MR) Weather Model and CIME, run the **checkout_externals** script from /path/to/my_ufs_sandbox.

.. code-block:: console

    ./manage_externals/checkout_externals

The **checkout_externals** script will read the configuration file called ``Externals.cfg`` and
will download model and CIME into /path/to/my_ufs_sandbox.

To see more details regarding the checkout_externals script from the command line, type:

.. code-block:: console

    ./manage_externals/checkout_externals --help

To confirm a successful download of all components, you can run ``checkout_externals``
with the status flag to show the status of the externals:

.. code-block:: console

    ./manage_externals/checkout_externals -S

This should show a clean status for all externals, with no characters in the first two
columns of output, as in this example:

.. code-block:: console

    Checking status of externals: model, stochastic_physics, fv3, ccpp/framework, atmos_cubed_sphere, ccpp/physics, fms, ww3, nems, tests/produtil/nceplibs-pyprodutil, fv3gfs_interface, nems_interface, cime,
    s   ./cime
        ./src/model
        ./src/model/FMS
        ./src/model/FV3
        ./src/model/FV3/atmos_cubed_sphere
        ./src/model/FV3/ccpp/framework
        ./src/model/FV3/ccpp/physics
    s   ./src/model/FV3/cime
        ./src/model/NEMS
        ./src/model/NEMS/cime/
        ./src/model/NEMS/tests/produtil/NCEPLIBS-pyprodutil
        ./src/model/WW3
        ./src/model/stochastic_physics

You should now have a complete copy of the source code in your /path/to/my_ufs_sandbox.

If there were problems obtaining an external, you might instead see something like:

.. code-block:: console

    e-  ./src/model/FV3

This might happen if there was an unexpected interruption while downloading.
First try rerunning ``./manage_externals/checkout_externals``.
If there is still a problem, try running with logging turned on using:

.. code-block:: console

   ./manage_externals/checkout_externals --logging

Check the ``manage_externals.log`` file to see what errors are reported.

Downloading input data
======================

A set of input datasets (fixed files, initial condition etc.) are needed to run the model and
UFS Medium-Range (MR) Weather Model input data are available through a `FTP data repository
<https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`. Datasets can be downloaded on a case by case basis
as needed and CIME-CCS provides tools to check and download input data automatically. The detailed
information about the required input datasets to run UFS Medium-Range (MR) Weather Model can be
found in here.

A local input data directory should exist on the local disk, and it also
needs to be set via the variable ``$DIN_LOC_ROOT`` and ``$DIN_LOC_IC``. By default, ``$DIN_LOC_IC``
is set to ``$DIN_LOC_ROOT/prod`` and all the input files are stored in a hierarchical way in the
``$DIN_LOC_ROOT`` directory but user ia also able to store raw input data that is processed in the
pre-processing step throuch the use of ``$DIN_LOC_IC`` variable. This will allow us to keep input data
in the users local space.

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

.. _platforms:

Preconfigured platforms
=======================

Preconfigured  machines are platforms that have machine specific files and settings scripts and that should
run the  UFS Medium-Range (MR) Weather Application **out-of-the-box** (other than potentially needing to download input files).
Preconfigured are usually listed by their common site-specific name.

To see the list of preconfigured  out of the box platforms, issue the following commands:

.. code-block:: console

    cd $SRCROOT/cime/scripts
    ./query_config --machines

Adding and porting to a new machine
===================================

To add a new machine local batch, run, environment, and compiler information must be added
in the CIME directly ``$SRCROOT/cime/config/ufs/machines directory``.

Detailed information on porting can be found in the `CIME porting guide
<http://esmci.github.io/cime/users_guide/porting-cime.html>`_.

The machine name "userdefined" refers to any machine that the user defines and requires
that a user edit the resulting xml files to fill in information required for the target platform. This
functionality is handy in accelerating the porting process and quickly
getting a case running on a new platform.

Validating your port
--------------------

Although the MR Weather Application can be run out-of-the-box for a variety of resolutions,
component combinations, and machines, MOST combinations of component
sets, resolutions, and machines have not undergone rigorous scientific validation.

  .. todo:: Define the port validation process

.. _configurations:

Model Configurations
====================

The UFS Medium-Range (MR) Weather Application can be configured at four out of the box resolutions
with two different Common Community Physics Package (`CCPP
<https://ccpp-techdoc.readthedocs.io/en/latest/Overview.html>`_) physics suites (``GFSv15p2`` or ``GFSv16beta``).

.. _supported-compsets:

Supported component sets
------------------------

The components of the modeling system can be combined in numerous ways to carry out various scientific or
software experiments. A particular mix of components, along with component-specific configuration and/or
namelist settings is referred to as  component set or "compset". The UFS Medium-Range (MR) Weather Application
has a shorthand naming convention for component sets that are supported out-of-the-box.

To determine what out of the box MR Weather Application compsets are available in the release, do
the following:

.. code-block:: console

    cd $SRCROOT/cime/scripts
    ./query_config --compsets

This should show a list of available compsets, as following:

.. code-block:: console

    Active component: ufsatm
           --------------------------------------
           Compset Alias: Compset Long Name
           --------------------------------------
       GFSv15p2             : FCST_ufsatm%v15p2_SLND_SICE_SOCN_SROF_SGLC_SWAV
       GFSv16beta           : FCST_ufsatm%v16beta_SLND_SICE_SOCN_SROF_SGLC_SWAV

.. _supported-grids:

Supported grids
---------------

CIME has the flexibility to support numerous out-of-the box model resolutions.
To see the grids that are currently supported, call you could call following command

The MR Weather Application currently supports four out of the box grids,

* C96 (~100km)
* C192 (~50km),
* C384 (~25km)
* C768 (~13km),

all with 64 vertical levels.
