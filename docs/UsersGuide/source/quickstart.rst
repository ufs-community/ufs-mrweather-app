.. _quickstart:

====================
Workflow Quick Start
====================


The following quick start guide is applicable to versions of the `MR Weather App
<https://github.com/ufs-community/ufs-mrweather-app>`_ that are on preconfigured machines as listed
`here <https://github.com/ufs-community/ufs/wiki/Supported-Platforms-and-Compilers>`_. For other machines, please refer to :numref:`Chapter %s <config_new_platform>` before using the quick start guide.


The workflow for building and running the App is built on the CIME
(Common Infrastructure for Modeling Earth) framework.  Please refer to
the `CIME Porting Documentation <http://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/porting-cime.html>`_
if CIME has not yet been ported to the target machine.

If you are new to CIME, please consider reading the `CIME Case Control System Part 1: Basic Usage
<https://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/index.html#case-control-system-part-1-basic-usage>`_
*after downloading the code*.  The CIME Users Guide will be easier to follow after the
directory structure has been created by the `git clone` command.

This is the procedure for quickly setting up and running a case of MR Weather App.

* Download the MR Weather App
* Create a case: use ``create_newcase``
* Setup  a case: use ``case.setup``
* Build  a case: use ``case.build``
* Run    a case: use ``case.submit``

.. _downloading:

Downloading the MR Weather App code and scripts
==========================================================================

Access to the code requires git. You will need access to the command line clients, ``git``
(v1.8 or greater). You can download the latest version of the release
code:

.. code-block:: console

    git clone https://github.com/ufs-community/ufs-mrweather-app.git -b ufs-v1.1.0 my_ufs_sandbox
    cd my_ufs_sandbox

.. note::
    When cloning the ufs-mrweather-app repository, the connection to github may time out.  In this
    case, resubmit the ``git clone`` command.

The information of being a "detached HEAD" is a standard git notification about a release tag.  If you plan to add development to the codes, you will need a development branch.

To checkout MR Weather Model components, including CIME, run the ``checkout_externals`` script from /path/to/my_ufs_sandbox.

.. code-block:: console

    ./manage_externals/checkout_externals

The ``checkout_externals`` script will read the configuration file ``Externals.cfg`` and
will download the model source and CIME into /path/to/my_ufs_sandbox.

To see more details regarding the checkout_externals script from the command line, type:

.. code-block:: console

    ./manage_externals/checkout_externals --help

To confirm a successful download of all components, you can run ``checkout_externals``
with the status flag to show the status of the externals:

.. code-block:: console

    ./manage_externals/checkout_externals -S

This should show a clean status for all externals, with no characters in the first two
columns of output, as in this example:

.. _top_level_dir_structure:

.. code-block:: console

    Checking status of externals: model, stochastic_physics, fv3, ccpp/framework, atmos_cubed_sphere, ccpp/physics, fms, nems, tests/produtil/nceplibs-pyprodutil, fv3gfs_interface, nems_interface, cime,
        ./cime
        ./src/model
        ./src/model/FMS
        ./src/model/FV3
        ./src/model/FV3/atmos_cubed_sphere
        ./src/model/FV3/ccpp/framework
        ./src/model/FV3/ccpp/physics
        ./src/model/FV3/cime
        ./src/model/NEMS
        ./src/model/NEMS/cime/
        ./src/model/NEMS/tests/produtil/NCEPLIBS-pyprodutil
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

.. _configurations:

Model Configurations
====================

The MR Weather App can be configured at four out-of-the-box
resolutions with two different compsets, ``GFSv15p2`` or
``GFSv16beta``.  These compsets invoke physics suites that use or not
an ocean-evolving parameterization depending on the initial data
provided. See the Introduction for more information on the physics
suites provided with the release and see the frequently-asked
questions (:ref:`FAQ <faq>`) section for more information on compsets,
physics suites, and initial datasets.

* Details of available component sets and resolutions are available from the ``query_config`` tool located in the ``cime/scripts`` directory

.. code-block:: console

   cd $SRCROOT/cime/scripts
   ./query_config --help

where ``$SRCROOT`` is the top directory of the ufs-mrweather-app.

.. _supported-compsets:

Supported component sets
------------------------

The components of the modeling system can be combined in numerous ways to carry out various scientific or
software experiments. A particular mix of components, along with component-specific configuration and/or
namelist settings is referred to as  component set or "compset". The MR Weather App
has a shorthand naming convention for component sets that are supported out-of-the-box.

To determine what MR Weather App compsets are available in the release, use
the following command:

.. code-block:: console

   cd $SRCROOT/cime/scripts
   ./query_config --compsets

This should show a list of available compsets:

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

:term:`CIME` has the flexibility to support numerous model resolutions.
To see the grids that are currently supported, use the following command

