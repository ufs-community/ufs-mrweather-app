.. _introduction:

****************
Introduction
****************

The Unified Forecast System (:term:`UFS`) is a community-based, coupled, comprehensive Earth modeling system. NOAA's operational model suite for numerical weather prediction (NWP) is quickly transitioning to the UFS from a number of different modeling systems. The UFS enables research, development, and contribution opportunities within the broader :term:`Weather Enterprise` (e.g., government, industry, and academia). For more information about the UFS, visit the `UFS Portal <https://ufscommunity.org/>`__.

The UFS includes `multiple applications <https://ufscommunity.org/science/aboutapps/>`__ that span local to global domains and a range of predictive time scales. This documentation describes the UFS Medium-Range Weather (MRW) Application (App), which targets predictions of atmospheric behavior out to about two weeks. The MRW App includes a prognostic atmospheric model, pre- and post-processing tools, and a community workflow. These components are documented within this User's Guide and supported through a `community forum <https://forums.ufscommunity.org/>`__. Additionally, the MRW App has transitioned from a :term:`CIME`-based workflow to the `Global Workflow <https://github.com/NOAA-EMC/global-workflow/>`__. New and improved capabilities for the upcoming release include the option to run in coupled or uncoupled mode, the addition of a verification package (METplus) for both deterministic and ensemble simulations, and support for the updated ``GFS_v17_p8`` physics scheme and stochastic physics. Future work will expand the capabilities of the application to include data assimilation (:term:`DA`) and a forecast restart/cycling capability.

..
   COMMENT: GitHub Discussions aren't live yet for the MRW, but aren't we deprecating the forums soon? Could post in global-workflow Discussions? https://github.com/NOAA-EMC/global-workflow/discussions

The MRW App is `available on GitHub <https://github.com/ufs-community/ufs-mrweather-app.git>`__ and is designed to be code that the community can run and improve. It is portable to a set of `commonly used platforms <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__. A limited set of configurations, such as specific model resolutions and physics options, are documented and supported. This documentation provides a :ref:`Quick Start Guide <quickstart>` and will soon provide a detailed guide for running the MRW Application on supported platforms. It also provides an overview of the release components and details on how to customize or modify different portions of the workflow.

The MRW App v1.1.0 citation is as follows and should be used when presenting results based on research conducted with the App: 

UFS Development Team. (2020, March 11). Unified Forecast System (UFS) Medium-Range Weather (MRW) Application (Version v1.1.0). 

..
   COMMENT: Update release number/links.
   COMMENT: Is the "future work" section accurate?
   COMMENT: Add v2.0.0 wiki page!
   COMMENT: Add "Zenodo. https://doi.org/........."

===========================
How to Use This Document
===========================

This guide instructs both novice and experienced users on downloading, building, and running the MRW Application. Please post questions in the `UFS Forums <https://forums.ufscommunity.org/>`__.

..
   COMMENT: Or post in GitHub Discussions? (not live yet) Or global-workflow Discussions? https://github.com/NOAA-EMC/global-workflow/discussions

.. code-block:: console

   Throughout the guide, this presentation style indicates shell commands and options, 
   code examples, etc.

Variables presented as ``$VAR`` or ``Dir123`` in this User's Guide refer to environment variables, variables in scripts, names of files, or directories. 

File paths or code that include angle brackets (e.g., ``<platform>.env``) indicate that users should insert options appropriate to their MRW App configuration (e.g., ``HERA.env``). 

.. hint:: 
   * To get started running the MRW App, see the :ref:`Quick Start Guide <quickstart>` for beginners or refer to the in-depth chapter on :ref:`Configuring a New Platform <config_new_platform>`.
   * For an outline of MRW App components, see section :numref:`Section %s <components-overview>` below or refer to :numref:`Chapter %s <components>` for a more in-depth treatment.
   * For background information on the MRW App code repositories and directory structure, see :numref:`Section %s <MRWStructure>` below. 

   ..
      COMMENT: Change config new platform ref to ":ref:`Running the Medium-Range Weather Application <build-mrw>`." once it's added. 


.. _MRWPrerequisites:

