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
behavior out to about two weeks. The MR Weather App v1.0 includes a prognostic
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
about chgres_cube can be found in the chgres_cube User’s Guide (under
development).

GFS analyses for initializing the MR Weather App can be in Gridded Binary
v2 (GRIB2) format (in 25o, 0.50, or 1.0o grid spacing) or in the NOAA Environmental
Modeling System (:term:`NEMS`) Input/Output (:term:`NEMSIO`) format.
Initialization from dates starting on January 1, 2018 are supported. Dates
before that may work, but are not guaranteed. GFS public archives can be
accessed through the NOAA National Center for Environmental Information (NCEI)
at https://www.ncdc.noaa.gov/data-access and through the NOAA Operational Model Archive and
Distribution System (NOMADS) at https://nomads.ncdc.noaa.gov/data/gfs4.
The initial conditions may be pre-staged on disk by the user or
automatically downloaded by the workflow.

Forecast model
==============

The prognostic model in the UFS MR Weather App is the atmospheric component
of the UFS Weather Model, which employs the Finite-Volume Cubed-Sphere (:term:`FV3`)
dynamical core. The atmospheric model in this release is an updated version
of the atmospheric model that is being used in the operational GFS v15.
A User’s Guide for the UFS Weather Model is here:
https://ufs-weather-model.readthedocs.io/en/release-public-v1/

Supported grid configurations for this release are the global meshes with
resolutions of C96 (~100km), C192 (~50km), C384 (~25km), and C768 (~13km),
all with 64 vertical levels. The Geophysical Fluid Dynamics Laboratory website
provides more information about FV3 and its grids here:
https://www.gfdl.noaa.gov/fv3.  Additional information about the FV3 dynamical
core is at https://noaa-emc.github.io/FV3_Dycore_v1.0/html/index.html.
Interoperable atmospheric physics, along with the Noah land surface model, are
supported through the use of the Common Community Physics Package (:term:`CCPP`;
described at https://dtcenter.org/community-code/common-community-physics-package-ccpp).
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

A scientific description of the parameterization and suites can be found at
https://dtcenter.org/GMTB/v4.0/sci_doc/, and technical documentation about the
:term:`CCPP` is at https://ccpp-techdoc.readthedocs.io/en/latest.
The model namelists for the physics suites differ in ways that go beyond
the physics to optimize various aspects of the model for use with each of the
suites.
The use of :term:`stochastic<Stochastic physics>` processes to represent model uncertainty is an option
in this release, although the option is off by default in both of the
supported physics suites. Three methods are supported for use separately or in
combination: Stochastic Kinetic Energy Backscatter (SKEB), Stochastically
Perturbed Physics Tendencies (SPPT), and Specific Humidity perturbations (SHUM).
A User’s Guide for the use of stochastic physics is at https://stochastic-physics.readthedocs.io/en/latest.
The UFS Weather Model ingests files produced by chgres_cube and outputs files
in NetCDF format on a Gaussian grid in the horizontal and model levels in the
vertical.

Post-processor
================================

The MR Weather App is distributed with two post-processing tools, the Unified
Post Processor (UPP) and wgrib2. The Unified Post Processor (UPP) converts the
native NetCDF output from the model to the GRIB2 format on standard isobaric
coordinates in the vertical. The UPP can also be used to compute a variety of
useful diagnostic fields. 

The wgrib2 utility can be used to perform horizontal interpolation
onto a regular latitude-longitude grid for these GRIB2 files.

These output formats can be used with visualization, plotting and verification
packages, or for further downstream post-processing, e.g. statistical
post-processing techniques. More information about UPP can be found here
https://upp.readthedocs.io/en/latest/
and the wgrib2 utility is described at
https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/.

Visualization Example
=========================

This release does not include support for model verification or visualization. Currently, 
only a basic NCL script is provided to create a basic visualization of model output.  
This is provided only as an example for users familiar with :term:`NCL`, and may be used to
do a visual check to verify that the application is set up correctly and
producing reasonable results.

ftp://ftp.emc.ncep.noaa.gov/EIB/UFS/visualization_example/

contains a README file describing the plotting scripts and example plots.

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
bundled libraries (:term:`NCEPLIBS`) and third-party libraries (:term:`NCEPLIBS-external`)
have both been built. Applications and models are expected to build and run out of the box.
In preconfigured platforms, users can proceed directly to the using the `CIME`_
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
and configurable platforms can be found at
https://github.com/ufs-community/ufs/wiki/Supported-Platforms-and-Compilers.

The workflow leverages the Common Infrastructure for Modeling the Earth (:term:`CIME`)
Case Control System (CCS). CIME comes with two default configurations, or
Component Sets (compsets). One compset is used to evoke the physics :term:`suite`
used in the operational GFS v15, while the other is used to evoke the
experimental GFS v16 physics. Based on the type of initial conditions, the
workflow determines whether the to employ the variant with constant or predicted
SST. The workflow provides
ways to choose the grid resolution, as well as to change namelist options,
such as history file frequency. It also allows for configuration of other
elements of the workflow; for example, whether to run some or all of the
pre-processing, forecast model, and post-processing steps. The CIME-CCS builds
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
A forum-based online support system with topical sections
(forums.ufscommunity.org) provides a centralized location for UFS users and
developers to post questions and exchange information. The forum complements
the distributed documentation, summarized here for ease of use.

.. table::  Centralized list of documentation

   +----------------------------+---------------------------------------------------------------------------------+
   | **Documentation**          | **Location**                                                                    |
   +============================+=================================================================================+
   | UFS MR Weather App v1.0    | https://ufs-mrweather-app.readthedocs.io/en/latest/                             |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | chgres_cube User's Guide   | https://prototype-chgres-cube.readthedocs.io/en/latest/                         |
   +----------------------------+---------------------------------------------------------------------------------+
   | UFS Weather Model v1.0     | https://ufs-weather-model.readthedocs.io/en/release-public-v1                   |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | FV3 Documentation          | https://noaa-emc.github.io/FV3_Dycore_v1.0/html/index.html                      |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Scientific            | https://dtcenter.org/GMTB/UFS/sci_doc/                                          |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | CCPP Technical             | https://ccpp-techdoc.readthedocs.io/en/latest/                                  |
   | Documentation              |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Stochastic Physics         | https://stochastic-physics.readthedocs.io/en/ufs_public_release/                |
   | User's Guide               |                                                                                 |
   +----------------------------+---------------------------------------------------------------------------------+
   | Unified Post Processor     | https://upp.readthedocs.io/en/latest/                                           |
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
   in a MR Weather experimental case. From within a case directory, you can determine the value of such a
   variable with ``./xmlquery VAR``. In some instances, ``$VAR`` refers to a shell
   variable or some other variable; we try to make these exceptions clear.

.. _CIME: http://esmci.github.io/cime/#
