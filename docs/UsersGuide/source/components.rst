.. _components:

************************
Components
************************

The MRW Application is a combination of several modeling components that work together to prepare, analyze, produce, and post-process forecast data. The major components of the system are:

* Build System (CMake)
* Workflow (``global-workflow``)
* Data and Pre-processing (``UFS_UTILS``)
* Forecast (:term:`UFS` :term:`Weather Model`)
* Post-processing (Unified Post-Processor [:term:`UPP`])


Additionally, the MRW Application includes the following optional components: 

* METplus-based Verification Suite
* Visualization Examples

These components are documented within this User's Guide and supported through a `community forum <https://forums.ufscommunity.org/>`__. 

..
   COMMENT: Will the forum website change?

=====================
Build System
=====================

The MRW Application includes an umbrella `CMake-based build system <https://github.com/NOAA-EMC/CMakeModules>`__ that assembles the components necessary for running the application. This release is supported for use with Linux and Mac operating systems and with Intel or GNU compilers. There is a small set of system libraries that are assumed to be present on the target computer, including CMake, a compiler, and an :term:`MPI` library that enables parallelism. For a full list, see :numref:`Section %s: Prerequisites <software-prereqs>` in the Introduction. 

Prerequisite libraries necessary for the application (e.g., NCEPLIBS and NCEPLIBS-external) are not included in the MRW Application build system but are available pre-built on preconfigured platforms. On other systems, they can be installed as a software bundle via the :term:`HPC-Stack` or :term:`spack-stack`. On preconfigured (Level 1) `platforms <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__, the MRW App is expected to build and run out of the box. Users can proceed directly to the using the workflow, as described in the :ref:`Quick Start Guide <quickstart>`. On configurable (Level 2) platforms, the software stack is expected to install successfully, but it is not available in a central location. Applications and
models are expected to build and run once HPC-Stack or spack-stack has been built. Limited-Test (Level 3) and Build-Only (Level 4) platforms are those in which the developers have built the code but little or no pre-release testing has been conducted, respectively. A complete description of the levels of support, along with a list of preconfigured and configurable platforms can be found `here <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__.

.. _gw:

=====================
Global Workflow
=====================

The MRW Application leverages the Rocoto-based Global Workflow. The Global Workflow repository (``global-workflow``) contains the workflow layer of the application, which ensures that each task in the experiment runs in the proper sequence. The workflow also provides ways to choose the grid resolution, physics namelist options, forecast length in hours, and history file frequency. It also allows for configuration of other elements of the workflow; for example, whether to run some or all of the pre-processing, forecast model, and post-processing steps.

After running the checkout script in the ``sorc`` directory, the Global Workflow also pulls in the code and scripts for the analysis, forecast, and post-processing components. These non-workflow components are known as submodules. Each of the system submodules has its own repository. 

..
   COMMENT: Can the workflow be run using stand-alone scripts on systems w/o Rocoto?

.. _utils:

=======================================
Data and Pre-Processing
=======================================

The MRW App includes the :term:`chgres_cube` pre-processing software, which is part of the `UFS_UTILS <https://github.com/ufs-community/UFS_UTILS>`__ pre-processing utilities package. ``chgres_cube`` converts the Global Forecast System (GFS) analyses to the format needed by the :term:`Weather Model`. GFS Analysis data files are observation files that provide a snapshot of what the state of the atmosphere was at a specific time. Additional information about ``chgres_cube`` can be found in the `UFS_UTILS Technical Documentation <https://noaa-emcufs-utils.readthedocs.io/en/latest/ufs_utils.html#chgres-cube>`__.

..
   COMMENT: What exactly is a GFS analysis?

GFS analyses for initializing the MRW App can be in one of three formats:

   * Gridded Binary v2 (:term:`GRIB2`) format (with 0.50, or 1.0 degree grid spacing),
   * The NOAA Environmental Modeling System (:term:`NEMS`) Input/Output (:term:`NEMSIO`) format, or
   * Network Common Data Form (:term:`NetCDF`) format. Initialization from dates starting on January 1, 2018 are supported. Dates before that may work but are not guaranteed. 

GFS public archives can be accessed through the `THREDDS Data Server at NCEI <https://www.ncei.noaa.gov/thredds/model/gfs.html>`__. A small sample of files in all supported formats can be found at `the EMC FTP site <https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`__. Additionally, public archives of model data can be accessed through the `NOAA Operational Model Archive and Distribution System <https://nomads.ncep.noaa.gov/>`__ (NOMADS). The initial conditions may be pre-staged on disk by the user; alternatively, users can automatically download the files as part of the Global Workflow if they have access to NOAA :term:`HPSS`.