===============================================
Prerequisites for Using the MRW Application
===============================================

Background Knowledge Prerequisites
=====================================

The instructions in this documentation assume that users have certain background knowledge: 

   * Familiarity with LINUX/UNIX systems
   * Command line basics
   * System configuration knowledge (e.g., compilers, environment variables, paths, etc.)
   * Numerical Weather Prediction
   * Meteorology

..
   COMMENT: Add subpoints!

Additional background knowledge in the following areas could be helpful:

   * High-Performance Computing (HPC) Systems for those running the MRW App on an HPC system
   * Programming (particularly Python) for those interested in contributing to the MRW App code
   * Creating an SSH Tunnel to access HPC systems from the command line
   * Containerization
   * Workflow Managers/Rocoto

..
   COMMENT: Eliminate containerization?


Software/Operating System Requirements
=========================================
The UFS MRW Application has been designed so that any sufficiently up-to-date machine with a UNIX-based operating system should be capable of running the application. NOAA `Level 1 & 2 systems <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__ already have these prerequisites installed. However, users working on other systems must ensure that the following requirements are installed on their system: 

**Minimum Platform Requirements:**

   * UNIX style operating system such as CNL, AIX, Linux, Mac

   ..
      COMMENT: Does it need to be POSIX-compliant, too, as w/SRW, or is that implied? 

   * >44 GB disk space

      * 18 GB input data from GFS for "out-of-the-box" MRW App case
      * 8 GB for :term:`HPC-Stack` full installation
      * 3 GB for ``ufs-mrweather-app`` installation and build
      * 11 GB for 120hr/5-day forecast 
   
   ..
      COMMENT: Update disk space requirements once "out-of-the-box" case, data, & tests are settled on. CHANGE/REVISE all numbers above for accuracy!!!
      COMMENT: What are the memory requirements?

   * Python 3.7+
   
   ..
      COMMENT: Add: ", including prerequisite packages ``jinja2``, ``pyyaml`` and ``f90nml``"??? Or is that just SRW?

   * Perl 5

   * Git client (1.8+)

   * Fortran compiler released since 2018

      * gfortran v9+ or ifort v18+ are the only ones tested, but others may work.

   * C compiler compatible with the Fortran compiler

      * gcc v9+, ifort v18+, and clang v9+ (macOS, native Apple clang or LLVM clang) have been tested

      ..
         COMMENT: Should it be C AND C++???
         COMMENT: Have all of these versions been tested...?
         COMMENT: Do we need curl and wget for MRW?

   * Lmod

The following software is also required to run the MRW Application, but :term:`HPC-Stack` (which contains the software libraries necessary for building and running the MRW App) can be configured to build these requirements:

   * :term:`MPI` (MPICH, OpenMPI, or other implementation)

      * Only **MPICH** or **OpenMPI** can be built with spack-stack. Other options must be installed separately by the user (if desired). 
   
   * `CMake v3.20+ <http://www.cmake.org/>`__

   ..
      COMMENT: Check that this is the case for spack-stack, not just HPC-Stack.

   * `spack-stack <https://github.com/NOAA-EMC/spack-stack>`__ or `HPC-Stack <https://github.com/NOAA-EMC/hpc-stack>`__, which include:

      * `NCEPLIBS <https://github.com/NOAA-EMC/NCEPLIBS>`__
      * `NCEPLIBS-external <https://github.com/NOAA-EMC/NCEPLIBS-external>`__ (includes ESMF)

   ..
      COMMENT: Are more software packages required? Should NCEPLIBS, etc. be listed at all???

Optional but recommended prerequisites for all systems:

   * Conda for installing/managing Python packages
   * Bash v4+
   * Rocoto Workflow Management System (1.3.1)
   * Python packages ``matplotlib``, ``numpy``, ``cartopy``, and ``netCDF4`` for graphics

..
   COMMENT: Are these the only packages need for graphics in MRW? 

After installing these prerequisites, users may continue on to build the MRW App as documented in the :ref:`quickstart`.


.. _components-overview:

==============================
MRW App Components Overview 
==============================

Build System and Workflow
===========================

