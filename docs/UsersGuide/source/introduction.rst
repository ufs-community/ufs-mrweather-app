.. _introduction:

****************
Introduction
****************

The Unified Forecast System (:term:`UFS`) is a community-based, coupled, comprehensive Earth modeling system. NOAA's operational model suite for numerical weather prediction (NWP) is quickly transitioning to the UFS from a number of different modeling systems. The UFS enables research, development, and contribution opportunities within the broader :term:`Weather Enterprise` (e.g., government, industry, and academia). For more information about the UFS, visit the `UFS Portal <https://ufscommunity.org/>`__.

The UFS includes `multiple applications <https://ufscommunity.org/science/aboutapps/>`__ that span local to global domains and a range of predictive time scales. This documentation describes the UFS Medium-Range Weather (MRW) Application (App), which targets predictions of atmospheric behavior out to about two weeks. This MRW App release includes a prognostic atmospheric model, pre- and post-processing tools, and a community workflow. These components are documented within this User's Guide and supported through a `community forum <https://forums.ufscommunity.org/>`__. Additionally, the MRW App has transitioned from a :term:`CIME`-based workflow to the `global workflow <https://github.com/NOAA-EMC/global-workflow/>`__. New and improved capabilities for the upcoming release include the option to run in coupled or uncoupled mode, the addition of a verification package (METplus) for both deterministic and ensemble simulations and support for four physics schemes and stochastic physics options. Future work will expand the capabilities of the application to include data assimilation (DA) and a forecast restart/cycling capability.

The MRW App is `available on GitHub <https://github.com/ufs-community/ufs-mrweather-app.git>`__ and is designed to be code that the community can run and improve. It is portable to a set of `commonly used platforms <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__. A limited set of configurations of the release, such as specific model resolutions and physics options, are documented and supported. This documentation provides a :ref:`Quick Start Guide <quickstart>` and a detailed guide for running the MRW Application on supported platforms. It also provides an overview of the release components and details on how to customize or modify different portions of the workflow.

The MRW App v1.1.0 citation is as follows and should be used when presenting results based on research conducted with the App: 

UFS Development Team. (2020, March 11). Unified Forecast System (UFS) Medium-Range Weather (MRW) Application (Version v1.1.0). 

..
   COMMENT: Update release number/links; remove reference to "upcoming" release.
   COMMENT: Is the "future work" section accurate?
   COMMENT: Add v2.0.0 wiki page!
   COMMENT: Add "Zenodo. https://doi.org/........."

===========================
How to Use This Document
===========================

This guide instructs both novice and experienced users on downloading, building, and running the MRW Application. Please post questions in the `UFS Forum <https://forums.ufscommunity.org/>`__.

.. code-block:: console

   Throughout the guide, this presentation style indicates shell commands and options, 
   code examples, etc.

Variables presented as ``AaBbCc123`` in this User's Guide typically refer to variables in scripts, names of files, and directories. Variables presented as ``$VAR`` in this guide typically refer to variables in XML files in a MRW App experiment or to environment variables.

File paths or code that include angle brackets (e.g., ``<platform>.env``) indicate that users should insert options appropriate to their MRW App configuration (e.g., ``HERA.env``). 