..
   COMMENT: Update links once MRW data bucket is set up. 

.. WARNING::
   For GFS data, dates prior to 1 January 2018 may work but are not guaranteed.

================
Forecast Model
================

The prognostic model in the MRW App is the atmospheric component of the UFS Weather Model, which employs the Finite-Volume Cubed-Sphere (:term:`FV3`) dynamical core. The :term:`dynamical core` is the computational part of a model that solves the equations of fluid motion. The atmospheric model in this release is an updated version of the atmospheric model that is being used in the operational GFS v16. A User's Guide for the UFS :term:`Weather Model` can be found `here <https://ufs-weather-model.readthedocs.io/en/latest/>`__. Additional information about the FV3 dynamical core can be found in the `scientific documentation <https://repository.library.noaa.gov/view/noaa/30725>`__, the `technical documentation <https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html>`__, and on the `NOAA Geophysical Fluid Dynamics Laboratory website <https://www.gfdl.noaa.gov/fv3/>`__.

The UFS Weather Model ingests files produced by ``chgres_cube`` and outputs files in ``netCDF`` format, which use a Gaussian grid in the horizontal direction and model levels in the vertical direction. Supported grid configurations for this release are the global meshes with resolutions of C48 (~200km), C96 (~100 km), C192 (~50 km), C384 (~25 km), and C768 (~13 km), all with 127 vertical levels. The `NOAA Geophysical Fluid Dynamics Laboratory website <https://www.gfdl.noaa.gov/fv3/fv3-grids/>`__ provides more information about FV3 and its grids.  

.. table:: Grid resolutions

   +-----------+--------------+--------------+
   | # Cells   | Degrees      | Resolution   |
   +===========+==============+==============+
   | C48       | 2 degrees    | ~200km       |
   +-----------+--------------+--------------+
   | C96       | 1 degree     | ~ 100km      |
   +-----------+--------------+--------------+
   | C192      | 1/2 degree   | ~ 50km       |
   +-----------+--------------+--------------+
   | C384      | 1/4 degree   | ~ 25km       |
   +-----------+--------------+--------------+
   | C768      | 1/8th degree | ~ 13km       |
   +-----------+--------------+--------------+
   
..
   COMMENT: Are the next two rows applicable?    
   
      | C1152     |              | ~ 9km        |
      +-----------+--------------+--------------+
      | C3072     |              | ~ 3km        |
      +-----------+--------------+--------------+

Physics
============

Interoperable atmospheric physics, along with various land surface model options, are supported through the Common Community Physics Package (:term:`CCPP`), described `here <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`__. Atmospheric physics are a set of numerical methods describing small-scale processes such as clouds, turbulence, radiation, and their interactions. Currently, the ``global-workflow`` uses CCPP v6.0.0, which includes the supported ``GFS_v17_p8`` physics suite. This suite is a prototype of the physics suite that will be used in the operational implementation of the Global Forecast System (GFS) v17. It is expected to evolve before its operational implementation in 2024. The GFS v17 physics suite includes improvements to the microphysics paramaterizations, deep cumulus physics, gravity wave drag, and land surface model compared to the GFS v16 physics suite. ``FV3_GFS_v17_p8`` is used with the ATM configurations of the Weather Model, while ``FV3_GFS_v17_coupled_p8`` is used with the subseasonal-to-seasonal (S2S) configurations of the model. A scientific description of the CCPP parameterizations and suites can be found in the `CCPP Scientific Documentation <https://dtcenter.ucar.edu/GMTB/v6.0.0/sci_doc/index.html>`__, and CCPP technical aspects are described in the `CCPP Technical Documentation <https://ccpp-techdoc.readthedocs.io/en/v6.0.0/>`__. The model namelist has many settings beyond the physics suites that can optimize various aspects of the model for use with each of the supported suites.

The use of :term:`stochastic <Stochastic physics>` processes to represent model uncertainty is also an option in the upcoming release, although the option is off by default in the supported physics suites. Five methods are supported for use separately or in combination: Stochastic Kinetic Energy Backscatter (SKEB), Stochastically Perturbed Physics Tendencies (SPPT), Specific Humidity perturbations (SHUM), Stochastically Perturbed Parameterizations (SPP), and Land Surface Model (LSM) SPP. A User's Guide for the Stochastic Physics options is available `here <https://stochastic-physics.readthedocs.io/en/release-public-v3/>`__. 


