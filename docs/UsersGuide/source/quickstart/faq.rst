.. _faq:
  
===
FAQ
===

How can I see/check the steps in my workflow?
=============================================

A good way to see what _case.submit_ will do, is to use **preview_run** command, 
which will output the environment for your run along with the batch submit and mpirun commands. 
The following is example output for the UFS Medium-Range Weather workflow:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./preview_run

How can I run an individual task in the exiting workflow?
=========================================================

The CIME-CCS allows you to run the specific task in the workflow by supplying the **--only-job** parameter to the **case.submit** command.  

Following the example to run only the preprocessing utility **chgres**

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./case.submit --only-job case.chgres

This will create the initial conditions for the model simulation using the raw input files are provided by NOAA Operational Model 
Archive and Distribution System (NOMADS).

To run the simulation:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./case.submit --only-job case.run 

If user wants to define the first job submitted in a workflow, the **--job** parameter can be pass to the **case.submit** command.

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./case.submit --job case.run

In this case, two dpendent jobs will be submited: model simulation and post-processing. 

How can I change wall clock time for specific task in the workflow?
===================================================================

This can be done by using ``xmlchange`` command. For example, following can be used to set job wall clock time to 10 minutes for **chgres**

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange JOB_WALLCLOCK_TIME=00:10:00 --subgroup case.chgres

.. note::
   
    without **--subgroup** option, the **xmlchange** command chnages the job wall clock time for the simulation itself (**case.run**).

How can I change project account that will be used to submit jobs?
==================================================================

There are two ways to change project account that is used to submit job:

* Set **PROJECT** environment variable before creating case
* Use ``xmlchange`` command to change project account. The following command can be used to change project account for **chgres** task (please replace PROJECT ID with an appropriate project number). 

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange CHARGE_ACCOUNT=[PROJECT ID] --subgroup case.chgres

How do I change the processor layout?
=====================================

The total number of processor used by the UFS Medium-Range Weather Model can be modified by using ``xmlchange`` command and editing ``user_nl_ufsatm`` file.

To query the default configuration of the processor layout:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./pelayout 

and to change the default processor layout:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange NTASKS_ATM=150

This will set the total number of processor to 150 but the model configuration files (**model_configure** and **input.nml**) need to be changed to be
consistent with the total number of processor set by ``xmlchange`` command.

In this case, following namelist options need to be modified accordingly:

- **layout**: Processor layout on each tile.
- **ntiles**: Number of tiles on the domain. For the cubed sphere, this should be 6, one tile for each face of the cubed sphere.
- **write_groups**: Number of group for I/O tasks.
- **write_tasks_per_group**: Number of I/O tasks for each group. 

The number of tasks assigned to a domain for UFS Medium-Range Weather Model needs must equal to

.. math::

    NTASKS\_ATM = layout_x * layout_y * ntiles + write\_tasks\_per\_group * write\_groups

To have consistent model configuration with **NTASKS_ATM** defined above. ``user_nl_ufsatm`` can be changed as following

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

    The model resolution also need to be devided evenly with the layout pair. For the given configuration (C96 resolution), :math:`96/3 = 32` and :math:`96/8 = 12`  

For the high-resolution cases (i.e. C768), user also need to activate threading to reduce memory consumption for each compute node:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange BUILD_THREADED=TRUE
    ./xmlchange NTHRDS_ATM=2

.. note::

    The model needs to be build again by threading support. Setting **NTHRDS_ATM** does not require to make chnages in the model
    configuration files. The job submission scripts handle it automatically and submit jobs using more compute node.

How do I restart the model?
===========================

To restart the model ``xmlchange`` command can be used:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange CONTINUE_RUN=TRUE
    ./case.submit

In this case, CIME-CCS makes the required changes the model namelist files (``model_configure`` and ``input.nml``) and also copies the files from **RESTART** to **INPUT** directory. 

.. note::

    If there are restarts files belongs to multiple time snapshots (i.e. 20190909.060000., 20190909.120000. prefixes if it is written in every 6-hours), CIME-CCS gets the latest one (the files with **20190909.120000.** prefix) automatically.

The restart inteval can be also changed to 6 hourly interval as following:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange REST_OPTION=nhours
    ./xmlchange REST_N=6

.. note::
 
    The default value of **restart_interval** namelist option is zero (0) and the model writes single restart file at the end of the simulation.

The following example demostrates the 48 hours model simulation splited to 24 hours with cold start and another 24 hours simulation with warm start.

The initial 24 hours simulation:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange STOP_OPTION=nhours
    ./xmlchange STOP_N=24
    ./case.submit

and restart the model for 24 hours simulation:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange CONTINUE_RUN=TRUE
    ./case.submit

.. note::

    The restart run lenght can be changed using ``xmlchange`` command by setting **STOP_N** and **STOP_OPTION**.

How do I download new initial condition from NOMADS server?
================================================================

The raw initial condition for UFS Medium-Range (MR) Weather Model is provided by NOAA Operational Model Archive and Distribution System (NOMADS).
The Global Forecast System (GFS) output is processed using provided pre-processing tool (CHGRES) for desired model resolution and date. To download
new raw input data, you just need to chnage the simulation date using following command:

.. code-block:: console

    cd $SRCROOT/cime/scripts/$CASEROOT
    ./xmlchange RUN_STARTDATE=YYYY-MM-DD

.. note::

    By default the raw data will be placed under ``$DIN_LOC_ROOT`` but use can change the location of the raw input data. For example, following
    command can be used to create a directory under ``$SRCROOT/cime/scripts/$CASEROOT`` as ``prod`` to download and place new raw input data.

    .. code-block:: console

        cd $SRCROOT/cime/scripts/$CASEROOT
        ./xmlchange DIN_LOC_IC=`pwd`/prod
        ./preview_namelist

    The ``./case.build`` automatically trigger a command to download data but the download command can be triggered by issuing following command.

    .. code-block:: console

        cd $SRCROOT/cime/scripts/$CASEROOT
        ./check_input_data --download

.. note::

    Please be aware that the NOMADS server only keeps last 10 days data.