.. hint:: 
   * To get started running the MRW App, see the :ref:`Quick Start Guide <quickstart>` for beginners or refer to the in-depth chapter on :ref:`Configuring a New Platform <config_new_platform>`.
   * For background information on the MRW App code repositories and directory structure, see :numref:`Section %s <MRWStructure>` below. 
   * For an outline of MRW App components, see section :numref:`Section %s <components-overview>` below or refer to :numref:`Chapter %s <components>` for a more in-depth treatment.

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
      COMMENT: Does it need to be POSIX-compliant, too, as /wSRW, or is that implied? 

   * >40 GB disk space

      * 18 GB input data from GFS, RAP, and HRRR for "out-of-the-box" MRW App case described in :numref:`Chapter %s <quickstart>`
      * 6 GB for :term:`spack-stack` full installation
      * 1 GB for ufs-mrweather-app installation
      * 11 GB for 120hr/5-day forecast 
   
   ..
      COMMENT: change ref to build-mrw once created
   
   * 4GB memory (25km domain)

   ..
      COMMENT: CHANGE/REVISE all numbers above to correspond to MRW!!!
      COMMENT: How large is basic input data for out-of-the-box case? 
      COMMENT: Where does data come from for out-of-the-box case? Probs no RAP or HRRR...
      COMMENT: How much disk space required for spack-stack? For ufs-mrweather-app installation? For forecast? 

   * Python 3.7+

   ..
      COMMENT: Add: ", including prerequisite packages ``jinja2``, ``pyyaml`` and ``f90nml``"??? Or is that just SRW?

   * Perl 5

   * Git client (1.8+)

   * Fortran compiler released since 2018

      * gfortran v9+ or ifort v18+ are the only ones tested, but others may work.

   * C compiler compatible with the Fortran compiler

      * gcc v9+, ifort v18+, and clang v9+ (macOS, native Apple clang or LLVM clang) have been tested

   * Lmod

   ..
      COMMENT: Should it be C AND C++???
      COMMENT: Do we need curl and wget for MRW?
      COMMENT: Have all of these versions been tested...?

The following software is also required to run the MRW Application, but :term:`spack-stack` (which contains the software libraries necessary for building and running the MRW App) can be configured to build these requirements:

   * :term:`MPI` (MPICH, OpenMPI, or other implementation)

      * Only **MPICH** or **OpenMPI** can be built with spack-stack. Other options must be installed separately by the user (if desired). 
   
   * `CMake v3.20+ <http://www.cmake.org/>`__

   ..
      COMMENT: Check that this is the case for spack-stack, not just HPC-Stack.

   * `spack-stack <https://github.com/NOAA-EMC/spack-stack>`__ (or `HPC-Stack <https://github.com/NOAA-EMC/hpc-stack>`__), which includes:

      * `NCEPLIBS-external <https://github.com/NOAA-EMC/NCEPLIBS-external>`__ (includes ESMF)
      * `NCEPLIBS <https://github.com/NOAA-EMC/NCEPLIBS>`__

   ..
      COMMENT: Are more software packages required? Should NCEPLIBS, etc. be listed at all???
      COMMENT: Are all of these version numbers up to date?

..
   COMMENT: Add: "For MacOS systems, some additional software is needed. It is recommended that users install this software using the `Homebrew <https://brew.sh/>`__ package manager for MacOS:" plus 
   COMMENT: ADD MacOS-specific software here!!!
      * bash v4.x
      * GNU compiler suite v.11 or higher with gfortran
      * cmake
      * make
      * coreutils
      * gsed
   More details are in :numref:`Section %s <genericMacOS>`.
   COMMENT: Change above to reflect spack-stack details and/or integrate spack-stack docs.

Optional but recommended prerequisites for all systems:

   * Conda for installing/managing Python packages
   * Bash v4+
   * Rocoto Workflow Management System (1.3.1)
   * Python packages ``scipy``, ``matplotlib``, ``pygrib``, ``cartopy``, and ``pillow`` for graphics

..
   COMMENT: Are these packages need for graphics in MRW? or just SRW?

After installing these prerequisites, users may continue on to build the MRW App as documented in the :ref:`quickstart`.


.. _components-overview:

==============================
MRW App Components Overview 
==============================

Pre-Processor Utilities and Initial Conditions
=================================================

The MRW App requires input model data and the :term:`chgres_cube` pre-processing software, which is part of the `UFS_UTILS <https://github.com/ufs-community/UFS_UTILS>`__ pre-processing utilities package, to initialize and prepare the model. Additional information about the pre-processor utilities can be found in :numref:`Chapter %s <utils>`, in the `UFS_UTILS Technical Documentation <https://noaa-emcufs-utils.readthedocs.io/en/latest>`__, and in the `UFS_UTILS Scientific Documentation <https://ufs-community.github.io/UFS_UTILS/index.html>`__.


Forecast Model
==================

