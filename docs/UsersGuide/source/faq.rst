.. _faq:

===
FAQ
===

How can I set required environment variables?
=============================================
The best practice is to set environment variables (``UFS_SCRATCH``, ``UFS_INPUT``,
``UFS_DRIVER``, ``CIME_MODEL``, and ``PROJECT``) in the user's enviroment. Some systems
(in particular Stampede2) require to to export them in the ``.bashrc`` (Bash shell) or
``.tcshrc`` (Tcsh shell) files for the batch jobs to function. These environment
variables are then set automatically when a user opens a new shell or logs in to the server
(including compute nodes). In platforms that are not preconfigured, the NCEPLIBS-provided
shell script (``setenv_nceplibs.sh|.csh``) must be sourced in the same way.

**BASH:**

.. code-block:: console

    export UFS_INPUT=/path/to/inputs
    export UFS_SCRATCH=/path/to/outputs
    export PROJECT=your_compute_project
    export UFS_DRIVER=nems
    export CIME_MODEL=ufs
    source /path/to/nceplibs/bin/setenv_nceplibs.sh

**TCSH:**

.. code-block:: console

    setenv UFS_INPUT /path/to/inputs
    setenv UFS_SCRATCH /path/to/outputs
    setenv PROJECT your_compute_project
    setenv UFS_DRIVER nems
    setenv CIME_MODEL ufs
    source /path/to/nceplibs/bin/setenv_nceplibs.csh

How can I see/check the steps in my workflow?
=============================================

A good way to see what ``case.submit`` will do, is to use the ``preview_run`` command,
which will output the environment for your run along with the batch submit and mpirun commands.

.. code-block:: console

    cd $CASEROOT
    ./preview_run

How can I run an individual task in the existing workflow?
==========================================================

The CIME allows you to run a specific task in the workflow by supplying the ``--only-job``
parameter to the ``case.submit`` command.

The following example will run only the preprocessing utility ``chgres_cube``:

.. code-block:: console

    cd $CASEROOT
    ./case.submit --only-job case.chgres

This will create the initial conditions for the model simulation using the raw input files that are
provided by NOAA Operational Model Archive and Distribution System (NOMADS).

To run the simulation:

.. code-block:: console

    cd $CASEROOT
    ./case.submit --only-job case.run

If the user wants to define the first job submitted in a workflow, the ``--job`` parameter can be passed to the ``case.submit`` command.

.. code-block:: console

    cd $CASEROOT
    ./case.submit --job case.run

In this case, two dependent jobs will be submitted: model simulation and post-processing.

How can I change the wall clock time and queue for specific tasks in the workflow?
==================================================================================

These can be done by using the ``xmlchange`` command.

For example, the following command can be used to set the job wall clock time to 10 minutes for ``chgres_cube``

.. code-block:: console

    cd $CASEROOT
    ./xmlchange JOB_WALLCLOCK_TIME=00:10:00 --subgroup case.chgres

The following command will change the job queue to ``bigmem`` for ``chgres_cube``:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange JOB_QUEUE=bigmem --subgroup case.chgres

.. note::

    Without the ``--subgroup`` option, the ``xmlchange`` command changes the job wall clock time for all
    submitted jobs.

What should the wall clock time be for a C768 24-hour forecast on Gaea?
=======================================================================

For this run you should set the ``JOB_WALLCLOCK_TIME`` to one hour. For instructions
on how to do that, see the FAQ above.

How can I change the project account that will be used to submit jobs?
======================================================================

There are two ways to change project account that is used to submit job:

* Set ``PROJECT`` environment variable before creating case
* Use the ``xmlchange`` command to change the project account (please
  replace PROJECT ID with an appropriate project number).

.. code-block:: console

    cd $CASEROOT
    ./xmlchange PROJECT=[PROJECT ID]

.. note::

   A PROJECT environment variable setting will take precident over the case XML setting.


How do I change the processor layout for the UFS Weather Model?
===============================================================

The total number of processor used by the UFS Weather Model can be modified by using ``xmlchange`` command and editing the ``user_nl_ufsatm`` file.

To query the default configuration of the processor layout:

.. code-block:: console

    cd $CASEROOT
    ./pelayout

and to change the default processor layout:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange NTASKS_ATM=150

This will set the total number of processors to 150, but the model configuration files (``model_configure`` and ``input.nml``) must be changed to be
consistent with the total number of processors set by the ``xmlchange`` command.

