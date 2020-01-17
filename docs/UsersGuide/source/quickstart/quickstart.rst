.. _quickstart:

==========================
Model Workflow Quick Start
==========================

The following quick start guide is for versions of the `UFS Medium-Range Weather Application 
<https://github.com/ufs-community/ufs-mrweather-app>`_ that have already been ported to the local 
target machine. The workflow for building and running the application is built on the CIME
(Common Infrastructure for Modeling Earth) framework.  Please refer to
the `CIME Porting Documentation <http://esmci.github.io/cime/users_guide/porting-cime.html>`_ if CIME
has not yet been ported to the target machine.

If you are new to CIME, please consider reading the
`CIME Case Control System Part 1: Basic Usage <https://esmci.github.io/cime/users_guide/index.html#case-control-system-part-1-basic-usage>`_ first.

This is the procedure for quickly setting up and running a case of UFS Medium-Range Weather Application.

* Download the UFS Medium-Range Weather Application
* Create a case: Details of available component sets and resolutions are available from the ``query_config`` tool located in the ``ufs-mrweather-app/cime/scripts`` directory 

.. code-block:: console

    cd ufs-mrweather-app/cime/scripts
    ./query_config --help


See the `supported component sets <https://ufs-mrapp.readthedocs.io/en/latest/quickstart/configurations.html#supported-component-sets>`_,
`supported model resolutions <https://ufs-mrapp.readthedocs.io/en/latest/quickstart/configurations.html#supported-grids>`_ and `supported
machines <https://ufs-mrapp.readthedocs.io/en/latest/quickstart/configurations.html#supported-platforms-and-compilers>`_ for a complete 
list of UFS Medium-Range Weather Application supported component sets, grids and computational platforms.

.. note::

   Variables presented as ``$VAR`` in this guide typically refer to variables in XML files
   in a case. From within a case directory, you can determine the value of such a
   variable with ``./xmlquery VAR``. In some instances, ``$VAR`` refers to a shell
   variable or some other variable; we try to make these exceptions clear.

Download the application and its components
===========================================

The UFS Medium-Range Weather Application is hosted under GitHub and following steps can be
used to clone the application and download its components such as CIME and `UFS Medium-Range Weather Model
<https://github.com/ufs-community/ufs-weather-model/tree/ufs_public_release>`_.

.. code-block:: console

    git clone https://github.com/ufs-community/ufs-mrweather-app.git
    cd ufs-mrweather-app
    ./manage_externals/checkout_externals 

Create a case
==============

The `create_newcase`_ command creates a case directory containing the scripts and XML
files to configure a case (see below) for the requested resolution, component set, and
machine. **create_newcase** has three required arguments: ``--case``, ``--compset``,
``--res`` and ``--workflow`` (invoke **create_newcase --help** for help).

On machines where a project or account code is needed, you
must either specify the ``--project`` argument to **create_newcase** or set the
``$PROJECT`` variable in your shell environment.

If running on a supported machine, that machine will
normally be recognized automatically and therefore it is *not* required
to specify the ``--machine`` argument to **create_newcase**.

Invoke **create_newcase** as follows:

.. code-block:: console

    ./create_newcase --case CASENAME --compset COMPSET --res GRID --workflow WORKFLOW

where:

- ``CASENAME`` defines the name of your case (stored in the ``$CASE`` XML variable). This
  is a very important piece of metadata that will be used in filenames, internal metadata
  and directory paths. **create_newcase** will create the *case directory* with the same
  name as the ``CASENAME``. If ``CASENAME`` is simply a name (not a path), the case
  directory is created in the directory where you executed create_newcase. If ``CASENAME``
  is a relative or absolute path, the case directory is created there, and the name of the
  case will be the last component of the path. The full path to the case directory will be
  stored in the ``$CASEROOT`` XML variable. 

- ``COMPSET`` is the component set and can be ``GFSv15p2`` or ``GFSv16beta``, which are only
  supported Common Community Physics Package (CCPP) suites. If you would like to learn more about CCPP
  please consider reading the `CCPP Overview <https://ccpp-techdoc.readthedocs.io/en/latest/Overview.html>`.  

- ``GRID`` is the model resolution, which can be ``C96``, ``C192``, ``C384`` and ``C768``.

- ``WORKFLOW`` is the workflow and can be set as ``ufs-mrweather`` or ``ufs-mrweather_wo_post``. The
  ``ufs-mrweather`` includes both pre- and post-processing steps, while ``ufs-mrweather_wo_post`` includes 
  only pre-processing step. In the current version of the UFS Medium-Range Weather Application, the 
  pre-processing step need to be run to generate initial conditions for the UFS Medium-Range Weather Model.
  In this case, the raw input files are provided by `NOAA Operational Model Archive and Distribution System
  (NOMADS) <https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod>`_ and please be aware that the NOMADS
  server only keeps last 10 days data.