Atmospheric Model
--------------------
The prognostic atmospheric model in the UFS MRW Application uses the Finite-Volume Cubed-Sphere
(:term:`FV3`) dynamical core. The :term:`dynamical core` is the computational part of a model that solves the equations of fluid motion for the atmospheric component of the UFS Weather Model. A User's Guide for the UFS :term:`Weather Model` can be found `here <https://ufs-weather-model.readthedocs.io/en/latest/>`__. Additional information about the FV3 dynamical core can be found in the `scientific documentation <https://repository.library.noaa.gov/view/noaa/30725>` and the `technical documentation <https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html
\>`__.

Common Community Physics Package
------------------------------------

The `Common Community Physics Package <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`__ (:term:`CCPP`) supports interoperable atmospheric physics and land surface model options. Atmospheric physics are a set of numerical methods describing small-scale processes such as clouds, turbulence, radiation, and their interactions. The upcoming MRW App release includes four physics suites and :term:`stochastic<Stochastic physics>` options to represent model uncertainty. 

..
   COMMENT: It seems like all but the GFS v16 are designed only for high resolution grids... so why are we including them with this release? It seems like GFS v16 would be more appropriate for the MRW App.

Unified Post-Processor
=========================

The Medium-Range Weather (MRW) Application is distributed with a post-processing tool, the `Unified Post Processor <https://dtcenter.org/community-code/unified-post-processor-upp>`__ (:term:`UPP`). The UPP converts the native netCDF output from the model to :term:`GRIB2` format on standard isobaric coordinates in the vertical direction. The UPP can also be used to compute a variety of useful diagnostic fields, as described in the `UPP User’s Guide <https://upp.readthedocs.io/en/upp-v9.0.0/>`__. The UPP output can be used with visualization, plotting and verification packages, or for further downstream post-processing (e.g., statistical post-processing techniques).

..
   COMMENT: Do we need to include this? Not sure LBCS exist for a global model, but ICS probably do...
      Data Format
      ==============

      The MRW App supports the use of external model data in :term:`GRIB2`, :term:`NEMSIO`, and :term:`netCDF` format when generating initial and boundary conditions. The UFS Weather Model ingests initial and lateral boundary condition files produced by :term:`chgres_cube`. 
   
   COMMENT: What about this? Are the accepted data formats the same for MRW?

      Unified Post-Processor (UPP)
      ==============================

      The `Unified Post Processor <https://dtcenter.org/community-code/unified-post-processor-upp>`__ (:term:`UPP`) processes raw output from a variety of numerical weather prediction (:term:`NWP`) models. In the MRW App, it converts data output from netCDF format to GRIB2 format. The UPP can also be used to compute a variety of useful diagnostic fields, as described in the `UPP User’s Guide <https://upp.readthedocs.io/en/latest/>`__. 


.. _Metplus:

METplus Verification Suite
=============================

The Model Evaluation Tools (MET) package is a set of statistical verification tools developed by the `Developmental Testbed Center <https://dtcenter.org/>`__ (DTC) for use by the :term:`NWP` community to help them assess and evaluate the performance of numerical weather predictions. MET is the core component of the enhanced METplus verification framework. The suite also includes the associated database and display systems called METviewer and METexpress. METplus spans a wide range of temporal and spatial scales. It is intended to be extensible through additional capabilities developed by the community. More details about METplus can be found in :numref:`Chapter %s <MetplusComponent>` and on the `METplus website <https://dtcenter.org/community-code/metplus>`__.

Visualization Example
=======================

This release does not include support for model visualization. Four basic NCAR Command Language (:term:`NCL`) scripts are provided to create a basic visualization of model output, but this capability is provided only as an example for users familiar with NCL. The scripts may be used to complete a visual check to verify that the application is producing reasonable results.

..
   COMMENT: Is this still true? Should we switch to something like:
      
      The MRW Application includes Python scripts to create basic visualizations of the model output. :numref:`Chapter %s <graphics>` contains usage information and instructions; instructions also appear at the top of the scripts. 
   
   Would need to make a graphics chapter...
   Regardless, the current plotting scripts seem to be in Python, not NCL...


Workflow and Build System
===========================

The MRW Application has a portable CMake-based build system that packages together all the components required to build the MRW Application. Once built, users can generate a Rocoto-based workflow that will run each task in the proper sequence (see `Rocoto documentation <https://github.com/christopherwharrop/rocoto/wiki/Documentation>`__ for more on workflow management). 