In this case, the following namelist options need to be modified accordingly:

- **layout**: Processor layout on each tile.
- **ntiles**: Number of tiles on the domain. For the cubed sphere, this should be 6, one tile for each face of the cubed sphere.
- **write_groups**: Number of group for I/O tasks.
- **write_tasks_per_group**: Number of I/O tasks for each group.

The number of tasks assigned to a domain for UFS Medium-Range Weather Model must be equal to:

.. math::

    NTASKS\_ATM = layout_x * layout_y * ntiles + write\_tasks\_per\_group * write\_groups

to have consistent model configuration with **NTASKS_ATM** defined above. ``user_nl_ufsatm`` can be changed as following:

.. code-block:: console

    !----------------------------------------------------------------------------------
    ! Users should add all user specific namelist changes below in the form of
    !   namelist_var = new_namelist_value
    ! Note - that it does not matter what namelist group the namelist_var belongs to
    !----------------------------------------------------------------------------------
    layout = 3,8
    write_groups = 1
    write_tasks_per_group = 6

.. note::

    The model resolution also needs to divide evenly with the layout pair. For the given configuration (C96 resolution), :math:`96/3 = 32` and :math:`96/8 = 12`.

How do I change the number of OPENMP threads?
=============================================

The user may need to change the number of threads to reduce memory consumption for each compute node. This is
especially true for high-resolution cases, and is already set by CIME for C768. This can be done
using the following command:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange NTHRDS_ATM=4
    ./case.setup --reset
    ./case.build --clean-all
    ./case.build

.. note::

    The model needs to be built again if threading is changed from 1. Setting **NTHRDS_ATM** does not require changes in the model
    configuration files. The job submission scripts handle it automatically and submit jobs using more compute nodes.

How do I restart the model?
===========================

To restart the model the ``xmlchange`` command can be used:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange CONTINUE_RUN=TRUE
    ./case.submit

In this case, CIME makes the required changes to the model namelist files (``model_configure`` and ``input.nml``) and also copies the files from the ``RESTART`` to the ``INPUT`` directory.

.. note::

    If there are restart files belonging to multiple time snapshots (i.e. with 20190829.060000., 20190829.120000. prefixes if written every 6-hours), CIME gets the latest one (the files with ``20190829.120000.`` prefix) automatically.

The restart interval can also be changed to a 6 hourly interval as follows:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange REST_OPTION=nhours
    ./xmlchange REST_N=6

.. note::

    The default value of the **restart_interval** namelist option is zero (0), and the model writes a single restart file at the end of the simulation.

The following example demonstrates the 48 hour model simulation split into an initial 24-hour simulation with a cold start plus an additional 24-hour simulation with warm start.

The initial 24 hours simulation:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange STOP_OPTION=nhours
    ./xmlchange STOP_N=24
    ./case.submit

and restart the model for 24 hours simulation:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange CONTINUE_RUN=TRUE
    ./case.submit

.. note::

    The restart run length can be changed using the ``xmlchange`` command and setting ``STOP_N`` and ``STOP_OPTION``.

The model outputs always start from 000 (e.g.,  sfcf000.nc, atmf000.nc), and don't depend on the model start time and method (warm or cold start).

How do I change a namelist option for chgres_cube or the model?
===============================================================
From the case directory running ``./preview_namelists`` will generate the namelists for the run.  This is normally run by ``case.submit``, but you can also run it from the command line after running the command ``case.setup``.   Run it once before editing ``user_nl_ufsatm`` and examine ``input.nml`` to see the default value, then edit ``user_nl_ufsatm`` and run it again to see the change.

Typical usage of ``preview_namelists`` is simply:

.. code-block:: console

   ./preview_namelists

The ``input.nml`` will be generated under the directory CaseDocs,

.. code-block:: console

    ls CaseDocs
    atm_in  config.nml  input.nml  itag.tmp  model_configure

To set model namelist options in CIME, edit the file ``user_nl_ufsatm`` in
the case and add the change(s) as name-value pairs. For example:

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
    do_skeb = T

Then run ``./case.submit``. This will update the namelist and submit the job.

If you want to review what you have done before you submit the case, you can
run ``./preview_namelists`` and then examine the namelist(s) in the run directory
or the case subdirectory ``CaseDocs/``.

Some variables are tied to xml in the case and can only be changed via the
``xmlchange`` command. Attempting to change them by editing the file
``user_nl_ufsatm`` may generate an error.
The parameters that need to be changed via ``xmlchange`` are defined in ``namelist_definition_ufsatm.xml``.

