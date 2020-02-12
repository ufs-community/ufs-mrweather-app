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

One of the first steps for many users is getting CIME-based models running on their local machine.
This section describes that process.

Steps for porting 
^^^^^^^^^^^^^^^^^

Porting CIME involves several steps. To add a new machine, batch, run, environment, and compiler 
information must be added in the CIME directly ``$SRCROOT/cime/config/ufs/machines directory``.

- cprnc tool need to be build. 

  .. code-block:: console

      cd $CIMEROOT/tools/cprnc
      CIMEROOT=../.. ../configure --macros-format=Makefile --mpilib=mpi-serial
      CIMEROOT=../.. source ./.env_mach_specific.sh && make

  Finally, put the resulting executable in CCSM_CPRNC that will be defined in new section of config_machines.xml

- Then, new platform/machine need to be defined 

  You can edit **$CIMEROOT/config/ufs/machines/config_machines.xml** and add a new entry 
  for your machine. In this case, the exiting platforms in the **config_machines.xml** can be used as a starting
  point or reference. For more details `see the config_machines.xml file 
  <http://esmci.github.io/cime/users_guide/machine.html#machinefile>`_.

  Check to ensure that your **config_machines.xml** file conforms to the CIME schema definition by doing the 

  .. code-block:: console

      cd $CIMEROOT
      xmllint --noout --schema config/xml_schemas/config_machines.xsd config/ufs/machines/config_machines.xml

- If you have a batch system, you may also need to create a **$CIMEROOT/config/$model/machines/config_batch.xml**
  file. For more details `see the config_batch.xml file 
  <http://esmci.github.io/cime/users_guide/machine.html#config-batch-xml-batch-directives>`_.

  .. code-block:: console

      cd $CIMEROOT
      xmllint --noout --schema config/xml_schemas/config_batch.xsd config/ufs/machines/config_batch.xml

- Once you have defined a basic configuration for your machine in your machine and batch xml files, run
  following test to test both CIME and CIME-driven UFS MR-Weather Model.

  .. code-block:: console

      cd $CIMEROOT/scripts
      ./create_test SMS_Lh5.C96.GFSv15p2 --workflow ufs-mrweather --machine $MACHINE

  The **$MACHINE** is the name of the machine that is added to the **config_machines.xml**.

  This will test the end-to-end workflow including pre-processing, forward model and post-processing. The detailed 
  information on testing can be found in the `Testing Section <https://ufs-mrapp.readthedocs.io/en/latest/testing.html>`_.