..
   COMMENT: Can the app also be run stand-alone (i.e. w/o a workflow manager)?

This MRW Application release has been tested on a variety of platforms widely used by researchers, including NOAA High-Performance Computing (HPC) systems (e.g., Jet, Gaea), cloud environments, and generic Linux and macOS systems. Four `levels of support <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__ have been defined for the MRW Application. Preconfigured (Level 1) systems already have the required software libraries available in a central location via the *spack-stack*. The MRW Application is expected to build and run out-of-the-box on these systems, and users can :ref:`download the MRW App code <quickstart>` without first installing prerequisites. On other platforms (Levels 2-4), the required libraries will need to be installed as part of the :ref:`MRW Application build <quickstart>` process. On Level 2 platforms, installation should be straightforward, and the MRW App should build and run successfully. On Level 3 & 4 platforms, users may need to perform additional troubleshooting since little or no pre-release testing has been conducted on these systems.

..
   COMMENT: Is Linux/Mac still supported? Seems like we're not testing it... 
   COMMENT: Switch quickstart ref to DownloadMRWApp/BuildMRW ref once available.
   COMMENT: What about Level 2 systems?! Do we have any?

.. _MRWStructure:

===========================================
Code Repositories and Directory Structure
===========================================

The :term:`umbrella repository` for the MRW Application is named ``ufs-mrweather-app``. It is available on GitHub at https://github.com/ufs-community/ufs-mrweather-app. An umbrella repository is a repository that houses external code, called "externals," from additional repositories. The MRW Application includes the ``manage_externals`` tool and a configuration file called ``Externals.cfg``, which tags the appropriate versions of the external repositories associated with the MRW App (see :numref:`Table %s <top_level_repos>`).

.. _top_level_repos:

.. table::  List of top-level repositories that comprise the UFS SRW Application

   +----------------------------------+---------------------------------------------------------+
   | **Repository Description**       | **Authoritative repository URL**                        |
   +==================================+=========================================================+
   | Umbrella repository for the UFS  | https://github.com/ufs-community/ufs-mrweather-app      |
   | Medium-Range Weather Application |                                                         |
   +----------------------------------+---------------------------------------------------------+
   | Repository for the global        | https://github.com/NOAA-EMC/global-workflow             |
   | workflow                         |                                                         |
   +----------------------------------+---------------------------------------------------------+

..
   COMMENT: At the moment, only the global workflow is in the checkout externals script. Add the following when updated:

      | Repository for                   | https://github.com/ufs-community/ufs-weather-model      |
      | the UFS Weather Model            |                                                         |
      +----------------------------------+---------------------------------------------------------+
      | Repository for UFS utilities,    | https://github.com/ufs-community/UFS_UTILS              |
      | including pre-processing,        |                                                         |
      | chgres_cube, and more            |                                                         |
      +----------------------------------+---------------------------------------------------------+
      | Repository for the Unified Post  | https://github.com/NOAA-EMC/UPP                         |
      | Processor (UPP)                  |                                                         |
      +----------------------------------+---------------------------------------------------------+

   The UFS Weather Model contains a number of sub-repositories, which are documented `here <https://ufs-weather-model.readthedocs.io/en/latest/CodeOverview.html>`__.

   .. note::
      The prerequisite libraries (including NCEP Libraries and external libraries) are not included in the UFS MRW Application repository. The `spack-stack <https://github.com/NOAA-EMC/spack-stack>`__ repository assembles these prerequisite libraries. The spack-stack has already been built on `preconfigured (Level 1) platforms <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__. However, it must be built on other systems. Users can view the spack-stack documentation :external:ref:`here <index>`. 


.. _TopLevelDirStructure:

Directory Structure
======================
The ``ufs-mrweather-app`` :term:`umbrella repository` structure is determined by the ``local_path`` settings contained within the ``Externals.cfg`` file. After ``manage_externals/checkout_externals`` is run (see :numref:`Chapter %s <quickstart>`), the specific GitHub repositories described in :numref:`Table %s <top_level_repos>` are cloned into the target subdirectories shown below. Directories that will be created as part of the build process appear in parentheses and will not be visible until after the build is complete. Some directories have been removed for brevity.

.. _hierarchical-repo-str:

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
      │   ├── archive
      │   ├── doxygen
      │   ├── note_fixfield.txt
      │   ├── Release_Notes.gfs.v16.0.0.md
      │   └── Release_Notes.gfs.v16.1.0.txt
      ├── driver
      │   ├── gdas
      │   ├── gfs
      │   └── product
      ├── ecflow
      │   └── ecf
      ├── env
      │   ├── gfs.ver
      │   ├── HERA.env
      │   ├── JET.env
      │   ├── ORION.env
      │   ├── WCOSS_C.env
      │   └── WCOSS_DELL_P3.env
      ├── exec
      ├── Externals.cfg
      ├── fix
      ├── gempak
      │   ├── dictionaries
      │   ├── fix
      │   └── ush
      ├── jobs
      │   ├── JGDAS_ATMOS_<JOBNAME>
      │   ├── JGDAS_ENKF_<JOBNAME>
      │   ├── JGFS_ATMOS_<JOBNAME>
      │   ├── JGLOBAL_ATMOS_<JOBNAME>
      │   ├── JGLOBAL_FORECAST
      │   ├── JGLOBAL_WAVE_<JOBNAME>
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
      │   ├── gldas
      │   ├── mom6
      │   ├── mon
      │   ├── parm_fv3diag
      │   ├── parm_wave
      │   ├── post
      │   ├── product
      │   ├── relo
      │   ├── transfer_gdas_1a.list
      │   ├── transfer_gdas_1b.list
      │   ├── transfer_gdas_1c.list
      │   ├── transfer_gdas_enkf_enkf_<##>.list
      │   ├── transfer_gdas_misc.list
      │   ├── transfer_gfs_<##>.list
      │   ├── transfer_gfs_gempak.list
      │   ├── transfer_gfs_misc.list
      │   ├── transfer_gfs_wave_restart<#>.list
      │   ├── transfer_gfs_wave_rundata.list
      │   ├── transfer_gfs_wave_wave.list
      │   ├── transfer_rdhpcs_gdas_enkf_enkf_<#>.list
      │   ├── transfer_rdhpcs_gdas.list
      │   ├── transfer_rdhpcs_gfs.list
      │   ├── transfer_rdhpcs_gfs_nawips.list
      │   ├── wave
      │   └── wmo
      ├── README.md
      ├── scripts
      │   ├── exemcsfc_global_sfc_prep.sh
      │   ├── exgdas_atmos_<name>.sh
      │   ├── exgdas_enkf_<name>.sh
      │   ├── exgfs_aero_init_aerosol.py
      │   ├── exgfs_atmos_<name>.sh
      │   ├── exgfs_nceppost_cpl.sh
      │   ├── exgfs_pmgr.sh
      │   ├── exgfs_prdgen_manager.sh
      │   ├── exgfs_wave_<name>.sh
      │   ├── exglobal_atmos_<name>.sh
      │   ├── exglobal_atmos_tropcy_qc_reloc.sh
      │   ├── exglobal_diag.sh
      │   ├── exglobal_forecast.sh
      │   ├── run_gfsmos_master.sh.<system>
      │   ├── run_reg2grb2.sh
      │   ├── run_regrid.sh
      │   └── vsdbjob_submit.sh
      ├── sorc
      │   ├── build
      │   ├── build_all.sh
      │   ├── build_<name>.sh
      │   ├── calc_analysis.fd
      │   ├── calc_increment_ens.fd
      │   ├── calc_increment_ens_ncio.fd
      │   ├── checkout.sh
      │   ├── cmake
      │   ├── CMakeLists.txt
      │   ├── cpl_build.cfg
      │   ├── emcsfc_ice_blend.fd
      │   ├── emcsfc_snow2mdl.fd
      │   ├── enkf_chgres_recenter.fd
      │   ├── enkf_chgres_recenter_nc.fd
      │   ├── fbwndgfs.fd
      │   ├── fregrid.fd
      │   ├── fv3nc2nemsio.fd
      │   ├── gaussian_sfcanl.fd
      │   ├── gdas2gldas.fd
      │   ├── getsfcensmeanp.fd
      │   ├── getsigensmeanp_smooth.fd
      │   ├── getsigensstatp.fd
      │   ├── gfs_bufr.fd
      │   ├── gfs_build.cfg
      │   ├── gfs_ncep_post.fd
      │   ├── gfs_post.fd
      │   ├── gldas2gdas.fd
      │   ├── gldas.fd
      │   ├── gldas_forcing.fd
      │   ├── gldas_model.fd
      │   ├── gldas_post.fd
      │   ├── gldas_rst.fd
      │   ├── global_cycle.fd
      │   ├── global_enkf.fd
      │   ├── global_gsi.fd
      │   ├── gsi.fd
      │   ├── install
      │   ├── interp_inc.fd
      │   ├── link_workflow.sh
      │   ├── logs
      │   ├── machine-setup.sh
      │   ├── make_hgrid.fd
      │   ├── make_solo_mosaic.fd
      │   ├── ncdiag_cat.fd
      │   ├── ncl.setup
      │   ├── oznmon_horiz.fd
      │   ├── oznmon_time.fd
      │   ├── partial_build.sh
      │   ├── radmon_angle.fd
      │   ├── radmon_bcoef.fd
      │   ├── radmon_bcor.fd
      │   ├── radmon_time.fd
      │   ├── recentersigp.fd
      │   ├── reg2grb2.fd
      │   ├── regrid_nemsio.fd
      │   ├── supvit.fd
      │   ├── syndat_getjtbul.fd
      │   ├── syndat_maksynrc.fd
      │   ├── syndat_qctropcy.fd
      │   ├── tave.fd
      │   ├── tocsbufr.fd
      │   ├── ufs_model.fd
      │   ├── ufs_utils.fd
      │   ├── verif-global.fd
      │   └── vint.fd
      ├── ush
      │   ├── calcanl_gfs.py
      │   ├── calcinc_gfs.py
      │   ├── cplvalidate.sh
      │   ├── drive_makeprepbufr.sh
      │   ├── emcsfc_ice_blend.sh
      │   ├── emcsfc_snow.sh
      │   ├── fix_precip.sh
      │   ├── forecast_det.sh
      │   ├── forecast_postdet.sh
      │   ├── forecast_predet.sh
      │   ├── fv3gfs_downstream_nems_cpl.sh
      │   ├── fv3gfs_downstream_nems.sh
      │   ├── fv3gfs_driver_grid.sh
      │   ├── fv3gfs_dwn_nems.sh
      │   ├── fv3gfs_filter_topo.sh
      │   ├── fv3gfs_make_grid.sh
      │   ├── fv3gfs_make_orog.sh
      │   ├── fv3gfs_nc2nemsio.sh
      │   ├── fv3gfs_regrid_nemsio.sh
      │   ├── fv3gfs_remap.sh
      │   ├── fv3gfs_remap_weights.sh
      │   ├── gaussian_sfcanl.sh
      │   ├── getdump.sh
      │   ├── getges.sh
      │   ├── getncdimlen
      │   ├── gfs_bfr2gpk.sh
      │   ├── gfs_bufr_netcdf.sh
      │   ├── gfs_bufr.sh
      │   ├── gfs_nceppost.sh
      │   ├── gfs_sndp.sh
      │   ├── gfs_transfer.sh
      │   ├── gfs_truncate_enkf.sh
      │   ├── gldas_archive.sh
      │   ├── gldas_forcing.sh
      │   ├── gldas_get_data.sh
      │   ├── gldas_liscrd.sh
      │   ├── gldas_post.sh
      │   ├── gldas_process_data.sh
      │   ├── global_cycle_driver.sh
      │   ├── global_cycle.sh
      │   ├── global_extrkr.sh
      │   ├── global_savefits.sh
      │   ├── gsi_utils.py
      │   ├── hpssarch_gen.sh
      │   ├── icepost.ncl
      │   ├── inter_flux.sh
      │   ├── link_crtm_fix.sh
      │   ├── load_fv3gfs_modules.sh
      │   ├── merge_fv3_aerosol_tile.py
      │   ├── minmon_xtrct_costs.pl
      │   ├── minmon_xtrct_gnorms.pl
      │   ├── minmon_xtrct_reduct.pl
      │   ├── mod_icec.sh
      │   ├── nems.configure.<name>.IN
      │   ├── nems_configure.sh
      │   ├── ocnpost.ncl
      │   ├── ozn_xtrct.sh
      │   ├── parsing_model_configure_DATM.sh
      │   ├── parsing_model_configure_FV3.sh
      │   ├── parsing_namelists_CICE.sh
      │   ├── parsing_namelists_FV3.sh
      │   ├── parsing_namelists_MOM6.sh
      │   ├── radmon_ck_stdout.sh
      │   ├── radmon_err_rpt.sh
      │   ├── radmon_verf_angle.sh
      │   ├── radmon_verf_bcoef.sh
      │   ├── radmon_verf_bcor.sh
      │   ├── radmon_verf_time.sh
      │   ├── rocoto
      │   ├── scale_dec.sh
      │   ├── syndat_getjtbul.sh
      │   ├── syndat_qctropcy.sh
      │   ├── trim_rh.sh
      │   ├── tropcy_relocate_extrkr.sh
      │   ├── tropcy_relocate.sh
      │   ├── WAM_XML_to_ASCII.pl
      │   ├── wave_grib2_sbs.sh
      │   ├── wave_grid_interp_sbs.sh
      │   ├── wave_grid_moddef.sh
      │   ├── wave_outp_cat.sh
      │   ├── wave_outp_spec.sh
      │   ├── wave_prnc_cur.sh
      │   ├── wave_prnc_ice.sh
      │   └── wave_tar.sh
      └── util
         ├── modulefiles
         ├── sorc
         └── ush


Hierarchical Repository Structure
=====================================

..
   COMMENT: Update this from code repos dirs doc!

===========================================================
User Support, Documentation, and Contributing Development
===========================================================
A `forum-based online support system <https://forums.ufscommunity.org>`__ with topical sections
provides a centralized location for UFS users and developers to post questions and exchange information. The forum complements the distributed documentation, summarized here for ease of use.