Here is an example on NCAR machine Cheyenne with the ``$USER`` shell environment variable
set to your cheyenne login name:

.. code-block:: console

    ./create_newcase --case /glade/scratch/$USER/cases/ufs-mrweather-app-workflow.c96 --compset GFSv15p2 --res C96 --workflow ufs-mrweather

Setting up the case run script
==============================

Issuing the `case.setup`_ command creates scripts needed to run the model
along with namelist ``user_nl_xxx`` files, where xxx denotes the set of components
for the given case configuration such as ``ufsatm`` and ``cpl``. 

cd to the case directory. Following the example from above:

.. code-block:: console

    cd /glade/scratch/$USER/cases/ufs-mrweather-app-workflow.c96

Before invoking **case.setup**, you could modify the ``env_mach_pes.xml`` file in the case directory 
using the `xmlchange`_ command as needed for the experiment (optional). (Note: To edit any of
the env xml files, use the `xmlchange`_ command. **xmlchange --help** can be used for help.)

Please also be aware that you need to provide consistent ``layout``, ``write_tasks_per_group`` and
``write_groups`` namelist options to the model when total number of PEs are changed. 

Invoke the **case.setup** command.

.. code-block:: console

    ./case.setup

Build the executable using the case.build command
=================================================

Modify build settings in ``env_build.xml`` (optional).

Run the build script.

.. code-block:: console

    ./case.build

Users of the NCAR cheyenne system should consider using
`qcmd <https://www2.cisl.ucar.edu/resources/computational-systems/cheyenne/running-jobs/submitting-jobs-pbs>`_
to compile UFS Medium-Range Weather Model on a compute node as follows:

.. code-block:: console

    qcmd -- ./case.build

The UFS Medium-Range Weather Model executable (named as ``ufs.exe``) will appear in the directory given by the
XML variable ``$EXEROOT``, which can be queried using:

.. code-block:: console

   ./xmlquery EXEROOT

Run the case
============

Modify runtime settings in ``env_run.xml`` (optional). Two settings you may want to change
now are:

1. Run length: By default, the model is set to run for 5 days based on the ``$STOP_N`` and
   ``$STOP_OPTION`` variables:

   .. code-block:: console

      ./xmlquery STOP_OPTION,STOP_N

   These default settings can be useful in `troubleshooting
   <http://esmci.github.io/cime/users_guide/troubleshooting.html>`_ runtime problems
   before submitting for a longer time or a production runs. For example, following setting can be used to
   set the simulation lenght to 36-hours. Please, also be aware that ``nyears``, ``nmonths`` and ``nsteps``
   options for ``STOP_OPTION`` are not supported in the UFS Medium-Range Weather Application.

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

4. The default start date (2019-09-09, 00 UTC) can be also changed by following commands

   .. code-block:: console

      ./xmlchange RUN_STARTDATE=YYYY-MM-DD
      ./xmlchange START_TOD=AS_SECOND

   where:

   - ``RUN_STARTDATE`` is the start date and need to be given in YYYY-MM-DD format such as 2020-01-15
   - ``START_TOD`` is the time of day in seconds such as 12 UTC need to be given as 43200 seconds.

Submit the job to the batch queue using the **case.submit** command.

.. code-block:: console

    ./case.submit

Based on the selected workflow (``ufs-mrweather`` or ``ufs-mrweather_wo_post``), the ``case.submit``
command submits a chain of jobs that their dependency is automatically set. For example, ``ufs-mrweather``
workflow submit a job array with three seperate job that will run in an order: pre-processing, simulation 
and post-processing.

When the jobs are complete, most output will *NOT* be written under the case directory, but
instead under some other directories (on NCAR's cheyenne machine, these other directories
will be in ``/glade/scratch/$USER``). Review the following directories and files, whose
locations can be found with **xmlquery** (note: **xmlquery** can be run with a list of
comma separated names and no spaces):

.. code-block:: console

   ./xmlquery RUNDIR,CASE,CASEROOT,DOUT_S,DOUT_S_ROOT

- ``$RUNDIR``

  This directory is set in the ``env_run.xml`` file. This is the
  location where UFS Medium-Range Weather Application was run. There should be log files for the model 
  component (i.e. of the form ufs.log.yymmdd-hhmmss) if ``$DOUT_S == FALSE``. To check that a run 
  completed successfully, check the last several lines of the ufs.log file for the string "PROGRAM nems
  HAS ENDED" and "RESOURCE STATISTICS".

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
.. _porting: http://esmci.github.io/cime/users_guide/porting-cime
.. _query_config: http://esmci.github.io/cime/users_guide/introduction-and-overview.html#discovering-available-cases-with-query-config
.. _create_newcase: http://esmci.github.io/cime/users_guide/create-a-case.html
.. _xmlchange: http://esmci.github.io/cime/Tools_user/xmlchange.html
.. _case.setup: http://esmci.github.io/cime/users_guide/setting-up-a-case.html