.. code-block:: console

    cd src/model/FV3/cime/cime_config
    cat namelist_definition_ufsatm.xml | grep "modify_via_xml"
    <entry id="ccpp_suite" modify_via_xml="CCPP_SUITES">
    <entry id="start_year" modify_via_xml="RUN_STARTDATE">
    <entry id="start_month" modify_via_xml="RUN_STARTDATE">
    <entry id="start_day" modify_via_xml="RUN_STARTDATE">
    <entry id="start_hour" modify_via_xml="START_TOD">
    <entry id="start_minute" modify_via_xml="START_TOD">
    <entry id="start_second" modify_via_xml="START_TOD">
    <entry id="nhours_fcst" modify_via_xml="STOP_N">
    <entry id="restart_interval" modify_via_xml="REST_N”>

The changes are required to ensure consistency between the model configuration and the CIME.

.. warning::

    The ``user_nl_ufsatm`` file is also used to control namelist options for chgres_cube and NCEP-Post. Different namelist groups in the model namelist and the pre-, post-processing tools could have the same namelist variable. In this case, just using the namelist variable causes failures in the automated namelist generation. The following is the list of namelist variables that needs to be used along with their group name.

    - alpha@nam_physics_nml
    - alpha@test_case_nml
    - avg_max_length@atmos_model_nml
    - avg_max_length@gfs_physics_nml
    - debug@atmos_model_nml
    - debug@gfs_physics_nml
    - icliq_sw@gfs_physics_nml
    - icliq_sw@nam_physics_nml
    - iospec_ieee32@fms_nml
    - iospec_ieee32@fms_io_nml
    - ntiles@fv_core_nml
    - ntiles@nest_nml
    - read_all_pe@fms_io_nml
    - read_all_pe@fms_nml
    - regional@chgres
    - regional@fv_core_nml

How do I turn on stochastic physics?
====================================

There are three types of stochastic physics supported with this release: SPPT, SHUM, and SKEB.
They can be used together or separately, and their use is controlled by setting model namelist options
DO_SPPT, DO_SHUM, DO_SKEB to true or false. These options are set to false by default for all
supported compsets and physics suites.

In addition to the namelist variables that turn stochastic physics on or off, there
are several variables that control the behavior of the physics. Those are explained
in the `Stochastic Physics User's Guide <https://stochastic-physics.readthedocs.io/en/ufs-v1.0.0/namelist_options.html>`_.

In order to set variables DO_SPPT, DO_SHUM, DO_SKEB to true in the model namelist,
as well as to set the values of the variables that customize the stochastic physics,
please see  FAQ entry `How do I change a namelist option for chgres_cube or the model?`

Can I customize the UPP output?
===============================

Starting with v1.1.0, you may customize your output following the instructions in  :numref:`Section %s <upp_output_files>`.

How do I find out which platforms are preconfigured for the MR Weather App?
===========================================================================

Preconfigured machines are platforms that have machine specific files and settings scripts and should
run the MR Weather Application **out-of-the-box** (other than potentially needing to download input files).
Preconfigured platforms are usually listed by their common site-specific name.

To see the list of preconfigured, out of the box platforms, issue the following commands:

.. code-block:: console

    cd $SRCROOT/cime/scripts
    ./query_config --machines

The output will contain entries like the following:

.. code-block:: console

   cheyenne (current) : NCAR SGI platform, os is Linux, 36 pes/node, batch system is PBS
   ('      os             ', 'LINUX')
   ('      compilers      ', 'intel,gnu,pgi')
   ('      mpilibs        ', ['mpt', 'openmpi'])
   ('      pes/node       ', '36')
   ('      max_tasks/node ', '36')

What are the compsets and physics suites supported in this release?
====================================================================

There are two compsets supported in this release: GFSv15p2 and GFSv16beta,
corresponding to the physics suites associated with the operational GFS v15 model
and with the developmental physics for the future implementation of GFS v16.
However, there are four physics suites supported for this release: GFSv15p2,
GFSv15p2_no_nsst, GFSv16beta, and GFSv16beta_no_nsst. The difference between a
suite and its no_nsst counterpart is that the no_nsst suites do not include the
Near Sea Surface Temperature (NSST) ocean parameterization. Instead, they
employ a simple ocean scheme (sfc_ocean) that keeps the sea surface temperature constant
throughout the forecast. Compset GFSv15p2 can use either the GFSv15p2 suite or
the GFSv15p2_no_nsst suite. Similarly, Compset GFSv16beta can use either the
GFSv16beta suite or the GFSv16beta_no_nsst suite. The choice is made based on the
format of the initial conditions file. When GRIB2 format is chosen, the non_nsst
suites are used. When NEMSIO or netCDF format is chosen, the suites with NSST are chosen.
These differences are needed because the GRIB2 files do not have all the fields
needed to initialize the operational NSST parameterization.