.. _list_of_documentation:

.. table:: Centralized list of documentation

   +----------------------------+---------------------------------------------------------------------------------+
   | **Documentation**          | **Location**                                                                    |
   +============================+=================================================================================+
   | MRW App v2.0               | https://ufs-mrweather-app.readthedocs.io/en/ufs-v1.1.0                          |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | chgres_cube User's Guide   | https://ufs-utils.readthedocs.io/en/ufs-v1.1.0                                  |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS Weather Model v2.0     | https://ufs-weather-model.readthedocs.io/en/ufs-v1.1.0                          |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | FV3 Documentation          | https://noaa-emc.github.io/FV3_Dycore_ufs-v1.1.0/html/index.html                |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Scientific            | https://dtcenter.org/GMTB/v4.1.0/sci_doc                                        |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Technical             | https://ccpp-techdoc.readthedocs.io/en/v4.1.0                                   |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Stochastic Physics         | https://stochastic-physics.readthedocs.io/en/ufs-v1.1.0                         |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | ESMF manual                | http://www.earthsystemmodeling.org/esmf_releases/public/ESMF_8_0_0/ESMF_refdoc  |
   +----------------------------+---------------------------------------------------------------------------------+
   | Common Infrastructure for  | http://esmci.github.io/cime/versions/ufs_release_v1.1/html/index.html           |
   | Modeling the Earth         |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Unified Post Processor     | https://upp.readthedocs.io/en/upp_v10.1.0/                                      |
   +----------------------------+---------------------------------------------------------------------------------+

..
   COMMENT: Update version numbers/links!

The UFS community is encouraged to contribute to the development effort of all related
utilities, model code, and infrastructure. Users can post issues in the related GitHub repositories to report bugs or to announce upcoming contributions to the code base. For code to be accepted in the authoritative repositories, users must follow the code management rules of each UFS component repository, which are outlined in the respective User's Guides listed in :numref:`Table %s <list_of_documentation>`. In particular, innovations involving the UFS Weather Model need to be tested using the regression tests described in its User’s Guide. These tests are part of the
official NOAA policy on accepting innovations into its code base, whereas the MRW App end-to-end tests
are meant as a sanity check for users.

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

.. _spack-stack: https://spack-stack.readthedocs.io/en/latest/