.. code-block:: console

   cd $SRCROOT/cime/scripts
   ./query_config --grids

This should show the a list of available grids for this release.

.. code-block:: console

   =========================================
   GRID naming convention
   =========================================
   The notation for the grid longname is
       a%name_l%name_oi%name_r%name_m%mask_g%name_w%name
   where
       a% => atm, l% => lnd, oi% => ocn/ice, r% => river, m% => mask, g% => glc, w% => wav

   Supported grid configurations are given via alias specification in
   the file "config_grids.xml". Each grid alias can also be associated  with the
   following optional attributes

    -------------------------------------------------------------
           default component grids:

    component         compset       value
    -------------------------------------------------------------
    atm      SATM              null
    lnd      SLND              null
    ocnice   SOCN              null
    rof      SROF              null
    glc      SGLC              null
    wav      SWAV              null
    iac      SIAC              null
    -------------------------------------------------------------

    alias: C96
      non-default grids are: atm:C96

    alias: C192
      non-default grids are: atm:C192

    alias: C384
      non-default grids are: atm:C384

    alias: C768
      non-default grids are: atm:C768


As can be seen, MR Weather App currently supports four grids with the following nominal resolutions

* C96 (~100km)
* C192 (~50km),
* C384 (~25km)
* C768 (~13km),

and all with 64 vertical levels.

Setup the environment
=====================

Four environment variables need to be set prior to running the CIME workflow:

.. code-block:: console

     export UFS_INPUT=/path/to/inputs
     export UFS_SCRATCH=/path/to/outputs
     export UFS_DRIVER=nems
     export CIME_MODEL=ufs

``UFS_INPUT`` should be set to the location of a folder where input
data will be accessed.  There should be a folder named
``ufs_inputdata`` underneath this folder.  The folder
``$UFS_INPUT/ufs_inputdata`` should exist before running the CIME
workflow. This is often a shared location on a platform so that all
users on that platform can access data from the same location.

``UFS_SCRATCH`` should be set to the location of a writeable folder
where output will be written for each case.  This is typically a user
scratch space or temporary location with a large allocation available.

The following settings are recommended on the pre-configured platforms:

.. table::  Path settings for pre-configured platforms.

   +-----------------+---------------------------------------------------------+---------------------------+
   | **Platform**    | **$UFS_INPUT**                                          |   **$UFS_SCRATCH**        |
   +=================+=========================================================+===========================+
   | NCAR Cheyenne   | $CESMDATAROOT                                           | /glade/scratch/$USER      |
   +-----------------+---------------------------------------------------------+---------------------------+
   | NOAA Hera       | /scratch1/NCEPDEV/stmp2/CIME_UFS                        | <my-project-dir>/$USER    |
   +-----------------+---------------------------------------------------------+---------------------------+
   | NOAA Jet        | /lfs4/HFIP/hfv3gfs/ufs-release-v1.1/CIME_UFS            | <my-project-dir>/$USER    |
   +-----------------+---------------------------------------------------------+---------------------------+
   | NOAA Gaea       | /lustre/f2/pdata/esrl/gsd/ufs/ufs-release-v1.1/CIME_UFS | <my-project-dir>/$USER    |
   +-----------------+---------------------------------------------------------+---------------------------+


On `platforms that are not pre-configured <https://github.com/ufs-community/ufs/wiki/Supported-Platforms-and-Compilers>`_ a script needs to be executed to define a set of environment variables related to the location of NCEPLIBS dependencies.

.. code-block:: console

     # SH or BASH shells
     source $NCEPLIBS_DIR/bin/setenv_nceplibs.sh

     # CSH or TCSH shells
     source $NCEPLIBS_DIR/bin/setenv_nceplibs.csh

The recommended best practice to set the ``$UFS_SCRATCH`` and
``$UFS_INPUT`` environment variables and source the NCEPLIBS provided
shell script ``setenv_nceplibs.sh|.csh`` is to add the above commands
to a startup script such as ``$HOME/.bashrc`` (Bash shell) or
``$HOME/.tcshrc`` (Tcsh shell). These files are executed automatically
when you start a new shell so that you do not need to re-define them
during each login.

.. important::
     On some platforms (in particular Stampede2) this practice is **required** to ensure the
     environment variables are properly set on compute nodes accessed by the workflow.

Create a case
==============

The `create_newcase`_ command creates a case directory containing the scripts and XML
files to configure a case (see below) for the requested resolution, component set, and
machine. ``create_newcase`` has three required arguments: ``--case``, ``--compset`` and
``--res``.   The ``workflow`` argument is optional, to select alternate workflow components (see below).
The ``project`` argument is optional, to set the batch system project account (see below).
(invoke ``create_newcase --help`` for help).