How can I change number of task used by chgres_cube or UPP (NCEP-Post)?
=======================================================================

By default, CIME automatically sets number of tasks used by ``chgres_cube`` and NCEP-Post (:term:`UPP`) based on the
resolution of the created case using following logic:

- **chgres_cube**

  It requires that number of task used by chgres_cube need to be divided evenly with the number of tiles (6).

  - C96: closest number of task to tasks_per_node, which can be divided by 6
  - C192: closest number of task to tasks_per_node, which can be divided by 6
  - C384: closest number of task to 2 * tasks_per_node, which can be divided by 6
  - C768: closest number of task to 4 * tasks_per_node, which can be divided by 6

- **UPP**

  - C96: tasks_per_node
  - C192: tasks_per_node
  - C384: 2 * tasks_per_node
  - C768: 4 * tasks_per_node

The number of tasks will increase along with the increased horizontal resolution due to the
memory consumption of the pre-processing tool and **tasks_per_node** is defined for the each platform
using **MAX_MPITASKS_PER_NODE** element (i.e. 36 for NCAR Cheyenne and 48 for TACC Stampede2).

To change the values set automatically by CIME-CSS, the ``xmlchange`` command can be used:

.. code-block:: console

    cd $CASEROOT
    ./xmlchange task_count=72 --subgroup case.chgres

This command will change the number of tasks used by chgres_cube to 72. If the user wants to change the number of
task for NCEP-Post, the subgroup option needs to set to ``case.gfs_post``.

How can I run the MR Weather App for another date without overriding my previous run?
==========================================================================================

Before running the App for a second date, you should save your previous run in
another directory by moving that directory to a different location.

From the case directory do:

.. code-block:: console

   RUNDIR = ` ./xmlquery RUNDIR --value`
   mv $RUNDIR $RUNDIR.forecastdate

How do I diagnose a failure with a high-resolution run?
=======================================================

One possible source of failure with high-resolution runs is lack of memory. To
diagnose if this is the problem, try a low resolution run first.

How can I diagnose errors when building the model?
==================================================

If the ``./case.build`` step fails, the first step is to inspect the build logs
in the case build directories. These files are called ``ufs.bldlog.YYMMDD-HHMMSS``
and ``atm.bldlog.YYMMDD-HHMMSS``, and may be compressed using ``gzip``. In this case,
unzip them using ``gunzip``.

How can I fix cmake build errors of type: This is now an error according to policy CMP0004
==========================================================================================

If the model build fails with an error message like:

.. code-block:: console

   CMake Error at CMakeLists.txt:180 (add_executable):
     Target "NEMS.exe" links to item
     "-L/lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64
     -L/lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64
     -lesmf -cxxlib -lrt -ldl
     /lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64/libnetcdff.a
     /lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64/libnetcdf.a
     /lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64/libhdf5_hl.a
     /lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64/libhdf5.a
     /lustre/f2/pdata/esrl/gsd/ufs/modules/NCEPlibs-ufs-v1.1.0/intel-18.0.6.288/cray-mpich-7.7.11/lib64/libz.a
     -g " which has leading or trailing whitespace.  This is now an error
     according to policy CMP0004.

then this usually means that one of the linker flags that the build process gathered from the ESMF MK file ``esmf.mk`` is either empty
or has trailing whitespaces. The easiest way to fix this is to locate ``esmf.mk`` (in the NCEPLIBS install directory, under ``lib``
or ``lib64``) and check the following entries:

.. code-block:: console

   ESMF_F90COMPILEPATHS
   ESMF_F90ESMFLINKRPATHS
   ESMF_F90ESMFLINKPATHS
   ESMF_F90ESMFLINKLIBS
   ESMF_F90LINKOPTS

If any of these is empty, simply add ``-g`` and make sure that there is no trailing whitespace added after it. For all others, check
that there are no trailing whitespaces. It is advisable to make a backup copy of this file before editing it manually.
