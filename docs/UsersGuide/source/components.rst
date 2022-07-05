.. _components:

************************
Components
************************

The MRW Application relies on the ``global-workflow`` and its subcomponents, including: 

* Pre-Processor Utilities & Initial Conditions
* :term:`UFS` :term:`Weather Model`
* Unified Post-Processor (:term:`UPP`)
* Build System and Workflow (global-workflow)
* METplus Verification Suite (optional)
* Visualization Examples (optional)

These components are documented within this User's Guide and supported through a `community forum <https://forums.ufscommunity.org/>`__. 

..
   COMMENT: Will the forum website change?

.. _utils:

=======================================
Pre-Processor and Initial Conditions
=======================================

The MRW App includes the :term:`chgres_cube` pre-processing software, which is part of the `UFS_UTILS <https://github.com/ufs-community/UFS_UTILS>`__ pre-processing utilities package. ``chgres_cube`` converts the Global Forecast System (GFS) analyses to the format needed by the :term:`Weather Model`. Additional information about ``chgres_cube`` can be found in the `UFS_UTILS Technical Documentation <https://noaa-emcufs-utils.readthedocs.io/en/latest/ufs_utils.html#chgres-cube>`__.

..
   COMMENT: What exactly is a GFS analysis?

GFS analyses for initializing the MRW App can be in one of three formats:

   * Gridded Binary v2 (:term:`GRIB2`) format (with 0.50, or 1.0 degree grid spacing),
   * The NOAA Environmental Modeling System (:term:`NEMS`) Input/Output (:term:`NEMSIO`) format, or
   * Network Common Data Form (:term:`NetCDF`) format. Initialization from dates starting on January 1, 2018 are supported. Dates before that may work but are not guaranteed. 

GFS public archives can be accessed through the `THREDDS Data Server at NCEI <https://www.ncei.noaa.gov/thredds/model/gfs.html>`__. A small sample of files in all supported formats can be found at `the EMC FTP site <https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`__. Additionally, public archives of model data can be accessed through the `NOAA Operational Model Archive and Distribution System <https://nomads.ncep.noaa.gov/>`__ (NOMADS). The initial conditions may be pre-staged on disk by the user; alternatively, users can automatically downloaded the files as part of the global workflow if they have access to NOAA :term:`HPSS`.

..
   COMMENT: Update links once MRW data bucket is set up. 

.. WARNING::
   For GFS data, dates prior to 1 January 2018 may work but are not guaranteed.

================
Forecast Model
================

The prognostic model in the MRW App is the atmospheric component of the UFS Weather Model, which employs the Finite-Volume Cubed-Sphere (:term:`FV3`) dynamical core. The :term:`dynamical core` is the computational part of a model that solves the equations of fluid motion. The atmospheric model in this release is an updated version of the atmospheric model that is being used in the operational GFS v16. A User's Guide for the UFS :term:`Weather Model` can be found `here <https://ufs-weather-model.readthedocs.io/en/latest/>`__. Additional information about the FV3 dynamical core is available `here <https://noaa-emc.github.io/FV3_Dycore_ufs-v2.0.0/html/index.html>`__.

The UFS Weather Model ingests files produced by ``chgres_cube`` and outputs files in ``netCDF`` format, which use a Gaussian grid in the horizontal direction and model levels in the vertical direction. Supported grid configurations for this release are the global meshes with resolutions of C96 (~100 km), C192 (~50 km), C384 (~25 km), and C768 (~13 km), all with 127 vertical levels. The `NOAA Geophysical Fluid Dynamics Laboratory website <https://www.gfdl.noaa.gov/fv3>`__ provides more information about FV3 and its grids. Additional information about the FV3 dynamical core is available at `here <https://noaa-emc.github.io/FV3_Dycore_ufs-v1.1.0/html/index.html>`__. 

..
   COMMENT: Will (C48 = 2­ degree ≈ 200km) be supported?


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
   | C1152     |              | ~ 9km        |
   +-----------+--------------+--------------+
   | C3072     |              | ~ 3km        |
   +-----------+--------------+--------------+