================================
Unified Post-Processor (UPP)
================================

The Medium-Range Weather (MRW) Application is distributed with a post-processing tool, the Unified
Post Processor (:term:`UPP`). The UPP converts the native netCDF output from the model to :term:`GRIB2` format on standard isobaric coordinates in the vertical direction. The UPP can also be used to compute a variety of useful diagnostic fields, as described in the `UPP User's Guide <https://upp.readthedocs.io/en/upp_v10.1.0/>`__.

The UPP output can be used with visualization, plotting and verification packages, or for further downstream post-processing (e.g., statistical post-processing techniques).


.. _MetplusComponent:

=============================
METplus Verification Suite
=============================

The enhanced Model Evaluation Tools (`METplus <https://dtcenter.org/community-code/metplus>`__) verification system can be integrated into the MRW App to facilitate forecast evaluation. METplus is a verification framework that spans a wide range of temporal scales (warn-on-forecast to climate) and spatial scales (storm to global). It is supported by the `Developmental Testbed Center (DTC) <https://dtcenter.org/>`__. 

METplus is included as part of the standard installation of the MRW App prerequisite libraries (either :term:`HPC-Stack` or :term:`spack-stack`). It is also preinstalled on many `Level 1 <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__ systems; existing builds can be viewed `here <https://dtcenter.org/community-code/metplus/metplus-4-1-existing-builds>`__. Additionally, METplus is incorporated into the MRW App's Global Workflow via the `EMC_verif-global <https://github.com/NOAA-EMC/EMC_verif-global>`__ subcomponent. This repository is a wrapper for running METplus within the workflow. 

The core components of the METplus framework include the statistical driver, MET, the associated database and display systems known as METviewer and METexpress, and a suite of Python wrappers to provide low-level automation and examples, also called use-cases. MET is a set of verification tools developed for use by the :term:`NWP` community. It matches up grids with either gridded analyses or point observations and applies configurable methods to compute statistics and diagnostics. Extensive documentation is available in the `METplus User’s Guide <https://metplus.readthedocs.io/en/v4.1.0/Users_Guide/overview.html>`__ and `MET User’s Guide <https://met.readthedocs.io/en/main_v10.1/index.html>`__. Documentation for all other components of the framework can be found at the Documentation link for each component on the METplus `downloads <https://dtcenter.org/community-code/metplus/download>`__ page.

Among other techniques, MET provides the capability to compute standard verification scores for comparing deterministic gridded model data to point-based and gridded observations. It also provides ensemble and probabilistic verification methods for comparing gridded model data to point-based or gridded observations. Currently, the MRW App supports the use of :term:`NDAS` observation files in `prepBUFR format <https://nomads.ncep.noaa.gov/pub/data/nccf/com/nam/prod/>`__ (which include conventional point-based surface and upper-air data) for point-based verification. It also supports gridded Climatology-Calibrated Precipitation Analysis (:term:`CCPA`) data for accumulated precipitation evaluation and Multi-Radar/Multi-Sensor (:term:`MRMS`) gridded analysis data for composite reflectivity and :term:`echo top` verification. 

..
   COMMENT: Can MRW use these files just like SRW?

METplus is being actively developed by :term:`NCAR`/Research Applications Laboratory (RAL), NOAA/Earth Systems Research Laboratories (ESRL), and NOAA/Environmental Modeling Center (EMC), and it is open to community contributions.

=========================
Visualization Example
=========================

The MRW Application currently does not include full support for model visualization. A Python script (``plot_mrw.py``) is provided to create basic visualizations of the model output, and a difference plotting script (``plot_mrw_cloud_diff.py``) is also included to visually compare two runs for the same domain and resolution. These scripts are available in the ``plotting_scripts`` directory of the MRW Application. However, this capability is provided only as an example for users familiar with Python and is currently "use at your own risk." 

The scripts are designed to output graphics in ``.png`` format for several standard meteorological variables (i.e., 2-m temperature, hourly precipitation, cloud cover, and 10-m wind) at a user inputted time range on the pre-defined :term:`CONUS` domain. The scripts can be used to visually verify the reasonableness of a forecast. At this time, users who wish to change the plotting domain will need to manually adjust the code, but support for more domains may be expanded in future releases. The scripts' comments and the file ``python_plotting_documentation.txt`` describe the plotting scripts in more detail. Sample plots are provided for a 48-hour forecast initialized on 8/29/2019 00 UTC using :term:`GRIB2`,  :term:`NEMSIO`, or :term:`netCDF` files as input datasets.