The MRW Application has a portable CMake-based build system that packages together all the components required to build the MRW Application. Once built, users can generate the Rocoto-based Global Workflow, which will run each task in the proper sequence. (See `Rocoto documentation <https://github.com/christopherwharrop/rocoto/wiki/Documentation>`__ for more on workflow management.) 

..
   COMMENT: Can the app also be run stand-alone (i.e. w/o a workflow manager)?

The MRW Application has been tested on a variety of platforms widely used by researchers, including NOAA High-Performance Computing (HPC) systems (e.g., Hera, Jet), cloud environments, and generic Linux and macOS systems. Four `levels of support <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__ have been defined for the MRW Application. Preconfigured (Level 1) systems already have the required software libraries available in a central location via the :term:`HPC-Stack` or :term:`spack-stack`. The MRW Application is expected to build and run out-of-the-box on these systems, and users can :ref:`download the MRW App code <quickstart>` without first installing prerequisites. On other platforms (Levels 2-4), the required libraries will need to be installed as part of the :ref:`MRW Application build <quickstart>` process. On Level 2 platforms, installation should be straightforward, and the MRW App should build and run successfully. On Level 3 & 4 platforms, users may need to perform additional troubleshooting since little or no pre-release testing has been conducted on these systems.

..
   COMMENT: Is Linux/Mac still supported? Seems like we're not testing it... 
   COMMENT: Switch quickstart ref to DownloadMRWApp/BuildMRW ref once available.
   COMMENT: What about Level 2 systems?! Do we have any?


Data and Pre-Processing Utilities 
=================================================

The MRW App requires input model data in :term:`GRIB2`, :term:`NEMSIO`, or :term:`netCDF` format. The :term:`chgres_cube` pre-processing software, which is part of the `UFS_UTILS <https://github.com/ufs-community/UFS_UTILS>`__ pre-processing utilities package, uses these files to initialize and prepare the model. Additional information about the pre-processor utilities can be found in :numref:`Section %s <utils>`, in the `UFS_UTILS Technical Documentation <https://noaa-emcufs-utils.readthedocs.io/en/latest>`__, and in the `UFS_UTILS Scientific Documentation <https://ufs-community.github.io/UFS_UTILS/index.html>`__.

Forecast Model
==================

Atmospheric Model
--------------------
The prognostic atmospheric model in the UFS MRW Application uses the Finite-Volume Cubed-Sphere
(:term:`FV3`) dynamical core. The :term:`dynamical core` is the computational part of a model that solves the equations of fluid motion for the atmospheric component of the UFS Weather Model. A User's Guide for the UFS :term:`Weather Model` can be found `here <https://ufs-weather-model.readthedocs.io/en/latest/>`__. Additional information about the FV3 dynamical core can be found in the `scientific documentation <https://repository.library.noaa.gov/view/noaa/30725>`__ and the `technical documentation <https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html>`__.

Common Community Physics Package
------------------------------------

The `Common Community Physics Package <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`__ (:term:`CCPP`) supports interoperable atmospheric physics and land surface model options. Atmospheric physics are a set of numerical methods describing small-scale processes such as clouds, turbulence, radiation, and their interactions. The MRW App currently includes the ``GFS_v17_p8`` physics suite as well as :term:`stochastic<Stochastic physics>` options to represent model uncertainty. 

..
   COMMENT: It seems like all but the GFS v16 are designed only for high resolution grids... so why are we including them with this release? It seems like GFS v16 would be more appropriate for the MRW App.

Unified Post-Processor
=========================

The Medium-Range Weather (MRW) Application is distributed with a post-processing tool, the `Unified Post Processor <https://dtcenter.org/community-code/unified-post-processor-upp>`__ (:term:`UPP`). The UPP converts the native :term:`netCDF` output from the model to :term:`GRIB2` format on standard isobaric coordinates in the vertical direction. The UPP can also be used to compute a variety of useful diagnostic fields, as described in the `UPP User's Guide <https://upp.readthedocs.io/en/upp_v10.1.0/InputsOutputs.html#>`__. The UPP output can be used with visualization, plotting and verification packages, or for further downstream post-processing (e.g., statistical post-processing techniques).

.. _Metplus:

METplus Verification Suite
=============================

The Model Evaluation Tools (MET) package is a set of statistical verification tools developed by the `Developmental Testbed Center <https://dtcenter.org/>`__ (DTC) for use by the :term:`NWP` community to help them assess and evaluate the performance of numerical weather predictions. MET is the core component of the enhanced METplus verification framework. METplus spans a wide range of temporal and spatial scales. It is intended to be extensible through additional capabilities developed by the community. More details about METplus can be found in :numref:`Chapter %s <MetplusComponent>` and on the `METplus website <https://dtcenter.org/community-code/metplus>`__.

Visualization Example
=======================

The MRW Application includes Python scripts to create basic visualizations of the model output. The scripts may be used to complete a visual check to verify that the application is producing reasonable results.

.. _MRWStructure:

===========================================
Code Repositories and Directory Structure
===========================================

Hierarchical Repository Structure
=====================================

The :term:`umbrella repository` for the MRW Application is named ``ufs-mrweather-app``. It is available on GitHub at https://github.com/ufs-community/ufs-mrweather-app. An umbrella repository is a repository that pulls in external code, called "externals," from additional repositories. The MRW Application includes the ``manage_externals`` tool and a configuration file called ``Externals.cfg``, which tags the appropriate versions of the external repositories associated with the MRW App (see :numref:`Table %s <top_level_repos>`).

.. _top_level_repos:

.. table::  List of top-level repositories that comprise the UFS MRW Application

   +----------------------------------+---------------------------------------------------------+
   | **Repository Description**       | **Authoritative repository URL**                        |
   +==================================+=========================================================+
   | UFS Medium-Range Weather         | https://github.com/ufs-community/ufs-mrweather-app      |
   | Application Umbrella Repository  |                                                         |
   +----------------------------------+---------------------------------------------------------+
   | Repository for the Global        | https://github.com/NOAA-EMC/global-workflow             |
   | Workflow                         |                                                         |
   +----------------------------------+---------------------------------------------------------+

The Global Workflow ``checkout.sh`` script then checks out the repositories listed in :numref:`Table %s <gw_repos>`. 

.. _gw_repos:

.. table::  List of Global Workflow subcomponents included in the UFS MRW Application

   +----------------------------------+---------------------------------------------------------+
   | **Repository Description**       | **Authoritative repository URL**                        |
   +==================================+=========================================================+
   | UFS Weather Model Repository     | https://github.com/ufs-community/ufs-weather-model      |
   +----------------------------------+---------------------------------------------------------+
   | Repository for UFS utilities,    | https://github.com/ufs-community/UFS_UTILS              |
   | including pre-processing,        |                                                         |
   | chgres_cube, and more            |                                                         |
   +----------------------------------+---------------------------------------------------------+
   | Unified Post Processor (UPP)     | https://github.com/NOAA-EMC/UPP                         |
   | Repository                       |                                                         |
   +----------------------------------+---------------------------------------------------------+
   | Verification package using MET   | https://github.com/NOAA-EMC/EMC_verif-global.git        |
   | and METplus                      |                                                         |
   +----------------------------------+---------------------------------------------------------+

