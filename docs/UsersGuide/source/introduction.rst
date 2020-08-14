.. _introduction:

============
Introduction
============

The Unified Forecast System (:term:`UFS`) is a community-based, coupled, comprehensive
Earth modeling system with applications that span local to global domains and
predictive time scales. It is designed to be the source system for NOAA’s
operational numerical weather prediction applications while enabling both
research and capabilities for the broader weather enterprise. For more
information about the UFS, visit the UFS Portal at https://ufscommunity.org/.

The Unified Forecast System (:term:`UFS`) can be configured into multiple applications
(see a complete list at https://ufscommunity.org/#/science/aboutapps).
The first of these to be released to the community is the UFS Medium-Range
(MR) Weather Application (App), which targets predictions of atmospheric
behavior out to about two weeks. The MR Weather App v1.1 includes a prognostic
atmospheric model, pre- and post-processing tools, and a community workflow
The release is available on GitHub and is designed to be a code that the
community can run and improve. It is portable to a set of commonly used
platforms. A limited set of configurations of the release, such as specific
model resolutions and physics options, are documented and supported.
This documentation provides an overview of the release components, a
description of the supported capabilities, a quick start for running the
application, and information on where to find more information and obtain
support.

Pre-processor and initial conditions
====================================
The MR Weather App is distributed with the :term:`chgres_cube` pre-processing software.
It converts the Global Forecast System (GFS) analyses to the format needed as
input to the model, which is six tiles in NetCDF format. Additional information
about chgres_cube can be found in the `chgres_cube User’s Guide <https://ufs-utils.readthedocs.io/en/ufs-v1.1.0/>`_.

GFS analyses for initializing the MR Weather App can be in Gridded Binary
v2 (GRIB2) format (in 0.25 , 0.50, or 1.0 degree grid spacing),  the NOAA Environmental
Modeling System (:term:`NEMS`) Input/Output (:term:`NEMSIO`) format, or Network Common Data Formt (:term: `NETCDF`).
Initialization from dates starting on January 1, 2018 are supported. Dates
before that may work, but are not guaranteed. GFS public archives can be
accessed through the National Centers for Environmental Information (NCEI)
`Global Forecast System website <https://www.ncdc.noaa.gov/data-access/model-data/model-datasets/global-forcast-system-gfs>`_
or through the `Thredds Data Server at NCEI <https://www.ncei.noaa.gov/thredds/model/gfs.html>`_. Some NETCDF data can be found at `ftp site <https://ftp.emc.ncep.noaa.gov/EIB/UFS/>`_.
The initial conditions may be pre-staged on disk by the user or
automatically downloaded by the workflow.

Forecast model
==============

The prognostic model in the UFS MR Weather App is the atmospheric component
of the UFS Weather Model, which employs the Finite-Volume Cubed-Sphere (:term:`FV3`)
dynamical core. The atmospheric model in this release is an updated version
of the atmospheric model that is being used in the operational GFS v15.
A User’s Guide for the UFS Weather Model is `here <https://ufs-weather-model.readthedocs.io/en/ufs-v1.1.0>`_.

Supported grid configurations for this release are the global meshes with
resolutions of C96 (~100 km), C192 (~50 km), C384 (~25 km), and C768 (~13 km),
all with 64 vertical levels. The `NOAA Geophysical Fluid Dynamics Laboratory website <https://www.gfdl.noaa.gov/fv3>`_
provides more information about FV3 and its grids. Additional information about the FV3 dynamical
core is at `here <https://noaa-emc.github.io/FV3_Dycore_ufs-v1.0.0/html/index.html>`_.
Interoperable atmospheric physics, along with the Noah land surface model, are
supported through the use of the Common Community Physics Package (:term:`CCPP`;
described `here <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`_.
There are four physics suites supported for the release.
Two of them are variations of an updated version of the physics :term:`suite` used in
the operational GFS v15, while the other two are variations of an experimental
suite that includes a subset of the developments for the next version of GFS,
GFS v16. The variations pertain to how the sea surface temperature (SST) is
initialized and parameterized to evolve, and are chosen depending on the type
of initial conditions for the App. Initial conditions in GRIB2 format have a
single two-dimensional field to initialize the SST, which must be kept constant
throughout the forecast. Initial conditions in :term:`NEMSIO` format have two two-dimensional
fields that describe the baseline SST and its near-surface perturbation related
to the diurnal cycle, enabling the use of the near-sea-surface-temperature (NSST)
physical parameterization to forecast the temporal variation in SST due to the
diurnal cycle.

A scientific description of the CCPP parameterizations and suites can be found in the
`CCPP Scientific Documentation <https://dtcenter.org/GMTB/v4.0/sci_doc>`_, and
CCPP technical aspects are described in the `CCPP Technical Documentation <https://ccpp-techdoc.readthedocs.io/en/latest>`_.
The model namelists for the physics suites differ in ways that go beyond
the physics to optimize various aspects of the model for use with each of the
suites.
The use of :term:`stochastic<Stochastic physics>` processes to represent model uncertainty is an option
in this release, although the option is off by default in both of the
supported physics suites. Three methods are supported for use separately or in
combination: Stochastic Kinetic Energy Backscatter (SKEB), Stochastically
Perturbed Physics Tendencies (SPPT), and Specific Humidity perturbations (SHUM).
A `User’s Guide for the use of stochastic physics <https://stochastic-physics.readthedocs.io/en/ufs-v1.0.0>`_ is provided.

The UFS Weather Model ingests files produced by chgres_cube and outputs files
in NetCDF format on a Gaussian grid in the horizontal and model levels in the
vertical.

Post-processor
================================

The MR Weather App is distributed with a post-processing tools, the Unified
Post Processor (UPP). The Unified Post Processor (UPP) converts the
native NetCDF output from the model to the GRIB2 format on standard isobaric
coordinates in the vertical. The UPP can also be used to compute a variety of
useful diagnostic fields, as described in the `UPP user's guide <https://upp.readthedocs.io/en/ufs-v1.0.0>`_.

The UPP output can be used with visualization, plotting and verification
packages, or for further downstream post-processing, e.g. statistical
post-processing techniques.

Visualization Example
=========================

This release does not include support for model verification or visualization. Currently,
only four basic NCAR Command Language (:term:`NCL`) scripts are provided to create a basic visualization of model output.
This capability is provided only as an example for users familiar with NCL, and may be used to
do a visual check to verify that the application is
producing reasonable results.

The scripts are available in the ftp site ftp://ftp.emc.ncep.noaa.gov/EIB/UFS/visualization_example/.
File visualization_README describes the plotting scripts. Example plots are provided
for the C96 5-day forecasts initialized on 8/29/2019 00 UTC using GRIB2 and NEMSIO
files as input datasets.

Workflow and Build System
=========================
The MR Weather App has a user-friendly workflow and a portable build system that
invokes the CMake build software before compiling the codes. This release is
supported for use with Linux and Mac operating systems, with Intel and GNU
compilers. There is a small set of system libraries that are assumed to be
present on the target computer, including CMake, a compiler, and the MPI
library that enables parallelism.

A few select computational platforms have been preconfigured for the release
with all the required libraries for building community releases of
UFS models and applications available in a central place. That means
bundled libraries (:term:`NCEPLIBS`) and third-party libraries (:term:`NCEPLIBS-external`),
including the Earth System Modeling Framework (ESMF)
have both been built. Applications and models are expected to build and run out of the box.
In preconfigured platforms, users can proceed directly to the using the
workflow, as described in the :ref:`Quick Start chapter <quickstart>`.

A few additional computational platforms are considered configurable for the release.
Configurable platforms are platforms where all of the required libraries for
building community releases of UFS models and applications are expected to
install successfully, but are not available in a central place. Applications and
models are expected to build and run once the required bundled libraries
(:term:`NCEPLIBS`) and third-party libraries (:term:`NCEPLIBS-external`) are built.

Limited-test and Build-Only computational platforms are those in which the developers
have built the code but little or no
pre-release testing has been conducted, respectively.
A complete description of the levels of support, along with a list of preconfigured
and configurable platforms can be found `here <https://github.com/ufs-community/ufs/wiki/Supported-Platforms-and-Compilers>`_.

The workflow leverages the Common Infrastructure for Modeling the Earth (:term:`CIME`)
Case Control System (CCS). As described in the `CIME documentation <http://esmci.github.io/cime/versions/ufs_release_v1.1/html/index.html>`_,
it comes with two default configurations, or
Component Sets (compsets). One compset is used to evoke the physics :term:`suite`
used in the operational GFS v15, while the other is used to evoke the
experimental GFS v16 physics. Based on the type of initial conditions, the
workflow determines whether the to employ the variant with simple or more complex 
SST. The workflow provides
ways to choose the grid resolution, as well as to change namelist options,
such as history file frequency. It also allows for configuration of other
elements of the workflow; for example, whether to run some or all of the
pre-processing, forecast model, and post-processing steps. The CIME builds
the forecast model and the workflow itself, but not the :term:`NCEP` Libraries or the
pre- and post-processing tools.

`CIME`_ supports a set of tests for the UFS MR Weather App, including the Smoke
Startup Test, the Exact Restart from Startup Test, and the Modified Threading
OPENMP bit for bit Test. These tests are described in more detail later in this
document and are intended for users to verify the App installation in new
platforms and to test the integrity of their code in case
they modify the source code.

User Support, Documentation, and Contributing Development
=========================================================
A `forum-based online support system <https://forums.ufscommunity.org>`_ with topical sections
provides a centralized location for UFS users and
developers to post questions and exchange information. The forum complements
the distributed documentation, summarized here for ease of use.

.. table::  Centralized list of documentation

   +----------------------------+---------------------------------------------------------------------------------+
   | **Documentation**          | **Location**                                                                    |
   +============================+=================================================================================+
   | UFS MR Weather App v1.1    | https://ufs-mrweather-app.readthedocs.io/en/ufs-v1.1.0                          |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | chgres_cube User's Guide   | https://ufs-utils.readthedocs.io/en/ufs-v1.1.0                                  |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS Weather Model v1.1     | https://ufs-weather-model.readthedocs.io/en/ufs-v1.1.0                          |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | FV3 Documentation          | https://noaa-emc.github.io/FV3_Dycore_ufs-v1.0.0/html/index.html                |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Scientific            | https://dtcenter.org/GMTB/v4.0/sci_doc                                          |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Technical             | https://ccpp-techdoc.readthedocs.io/en/v4.0                                     |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Stochastic Physics         | https://stochastic-physics.readthedocs.io/en/ufs-v1.0.0                         |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | ESMF manual                | http://www.earthsystemmodeling.org/esmf_releases/public/ESMF_8_0_0/ESMF_refdoc  |
   +----------------------------+---------------------------------------------------------------------------------+
   | Common Infrastructure for  | http://esmci.github.io/cime/versions/ufs_release_v1.0/html/index.html           |
   | Modeling the Earth         |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Unified Post Processor     | https://upp.readthedocs.io/en/ufs-v1.0.0                                        |
   +----------------------------+---------------------------------------------------------------------------------+

The UFS community is encouraged to contribute to the UFS development effort.
Issues can be posted in the GitHub repository for the App or the relevant
subcomponent to report bugs or to announce upcoming contributions to the code
base. For a code to be accepted in the authoritative repositories, the code
management rules of each component (described in their User’s Guides) need to be
followed. Innovations involving the UFS Weather Model need to be tested using
the regression test described in its User’s Guide. The regression tests
distributed with the UFS Weather Model differ from the CIME-base tests
distributed with the UFS MR Weather App because the former are part of the
official NOAA policy to accept innovations in its code base, while the latter
are meant as a sanity check for users.

Future Direction
================
Users can expect to see incremental capabilities in upcoming releases of the
UFS MR Weather App to enhance research options and support operational forecast
implementations. Planned advancements include addition of component models for
other Earth domains (such as oceans and sea ice), cycled data assimilation for
model initialization, and tools for objective forecast verification. Releases
of other UFS applications, such as the Stand-Alone Regional (SAR) application
are also forthcoming and will be announced through the UFS Forum and the UFS
Portal.

How To Use This Document
========================

This guide instructs both novice and experienced users on downloading,
building and running the MR Weather Application.

If you are a new user, we recommend reading the first few sections of
the `CIME`_ documentation which is written so that, as much as
possible, individual sections stand on their own and the `CIME`_
documentation guide can be scanned and sections read in a relatively
ad hoc order.

.. code-block:: console

    Throughout the guide, this presentation style indicates shell
    commands and options, fragments of code, namelist variables, etc.

.. note::

   Variables presented as ``$VAR`` in this guide typically refer to variables in XML files
   in a UFS MR Weather App experimental case. From within a case directory, you can determine the value of such a
   variable with ``./xmlquery VAR``. In some instances, ``$VAR`` refers to a shell
   variable or some other variable; we try to make these exceptions clear.

.. _CIME: http://esmci.github.io/cime/versions/ufs_release_v1.1/html/index.html