Interoperable atmospheric physics, along with various land surface model options, are supported through the Common Community Physics Package (:term:`CCPP`), described `here <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`__. Atmospheric physics are a set of numerical methods describing small-scale processes such as clouds, turbulence, radiation, and their interactions. There are currently four physics suites supported for the upcoming MRW release. The first is the ``FV3_RRFS_v1beta`` physics suite, which is being tested for use in the future operational implementation of the Rapid Refresh Forecast System (RRFS) planned for 2023-2024, and the second is ``FV3_GFS_v16``, which is an updated version of the physics suite used in the operational Global Forecast System (GFS) v16. Additionally, ``FV3_WoFS_v0`` and ``FV3_HRRR`` will be supported. A scientific description of the CCPP parameterizations and suites can be found in the `CCPP Scientific Documentation <https://dtcenter.ucar.edu/GMTB/v6.0.0/sci_doc/index.html>`__, and CCPP technical aspects are described in the `CCPP Technical Documentation <https://ccpp-techdoc.readthedocs.io/en/v6.0.0/>`__. The model namelist has many settings beyond the physics suites that can optimize various aspects of the model for use with each of the supported suites. 

The use of :term:`stochastic <Stochastic physics>` processes to represent model uncertainty is also an option in the upcoming release, although the option is off by default in the supported physics suites. Five methods are supported for use separately or in combination: Stochastic Kinetic Energy Backscatter (SKEB), Stochastically Perturbed Physics Tendencies (SPPT), and Specific Humidity perturbations (SHUM).
A `User's Guide for the Use of Stochastic Physics <https://stochastic-physics.readthedocs.io/en/release-public-v3/>`__ is provided. Additionally, there are Stochastically Perturbed Parameterizations (SPP) and Land Surface Model (LSM) Stochastically Perturbed Parameterizations. 

..
   COMMENT: It seems like all but the GFS v16 are designed only for high resolution grids... so why are we including them with this release? It seems like GFS v16 would be more appropriate for the MRW App.
..
   COMMENT: The paragraph above formerly said: "Two of them are variations of an updated version of the physics :term:`suite` used in the operational GFS v15, while the other two are variations of an experimental suite that includes a subset of the developments for the next version of GFS, GFS v16. The variations pertain to how the sea surface temperature (SST) is initialized and parameterized to evolve, and are chosen depending on the type of initial conditions for the App. Initial conditions in :term:`GRIB2` format have a single two-dimensional field to initialize the SST, which must be kept constant throughout the forecast. Initial conditions in :term:`NEMSIO` or :term:`netCDF` format have two two-dimensional fields that describe the baseline SST and its near-surface perturbation related to the diurnal cycle, enabling the use of the near-sea-surface-temperature (NSST) physical parameterization to forecast the temporal variation in SST due to the diurnal cycle." What, if any, of this should be included? 
   COMMENT: Add more detail on SPP/LSM/SPP?

================================
Unified Post-Processor (UPP)
================================

The Medium-Range Weather (MRW) Application is distributed with a post-processing tool, the Unified
Post Processor (:term:`UPP`). The UPP converts the native netCDF output from the model to :term:`GRIB2` format on standard isobaric coordinates in the vertical direction. The UPP can also be used to compute a variety of useful diagnostic fields, as described in the `UPP User's Guide <https://upp.readthedocs.io/en/ufs-v1.1.0>`__.

The UPP output can be used with visualization, plotting and verification packages, or for further downstream post-processing (e.g., statistical post-processing techniques).


.. _MetplusComponent:

=============================
METplus Verification Suite
=============================

The enhanced Model Evaluation Tools (`METplus <https://dtcenter.org/community-code/metplus>`__) verification system has been integrated into the MRW App to facilitate forecast evaluation. METplus is a verification framework that spans a wide range of temporal scales (warn-on-forecast to climate) and spatial scales (storm to global). It is supported by the `Developmental Testbed Center (DTC) <https://dtcenter.org/>`__. 

METplus is included as part of the standard installation of the MRW App prerequistite *:term:`spack-stack`*. It is also preinstalled on all `Level 1 <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__ systems; existing builds can be viewed `here <https://dtcenter.org/community-code/metplus/metplus-4-1-existing-builds>`__. 

..
   COMMENT: Is METplus installation supported for the release?