The UFS Weather Model is itself an :term:`umbrella repository` and contains a number of subcomponent repositories, which are documented `here <https://ufs-weather-model.readthedocs.io/en/latest/CodeOverview.html>`__. 

   .. note::
      The MRW Application prerequisite libraries (including NCEP Libraries and external libraries) are not included in the MRW App repository. The :term:`HPC-Stack` and :term:`spack-stack` repositories each assemble these prerequisite libraries. HPC-Stack or spack-stack has already been built on `preconfigured (Level 1) platforms <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__. However, it must be built on other systems. Users can view the HPC-Stack documentation :external:ref:`here <Overview>`. 


.. _TopLevelDirStructure:

Directory Structure
======================
The ``ufs-mrweather-app`` :term:`umbrella repository` structure is determined by the ``local_path`` settings contained within the ``Externals.cfg`` file. After ``manage_externals/checkout_externals`` is run (see :numref:`Chapter %s <quickstart>`), the specific GitHub repositories described in :numref:`Table %s <top_level_repos>` are cloned into the target subdirectories shown below. Directories that will be created as part of the build process appear in parentheses and will not be visible until after the build is complete. Some directories have been removed for brevity.

.. _dir-str:

.. code-block:: console

   ufs-mrweather-app/
      ├── build_global-workflow.sh
      ├── describe_version
      ├── docs
      │   └── UsersGuide
      ├── Externals.cfg
      ├── global-workflow
      │   ├── docs
      │   ├── driver
      │   ├── ecflow
      │   ├── env
      │   ├── exec               # Should this be removed or put in parentheses???
      │   ├── Externals.cfg
      │   ├── fix
      │   ├── gempak
      │   ├── jobs
      │   ├── modulefiles
      │   ├── parm
      │   ├── README.md
      │   ├── scripts
      │   ├── sorc
      │   ├── ush
      │   └── util
      ├── LICENSE.md
      ├── manage_externals
      │   ├── checkout_externals
      │   ├── LICENSE.txt
      │   ├── manic
      │   └── README.md
      ├── plotting_scripts
      │   ├── plot_mrw_cloud_diff.py
      │   ├── plot_mrw.py
      │   ├── python_plotting_documentation.txt
      │   └── sample_output.pdf
      └── README.md

An abbreviated version of the global-workflow directory tree:

.. code-block:: console

   global-workflow/
      ├── docs
      ├── driver
      │   ├── gdas
      │   ├── gfs
      │   └── product
      ├── ecflow
      ├── env
      │   ├── gfs.ver
      │   ├── HERA.env
      │   ├── JET.env
      │   ├── ORION.env
      │   ├── WCOSS_C.env
      │   └── WCOSS_DELL_P3.env
      ├── (exec)
      ├── Externals.cfg
      ├── fix
      ├── gempak
      │   ├── dictionaries
      │   ├── fix
      │   └── ush
      ├── jobs
      │   ├── JGDAS_<JOBS>    # multiple scripts
      │   ├── JGLOBAL_<JOBS>  # multiple scripts
      │   └── rocoto
      ├── modulefiles
      │   ├── module_base.<platform>.lua
      │   ├── modulefile.ww3.<platform>.lua
      │   ├── module-setup.csh.inc
      │   ├── module-setup.sh.inc
      │   ├── workflow_utils.<platform>.lua
      ├── parm
      │   ├── chem
      │   ├── config
      │   ├── mom6
      │   ├── parm_fv3diag
      │   ├── parm_wave
      │   ├── post
      │   ├── product
      │   ├── relo
      │   ├── transfer_<file>.list # multiple files
      │   ├── wave
      │   └── wmo
      ├── README.md
      ├── scripts
      │   ├── exemcsfc_global_sfc_prep.sh
      │   ├── exgdas_<name>.sh               # multiple shell scripts
      │   ├── exgfs_aero_init_aerosol.py
      │   ├── exgfs_<name>.sh                # multiple shell scripts
      │   ├── exglobal_<name>.sh             # multiple shell scripts
      │   ├── run_gfsmos_master.sh.<system>  # multiple shell scripts
      │   ├── run_<name>.sh                  # multiple shell scripts
      ├── sorc
      │   ├── build_<name>.sh       # multiple shell scripts
      │   ├── checkout.sh
      │   ├── cmake
      │   ├── CMakeLists.txt
      │   ├── enkf_chgres_recenter.fd
      │   ├── enkf_chgres_recenter_nc.fd
      │   ├── fbwndgfs.fd
      │   ├── fv3nc2nemsio.fd
      │   ├── gaussian_sfcanl.fd
      │   ├── gfs_bufr.fd
      │   ├── gfs_build.cfg
      │   ├── install
      │   ├── link_workflow.sh
      │   ├── logs
      │   ├── machine-setup.sh
      │   ├── ncl.setup
      │   ├── partial_build.sh
      │   ├── reg2grb2.fd
      │   ├── regrid_nemsio.fd
      │   ├── supvit.fd
      │   ├── syndat_getjtbul.fd
      │   ├── syndat_maksynrc.fd
      │   ├── syndat_qctropcy.fd
      │   ├── tave.fd
      │   ├── tocsbufr.fd
      │   └── vint.fd
      ├── ush
      │   └── rocoto
      └── util
         ├── modulefiles
         ├── sorc
         └── ush
..
   COMMENT: Update this from code repos dirs doc!
   COMMENT: Should exec be removed or put in parentheses? Doesn't appear to be in global-workflow on GitHub.
   COMMENT: See which files/directories are added after the build and put in parentheses?

===========================================================
User Support, Documentation, and Contributing Development
===========================================================
A `forum-based online support system <https://forums.ufscommunity.org>`__ with topical sections provides a centralized location for UFS users and developers to post questions and exchange information. The forum complements the distributed documentation, summarized here for ease of use.

