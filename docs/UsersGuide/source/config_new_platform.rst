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

- The first step is to define your machine. 

  You can edit **$CIMEROOT/config/ufs/machines/config_machines.xml** and add an appropriate section 
  for your machine. For more details `see the config_machines.xml file 
  <http://esmci.github.io/cime/users_guide/machine.html#machinefile>`_.

  The machine name "userdefined" refers to any machine that the user defines and requires
  that a user edit the resulting xml files to fill in information required for the target platform. This
  functionality is handy in accelerating the porting process and quickly getting a case running on a new platform.

  Check to ensure that your **config_machines.xml** file conforms to the CIME schema definition by doing the 

  .. code-block:: console

      cd $CIMEROOT
      xmllint --noout --schema config/xml_schemas/config_machines.xsd config/ufs/machines/config_machines.xml

- If you have a batch system, you may also need to create a **$CIMEROOT/config/$model/machines/config_batch.xml**
  file. For more details `see the config_batch.xml file 
  <http://esmci.github.io/cime/users_guide/machine.html#config-batch-xml-batch-directives>`_.

- Once you have defined a basic configuration for your machine in your machine and batch xml files, run
  following test to test both CIME and CIME-driven UFS MR-Weather Model.

  .. code-block:: console

      ./create_test SMS_Lh5.C96.GFSv15p2 --workflow ufs-mrweather --machine $MACHINE

  The **$MACHINE** is the name of the machine that is added to the **config_machines.xml**.

  .. note::

      If `NCEPLIBS <https://github.com/NOAA-EMC/NCEPLIBS>`_ and `NCEPLIBS-external <https://github.com/NOAA-EMC/NCEPLIBS-external>`_
      are installed to the different locations, then user might need edit **$CIMEROOT/config/ufs/machines/config_machines.xml**
      file and modify ``$ESMFMKFILE`` and ``$NETCDF`` to point **NCEPLIBS-external** installation diretory.

      If ``$ESMFMKFILE`` and ``$NETCDF`` environment variables are already defined then following modification need to be
      done **$CIMEROOT/config/ufs/machines/config_machines.xml** file. 

      .. code-block:: console

          ...
          <env name="ESMFMKFILE">$ENV{ESMFMKFILE}/lib/esmf.mk</env>
          <env name="NETCDF">$ENV{NETCDF}</env>
          ...


  This will test the end-to-end workflow including pre-processing, forward model and post-processing. The detailed 
  information on testing can be found in the `Testing Section <https://ufs-mrapp.readthedocs.io/en/latest/testing.html>`_.