On machines where a project or account code is needed, you
must either specify the ``--project $PROJECT`` argument in the ``create_newcase`` command, or set the
``$PROJECT`` variable in your shell environment.  If this argument is not set, the default value in config_machines.xml for ``$PROJECT`` will be used. An error will be reported if the default project account is not accessable.

If running on a preconfigured or configurable machine, that machine
will normally be recognized automatically and therefore it is not
required to specify the --machine argument to create_newcase. Generic linux and
macos systems will require the ``--machine`` argument to be used.

Invoke ``create_newcase`` as follows from the ``cime/scripts`` directory:

.. code-block:: console

    cd cime/scripts
    ./create_newcase --case CASENAME --compset COMPSET --res GRID --workflow WORKFLOW

where:

- ``CASENAME`` defines the name of your case (stored in the ``$CASE`` XML variable). This
  is a very important piece of metadata that will be used in filenames, internal metadata
  and directory paths. ``create_newcase`` will create the *case directory* with the same
  name as the ``CASENAME``. If ``CASENAME`` is simply a name (not a path), the case
  directory is created in the ``cime/scripts`` directory where you executed create_newcase.
  If ``CASENAME`` is a relative or absolute path, the case directory is created there and the name of the
  case will be the tail path. The full path to the case directory will be
  stored in the ``$CASEROOT`` XML variable.

- ``COMPSET`` is the component set and can be ``GFSv15p2`` or ``GFSv16beta``, which trigger
  supported Common Community Physics Package (CCPP) suites. If you would like to learn more about CCPP
  please consider reading the `CCPP Overview <https://ccpp-techdoc.readthedocs.io/en/latest/Overview.html>`_.

- ``GRID`` is the model resolution, which can be ``C96``, ``C192``, ``C384`` and ``C768``.

- ``WORKFLOW`` is the workflow and can be set as ``ufs-mrweather`` or ``ufs-mrweather_wo_post``. The
  ``ufs-mrweather`` includes both pre- and post-processing steps, while ``ufs-mrweather_wo_post`` includes
  only pre-processing step. In the current version of the MR Weather App, the
  pre-processing step need to be run to generate initial conditions for the UFS Weather Model.

- ``PROJECT`` is the project or account code needed to run batch jobs. You
  may either specify the ``--project $PROJECT`` argument in the ``create_newcase`` command, or set the
  ``$PROJECT`` variable in your shell environment.

Here is an example on NCAR machine Cheyenne with the ``$USER`` shell environment variable
set to your Cheyenne login name:

.. code-block:: console

    cd cime/scripts
    ./create_newcase --case $UFS_SCRATCH/ufs-mrweather-app-workflow.c96 --compset GFSv15p2 --res C96 --workflow ufs-mrweather

Setting up the case run script
==============================

Issuing the `case.setup`_ command creates scripts needed to run the model
along with namelist ``user_nl_xxx`` files, where xxx denotes the set of components
for the given case configuration such as ``ufsatm`` and ``cpl``.
Selected namelist entries can be customized by editing ``user_nl_xxx``, see :ref:`FAQ <faq>`.

cd to the case directory or case root (``$CASEROOT``) ``$UFS_SCRATCH/ufs-mrweather-app-workflow.c96`` as shown above:

.. code-block:: console

    cd /glade/scratch/$USER/cases/ufs-mrweather-app-workflow.c96

Before invoking ``case.setup``, you could modify the ``env_mach_pes.xml`` file in the case directory
using the `xmlchange`_ command as needed for the experiment (optional). (Note: To edit any of
the env xml files, use the `xmlchange`_ command. ``xmlchange --help`` can be used for help.)

Please also be aware that you need to provide consistent ``layout``, ``write_tasks_per_group`` and
``write_groups`` namelist options to the model when total number of PEs are changed.

Invoke the ``case.setup`` command.

.. code-block:: console

    ./case.setup

.. note::

   The CIME commands ``./xmlquery``, ``./case.setup``, ``./case.build``, ``./case.submit`` examine and modify
   the CIME case, and so, are linked into the directory specified by ``--case`` when the ``./create_newcase`` is run.  They should be run from this case directory.

Build the executable using the case.build command
=================================================

Modify build settings in ``env_build.xml`` (optional).

Run the build script.

.. code-block:: console

    ./case.build

Users of the NCAR cheyenne system should consider using
`qcmd <https://www2.cisl.ucar.edu/resources/computational-systems/cheyenne/running-jobs/submitting-jobs-pbs>`_
to compile UFS Weather Model on a compute node as follows:

.. code-block:: console

    qcmd -- ./case.build

The UFS Weather Model executable (named as ``ufs.exe``) will appear in the directory given by the
XML variable ``$EXEROOT``, which can be queried using:

.. code-block:: console

   ./xmlquery EXEROOT

.. _run_the_case:

Run the case
============

Modify runtime settings in ``env_run.xml`` (optional). Two settings you may want to change
now are:

1. Run length: By default, the model is set to run for 5 days based on the ``$STOP_N`` and
   ``$STOP_OPTION`` variables:

   .. code-block:: console

      ./xmlquery STOP_OPTION,STOP_N

   These default settings can be useful in `troubleshooting
   <http://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/troubleshooting.html>`_ runtime problems
   before submitting for a longer time or a production runs. For example, following setting can be used to
   set the simulation lenght to 36-hours. Please, also be aware that ``nyears``, ``nmonths`` and ``nsteps``
   options for ``STOP_OPTION`` are not supported in the MR Weather App.

   .. code-block:: console

      ./xmlchange STOP_OPTION=nhours,STOP_N=36

2. You can set the ``$DOUT_S`` variable to FALSE to turn off short term archiving:

   .. code-block:: console

      ./xmlchange DOUT_S=FALSE

3. The default job wall clock time, which is set to 12-hours, can be changed for relatively short and
   low-resolution simulations. For example, following commands sets the job wall clock time to 30-minutes.

   .. code-block:: console

      ./xmlchange JOB_WALLCLOCK_TIME=00:30:00
      ./xmlchange USER_REQUESTED_WALLTIME=00:30:00

4. The default start date (2019-08-29, 00 UTC) can be also changed by following commands

   .. code-block:: console

      ./xmlchange RUN_STARTDATE=YYYY-MM-DD
      ./xmlchange START_TOD=AS_SECOND

   where:

   - ``RUN_STARTDATE`` is the start date and need to be given in YYYY-MM-DD format such as 2020-01-15
   - ``START_TOD`` is the time of day in seconds such as 12 UTC need to be given as 43200 seconds.

Submit the job to the batch queue using the ``case.submit`` command.

.. code-block:: console

    ./case.submit

Based on the selected workflow (``ufs-mrweather`` or ``ufs-mrweather_wo_post``), the ``case.submit``
command submits a chain of jobs that their dependency is automatically set. For example, ``ufs-mrweather``
workflow submits a job array with three seperate jobs that will run in an order: pre-processing, simulation
and post-processing.  The first ten characters of the job names will be ``chgres.ufs``, ``run.ufs-mr``, and
``gfs_post.u``, respectively.

When the jobs are complete, most output will *NOT* be written under the case directory, but
instead under some other directories (defined by $UFS_SCRATCH).
Review the following directories and files, whose
locations can be found with ``xmlquery`` (note: ``xmlquery`` can be run with a list of
comma separated names and no spaces):

.. code-block:: console

   ./xmlquery RUNDIR,CASE,CASEROOT,DOUT_S,DOUT_S_ROOT

- ``$RUNDIR``

  This directory is set in the ``env_run.xml`` file. This is the
  location where MR Weather App was run. Log files for each stage of the workflow can be found here.

.. table::  Log files

   +---------------------+--------------------------------------+----------------------------------+
   | **Component**       | **File Name**                        |   **Look for...**                |
   +=====================+======================================+==================================+
   | chgres.ufs          | chgres_cube.yymmdd-hhmmss.log        | "DONE"                           |
   +---------------------+--------------------------------------+----------------------------------+
   | run.ufs-mr          | ufs.log.<jobid>.yymmdd-hhmmss        | "PROGRAM nems HAS ENDED"         |
   +---------------------+--------------------------------------+----------------------------------+
   | gfs_post.ufs        | oi.hhh                               | "PROGRAM UNIFIED_POST HAS ENDED" |
   +---------------------+--------------------------------------+----------------------------------+

- ``$DOUT_S_ROOT/$CASE``

  ``$DOUT_S_ROOT`` refers to the short term archive path location on local disk.
  This path is used by the case.st_archive script when ``$DOUT_S = TRUE``.

  ``$DOUT_S_ROOT/$CASE`` is the short term archive directory for this case. If ``$DOUT_S`` is
  FALSE, then no archive directory should exist. If ``$DOUT_S`` is TRUE, then
  log, history, and restart files should have been copied into a directory
  tree here.

- ``$DOUT_S_ROOT/$CASE/logs``

  The log files should have been copied into this directory if the run completed successfully
  and the short-term archiver is turned on with ``$DOUT_S = TRUE``. Otherwise, the log files
  are in the ``$RUNDIR``.

- ``$CASEROOT``

  There could be standard out and/or standard error files output from the batch system.

- ``$CASEROOT/CaseDocs``

  The case namelist files are copied into this directory from the ``$RUNDIR``.

.. _CIME: http://esmci.github.io/cime
.. _porting: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/porting-cime
.. _query_config: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/introduction-and-overview.html#discovering-available-cases-with-query-config
.. _create_newcase: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/create-a-case.html
.. _xmlchange: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/Tools_user/xmlchange.html
.. _case.setup: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/setting-up-a-case.html