The core components of the METplus framework include the statistical driver, MET, the associated database and display systems known as METviewer and METexpress, and a suite of Python wrappers to provide low-level automation and examples, also called use-cases. MET is a set of verification tools developed for use by the :term:`NWP` community. It matches up grids with either gridded analyses or point observations and applies configurable methods to compute statistics and diagnostics. Extensive documentation is available in the `METplus User’s Guide <https://metplus.readthedocs.io/en/v4.1.0/Users_Guide/overview.html>`__ and `MET User’s Guide <https://met.readthedocs.io/en/main_v10.1/index.html>`__. Documentation for all other components of the framework can be found at the Documentation link for each component on the METplus `downloads <https://dtcenter.org/community-code/metplus/download>`__ page.

Among other techniques, MET provides the capability to compute standard verification scores for comparing deterministic gridded model data to point-based and gridded observations. It also provides ensemble and probabilistic verification methods for comparing gridded model data to point-based or gridded observations. Verification tasks to accomplish these comparisons are defined in the MRW App in :numref:`Table %s <VXWorkflowTasksTable>`. Currently, the MRW App supports the use of :term:`NDAS` observation files in `prepBUFR format <https://nomads.ncep.noaa.gov/pub/data/nccf/com/nam/prod/>`__ (which include conventional point-based surface and upper-air data) for point-based verification. It also supports gridded Climatology-Calibrated Precipitation Analysis (:term:`CCPA`) data for accumulated precipitation evaluation and Multi-Radar/Multi-Sensor (:term:`MRMS`) gridded analysis data for composite reflectivity and :term:`echo top` verification. 

..
   COMMENT: Add the WorkflowTasksTable to MRW Docs!!!

METplus is being actively developed by :term:`NCAR`/Research Applications Laboratory (RAL), NOAA/Earth Systems Research Laboratories (ESRL), and NOAA/Environmental Modeling Center (EMC), and it is open to community contributions.

=========================
Visualization Example
=========================

This release does not include support for model visualization. Currently, only four basic NCAR Command Language (:term:`NCL`) scripts are provided to create a basic visualization of model output. This capability is provided only as an example for users familiar with NCL, and may be used to do a visual check to verify that the application is producing reasonable results.

The scripts are available in the FTP site ftp://ftp.emc.ncep.noaa.gov/EIB/UFS/visualization_example/.
File visualization_README describes the plotting scripts. Example plots are provided
for the C96 5-day forecasts initialized on 8/29/2019 00 UTC using :term:`GRIB2`,  :term:`NEMSIO`, or :term:`netCDF` files as input datasets.

..
   COMMENT: Is this still true?

===========================
Workflow and Build System
===========================
The MRW App has a user-friendly workflow and a portable build system that
invokes the CMake build software before compiling the code. This release is
supported for use with Linux and Mac operating systems, with Intel and GNU
compilers. There is a small set of system libraries that are assumed to be
present on the target computer, including CMake, a compiler, and the MPI
library that enables parallelism.

..
   COMMENT: Is Linus/Mac still supported? Seems like we're not testing it...

A few select computational platforms have been preconfigured for the release
with all the required libraries for building community releases of
UFS models and applications available in a central place. That means
bundled libraries included in (:term:`spack-stack`) has been built, and the MRW is expected to build and run out of the box. On preconfigured platforms, users can proceed directly to the using the
workflow, as described in the :ref:`Quick Start chapter <quickstart>`.

A few additional computational platforms are considered configurable for the release.
Configurable platforms are platforms where all of the required libraries for
building community releases of UFS models and applications are expected to
install successfully, but are not available in a central place. Applications and
models are expected to build and run once the (:term:`spack-stack`) libraries are built.

Limited-test and Build-Only computational platforms are those in which the developers
have built the code but little or no pre-release testing has been conducted, respectively.
A complete description of the levels of support, along with a list of preconfigured
and configurable platforms can be found `here <https://github.com/ufs-community/ufs-mrweather-app/wiki/Supported-Platforms-and-Compilers-for-MRW-App>`__.