..
   COMMENTS: Are these forums shifting to the EPIC website? If so, when? Update? 

.. _list_of_documentation:

.. table:: Centralized list of documentation

   +----------------------------+---------------------------------------------------------------------------------+
   | **Documentation**          | **Location**                                                                    |
   +============================+=================================================================================+
   | MRW App User's Guide       | https://ufs-mrweather-app.readthedocs.io/en/latest                              |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS_UTILS Technical        | https://noaa-emcufs-utils.readthedocs.io/en/latest                              |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS_UTILS Scientific       | https://ufs-community.github.io/UFS_UTILS/index.html                            |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS Weather Model          | https://ufs-weather-model.readthedocs.io/en/latest                              |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Global Workflow User's     | https://github.com/NOAA-EMC/global-workflow/wiki/Run-Global-Workflow            |
   | Guide                      |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | FV3 Scientific             | https://repository.library.noaa.gov/view/noaa/30725                             |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | FV3 Technical              | https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html                |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Scientific            | https://dtcenter.ucar.edu/GMTB/v6.0.0/sci_doc/index.html                        |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Technical             | https://ccpp-techdoc.readthedocs.io/en/v6.0.0/                                  |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Stochastic Physics         | https://stochastic-physics.readthedocs.io/en/release-public-v3/                 |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | ESMF manual                | https://earthsystemmodeling.org/docs/release/latest/ESMF_usrdoc/                |
   +----------------------------+---------------------------------------------------------------------------------+
   | spack-stack Documentation  | https://spack-stack.readthedocs.io/en/latest/                                   |
   +----------------------------+---------------------------------------------------------------------------------+
   | Unified Post Processor     | https://upp.readthedocs.io/en/latest/                                           |
   +----------------------------+---------------------------------------------------------------------------------+

..
   COMMENT: Update version numbers/links!
   COMMENT: Deleted:
      | Common Infrastructure for  | http://esmci.github.io/cime/versions/ufs_release_v1.1/html/index.html           |
      | Modeling the Earth         |                                                                                 |
      +----------------------------+---------------------------------------------------------------------------------+
   



The UFS community is encouraged to contribute to the development effort of all related
utilities, model code, and infrastructure. Users can post issues in the related GitHub repositories to report bugs or to announce upcoming contributions to the code base. For code to be accepted in the authoritative repositories, users must follow the code management rules of each UFS component repository, which are outlined in the respective User's Guides listed in :numref:`Table %s <list_of_documentation>`. In particular, innovations involving the UFS Weather Model need to be tested using the regression tests described in its User's Guide. These tests are part of the official NOAA policy on accepting innovations into its code base, whereas the MRW App end-to-end tests are meant as a sanity check for users.

..
   COMMENT: Revise this to better reflect WE2E test purposes. 

=================
Future Direction
=================
Users can expect to see incremental improvements and additional capabilities in upcoming releases of the MRW Application to enhance research opportunities and support operational forecast implementations. 

Planned advancements include addition of: 

   * component models for other Earth domains (such as oceans and sea ice)
   * cycled data assimilation for model initialization
   * expansion of supported platforms

..
   COMMENT: Are these up-to-date/accurate? Are any other enhancements in the works for future MRW releases? That GO-CART thing, for example?
   :external:ref:`Spack Stack Documentation <Overview>`


.. bibliography:: references.bib

.. _hpc-stack: https://hpc-stack.readthedocs.io/en/latest/