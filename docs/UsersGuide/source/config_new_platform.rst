.. _config_new_platform:

==========================
Configuring a new platform
==========================

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

-  `CMake 3.15  or newer <http://www.cmake.org/>`_

.. _CIME: http://esmci.github.io/cime

Software stack requirements
---------------------------

Add details of software stack requirements (compiler vendor, versions, etc.)


Generic MacOS (homebrew) platform
---------------------------------

CIME defines a generic build for MacOS using homebrew.  You must first
install NCEPLIBS-externals and NCEPLIBS following the `instructions
here. <https://github.com/NOAA-EMC/NCEPLIBS-external/wiki>`_.  Then
you will need to set the environment variable NCEPLIBS_DIR pointing to
the install location (/usr/local/ufs-release-v1).  You will also need
to define a root location for the model input and output data, again
using environment variables.  The following are suggestions:

- ``UFS_INPUT    $HOME/projects``

- ``UFS_SCRATCH  $HOME/projects/scratch``

Create these directories:

- ``mkdir -p $HOME/projects/scratch``

- ``mkdir -p $HOME/projects/ufs_inputdata``

You are now ready to build the ufs-mrweather-app as documented in the :ref:`quickstart`.
Use the optional --machine argument to create_newcase and create_test with value ``homebrew``.

Everything one needs to do to configure a platform
--------------------------------------------------







Porting CIME to a new machine
-----------------------------

This section described the steps needed to port the CIME workflow to a new platform.  

Build and install the "cprnc" tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The CIME testing system uses a tool called "cprnc" to compare NetCDF files. This tool
must be available on the local system in order for the testing system to work properly.
The source code is included with CIME, but it must be compiled and installed one time
on each new platform.

To build "cprnc" use these steps:

.. code-block:: console

      cd $CIMEROOT/tools/cprnc
      CIMEROOT=../.. ../configure --macros-format=Makefile --mpilib=mpi-serial
      CIMEROOT=../.. source ./.env_mach_specific.sh && make

You should now have a _cprnc_ executable. Remember the path to this tool as it will be added to the
`config_machines.xml` file in the next step, in the `CCSM_CPRNC` variable.

Add the new machine description to config_machines.xml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit the file **$CIMEROOT/config/ufs/machines/config_machines.xml** and add a new `<machine/>` entry
under the root XML element. 
A good approach to this is to copy an existing `<machine/>` description and modify it to match
the new machine to which you are porting CIME.  An example entry looks like this:

.. code-block::

    <machine MACH="hera">
      <DESC>NOAA hera system</DESC>
      <NODENAME_REGEX>hfe</NODENAME_REGEX>
      <OS>LINUX</OS>
      <COMPILERS>intel</COMPILERS>
      <MPILIBS>impi</MPILIBS>
      <PROJECT>nems</PROJECT>
      <SAVE_TIMING_DIR/>
      <CIME_OUTPUT_ROOT>/scratch1/NCEPDEV/nems/$USER</CIME_OUTPUT_ROOT>
      <DIN_LOC_ROOT>/scratch1/NCEPDEV/nems/Rocky.Dunlap/INPUTDATA</DIN_LOC_ROOT>
      <DIN_LOC_ROOT_CLMFORC>/scratch1/NCEPDEV/nems/Rocky.Dunlap/INPUTDATA/atm/datm7</DIN_LOC_ROOT_CLMFORC>
      <DOUT_S_ROOT>$CIME_OUTPUT_ROOT/archive/$CASE</DOUT_S_ROOT>
      <BASELINE_ROOT>/scratch1/NCEPDEV/nems/Rocky.Dunlap/BASELINES</BASELINE_ROOT>
      <CCSM_CPRNC>/home/Rocky.Dunlap/bin/cprnc</CCSM_CPRNC>
      <GMAKE>make</GMAKE>
      <GMAKE_J>8</GMAKE_J>
      <BATCH_SYSTEM>slurm</BATCH_SYSTEM>
      <SUPPORTED_BY>NCEP</SUPPORTED_BY>
      <MAX_TASKS_PER_NODE>80</MAX_TASKS_PER_NODE>
      <MAX_MPITASKS_PER_NODE>40</MAX_MPITASKS_PER_NODE>
      <PROJECT_REQUIRED>TRUE</PROJECT_REQUIRED>
      <mpirun mpilib="default">
        <executable>srun</executable>
        <arguments>
          <arg name="num_tasks">-n $TOTALPES</arg>
        </arguments>
      </mpirun>
      <mpirun mpilib="mpi-serial">
        <executable></executable>
      </mpirun>
      <module_system type="module">
        <init_path lang="sh">/apps/lmod/lmod/init/sh</init_path>
        <init_path lang="csh">/apps/lmod/lmod/init/csh</init_path>
        <init_path lang="python">/apps/lmod/lmod/init/env_modules_python.py</init_path>
        <cmd_path lang="sh">module</cmd_path>
        <cmd_path lang="csh">module</cmd_path>
        <cmd_path lang="python">/apps/lmod/lmod/libexec/lmod python</cmd_path>
        <modules compiler="intel">
          <command name="purge"/>
          <command name="load">intel/18.0.5.274</command>
        </modules>
        <modules mpilib="impi">
          <command name="load">netcdf/4.7.0</command>
          <command name="load">impi/2018.0.4</command>
	  <command name="use">/scratch1/BMC/gmtb/software/modulefiles/intel-18.0.5.274/impi-2018.0.4</command>
	  <command name="load">NCEPlibs/1.0.0alpha01</command>
        </modules>
        <modules>
          <command name="use">/scratch1/BMC/gmtb/software/modulefiles/generic</command>
          <command name="load">cmake/3.16.3</command>
        </modules>
      </module_system>
      <environment_variables comp_interface="nuopc">
        <env name="ESMF_RUNTIME_PROFILE">ON</env>
        <env name="ESMF_RUNTIME_PROFILE_OUTPUT">SUMMARY</env>
      </environment_variables>
    </machine>

Many of the XML elements above are self-explanatory.  For details about individual elements `see the config_machines.xml file 
<http://esmci.github.io/cime/users_guide/machine.html#machinefile>`_.

When finished, verify that your **config_machines.xml** file conforms to its schema definition: 

  .. code-block:: console

      cd $CIMEROOT
      xmllint --noout --schema config/xml_schemas/config_machines.xsd config/ufs/machines/config_machines.xml


Add the batch system to config_batch.xml
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Edit the file **$CIMEROOT/config/ufs/machines/config_batch.xml** and add a `<batch_system/>` element 
describing the batch system on the new machine.  Again, this can be done by copying an existing element
and making any needed modifications.  Here is an example batch description:

.. code-block:: 

    <batch_system MACH="hera" type="slurm">
      <batch_submit>sbatch</batch_submit>
      <submit_args>
        <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
        <arg flag="-q" name="$JOB_QUEUE"/>
        <arg flag="--account" name="$PROJECT"/>
      </submit_args>
      <directives>
        <directive>--partition=hera</directive>
      </directives>
      <queues>
        <queue walltimemax="08:00:00" nodemin="1" nodemax="210">batch</queue>
        <queue default="true" walltimemax="00:30:00" nodemin="1" nodemax="210">debug</queue>
      </queues>
    </batch_system>

For more details `see the config_batch.xml file 
<http://esmci.github.io/cime/users_guide/machine.html#config-batch-xml-batch-directives>`_.

To verify correctness of the config_batch.xml file, use the command:

  .. code-block:: console
      cd $CIMEROOT
      xmllint --noout --schema config/xml_schemas/config_batch.xsd config/ufs/machines/config_batch.xml

Verify that the port is working by running a simple test
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have completed the above steps, run the following test to see if you are able to
build and run a basic workflow with the UFS MR Weather application.

  .. code-block:: console

      cd $CIMEROOT/scripts
      ./create_test SMS_Lh5.C96.GFSv15p2 --workflow ufs-mrweather --machine $MACHINE

  The **$MACHINE** is the name of the machine that is added to the **config_machines.xml**.

  This will test the end-to-end workflow including pre-processing, model forecast and post-processing. 