The workflow leverages the Common Infrastructure for Modeling the Earth (:term:`CIME`)
Case Control System (CCS). As described in the `CIME documentation <http://esmci.github.io/cime/versions/ufs_release_v1.1/html/index.html>`__, it comes with two default configurations, or
Component Sets (compsets). One compset is used to evoke the physics :term:`suite`
used in the operational GFS v15, while the other is used to evoke the
experimental GFS v16 physics. Based on the type of initial conditions, the
workflow determines whether or not to employ the variant with simple or more complex
SST. The workflow provides ways to choose the grid resolution, as well as to change namelist options,
such as history file frequency. It also allows for configuration of other
elements of the workflow; for example, whether to run some or all of the
pre-processing, forecast model, and post-processing steps. The CIME builds
the forecast model and the workflow itself, but not the :term:`NCEP` Libraries or the
pre- and post-processing tools.

`CIME`_ supports a set of tests for the MRW App, including the Smoke
Startup Test, the Exact Restart from Startup Test, and the Modified Threading
OPENMP bit for bit Test. These tests are described in more detail later in this
document and are intended for users to verify the App installation in new
platforms and to test the integrity of their code in case
they modify the source code.

===========================================================
User Support, Documentation, and Contributing Development
===========================================================

A `forum-based online support system <https://forums.ufscommunity.org>`__ with topical sections
provides a centralized location for UFS users and
developers to post questions and exchange information. The forum complements
the distributed documentation, summarized here for ease of use.

.. table::  Centralized list of documentation

   +----------------------------+---------------------------------------------------------------------------------+
   | **Documentation**          | **Location**                                                                    |
   +============================+=================================================================================+
   | MRW App v1.1               | https://ufs-mrweather-app.readthedocs.io/en/ufs-v1.1.0                          |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | chgres_cube User's Guide   | https://ufs-utils.readthedocs.io/en/ufs-v1.1.0                                  |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS Weather Model v1.1     | https://ufs-weather-model.readthedocs.io/en/ufs-v1.1.0                          |
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
   | Unified Post Processor     | https://upp.readthedocs.io/en/ufs-v1.1.0                                        |
   +----------------------------+---------------------------------------------------------------------------------+

The UFS community is encouraged to contribute to the UFS development effort.
Issues can be posted in the GitHub repository for the App or the relevant
subcomponent to report bugs or to announce upcoming contributions to the code
base. For a code to be accepted in the authoritative repositories, the code
management rules of each component (described in their User’s Guides) need to be
followed. Innovations involving the UFS Weather Model need to be tested using
the regression test described in its User’s Guide. The regression tests
distributed with the UFS Weather Model differ from the CIME-base tests
distributed with the MRW App because the former are part of the
official NOAA policy to accept innovations in its code base, while the latter
are meant as a sanity check for users.

=================
Future Direction
=================

Users can expect to see incremental capabilities in upcoming releases of the
MRW App to enhance research options and support operational forecast
implementations. Planned advancements include addition of component models for
other Earth domains (such as oceans and sea ice), cycled data assimilation for
model initialization, and tools for objective forecast verification. Releases
of other UFS applications, such as the Stand-Alone Regional (SAR) application
are also forthcoming and will be announced through the UFS Forum and the UFS Portal.

==========================
How To Use This Document
==========================

This User's Guide instructs both novice and experienced users on downloading,
building and running the MRW Application.

If you are a new user, we recommend reading the first few sections of
the `CIME`_ documentation which is written so that, as much as
possible, individual sections stand on their own. The `CIME`_
documentation can be scanned and sections read in a relatively
ad hoc order.

.. code-block:: console

    Throughout the guide, this presentation style indicates shell
    commands and options, fragments of code, namelist variables, etc.

Variables presented as ``AaBbCc123`` in this User's Guide typically refer to variables in scripts, names of files, and directories.

File paths or code that include angle brackets (e.g., ``build_<platform>_<compiler>.env``) indicate that users should insert options appropriate to their MRW App configuration (e.g., ``build_orion_intel.env``).

..
   COMMENT: Change examples to be MRW-specific.

.. note::

   Variables presented as ``$VAR`` in this guide typically refer to variables in XML files
   in a MRW App experiment. From within a case directory, you can determine the value of such a
   variable with ``./xmlquery VAR``. In some instances, ``$VAR`` refers to a shell
   variable or some other variable; we try to make these exceptions clear.

.. _CIME: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/index.html
