.. _repos_and_directories:

=========================================
Code repositories and directory structure
=========================================

This chapter describes the code repositories that comprise the UFS MR Weather App,
without describing, in detail, any of the components. 

Hierarchical Repository Structure
---------------------------------

The umbrella repository for the UFS MR Weather App is named ufs-mrweather-app and is
available on GitHub at https://github.com/ufs-community/ufs-mrweather-app. An umbrella
repository is defined as a repository that includes links, called externals, to additional
repositories.  The UFS MR Weather App includes the ``checkout_externals`` tools along with a
configuration file called ``Externals.cfg``, which describes the external repositories
associated with this umbrella (see :numref:`Table %s <top_level_repos>`).

.. _top_level_repos:

.. table::  List of top-level repositories that comprise the UFS MR Weather App.

   +----------------------------+---------------------------------------------------------+
   | **Repository Description** | **Authoritative repository URL**                        |
   +============================+=========================================================+
   | Umbrella repository for    | https://github.com/ufs-community/ufs-mrweather-app      |
   | the UFS Weather App        |                                                         |
   +----------------------------+---------------------------------------------------------+
   | Umbrella repository for    | https://github.com/ufs-community/ufs-weather-model      |
   | the UFS Weather Model      |                                                         |
   +----------------------------+---------------------------------------------------------+
   | CIME CSS                   | https://github.com/ESMCI/cime                           |
   +----------------------------+---------------------------------------------------------+
   | Layer required for CIME to | https://github.com/ESCOMP/fv3gfs_interface              |
   | build ufs-weather-model    |                                                         |
   +----------------------------+---------------------------------------------------------+
   | Layer required for CIME to | https://github.com/ESCOMP/NEMS_interface                |
   | build NEMS driver          |                                                         |
   +----------------------------+---------------------------------------------------------+

The UFS MR Weather Model is itself an umbrella repository and contains a number of sub-repositories
used by the model as documented `here
<https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/CodeOverview.html>`_.
The CIME repository contains the workflow and build system for the prognostic model.  The last
two repositories provide interfaces to allow CIME to properly build the ufs-weather-model and the NEMS driver.

.. note:: 

   Note that the prerequisite libraries (including NCEP Libraries) are not included in the UFS MR
   Weather App repository.  The source code for these components resides in the `umbrella NCEPLIBS
   repository <https://github.com/NOAA-EMC/NCEPLIBS>`_, which has links to the 
   `chgres_cube preprocessor repository <https://github.com/NOAA-EMC/UFS_UTILS>`_ and to `UPP
   <https://github.com/NOAA-EMC/EMC_post>`_. 

These external components are already built on the preconfigured platforms listed here

.. todo:: add link to a section listing the precongured platforms

or must be cloned and built on other platforms according to the instructions provided in the
`NCEPLIBS wiki page <https://github.com/NOAA-EMC/NCEPLIBS/wiki/Cloning-and-Compiling-NCEPLIBS>`_.
A Users Guide for NCEPLIBS can be found here

.. todo:: add link to NCEPLIBS Users Guide
