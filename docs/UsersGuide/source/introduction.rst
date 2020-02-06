.. _introduction:

============
Introduction
============

The Unified Forecast System (UFS) is a community-based, coupled, comprehensive
Earth modeling system with applications that span local to global domains and
predictive time scales. It is designed to be the source system for NOAA’s
operational numerical weather prediction applications while enabling both
research and capabilities for the broader weather enterprise. For more
information about the UFS, visit the UFS Portal at https://ufscommunity.org/.

The Unified Forecast System (UFS) can be configured into multiple applications
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
The MR Weather App is distributed with the chgres_cube pre-processing software.
It converts the Global Forecast System (GFS) analyses to the format needed as
input to the model, which is six tiles in NetCDF format. Additional information
about chgres_cube can be found in the chgres_cube User’s Guide (under
development).

GFS analyses for initializing the MR Weather App can be in Gridded Binary v1
(GRIB1) or v2 (GRIB2) format, and can be in 25o, 0.50, or 1.0o grid spacing.
Initialization from dates starting on January 1, 2018 are supported. Dates
before that may work, but are not guaranteed. GFS public archives can be
accessible through the NOAA National Center for Environmental Information (NCEI)
at https://www.ncdc.noaa.gov/data-access. The NOAA Operational Model Archive and
Distribution System (NOMADS) offers 0.5o GRIB2 datasets dating back to January
1, 2019, while older datasets can be requested  from the NCDC archives at
https://www.ncdc.noaa.gov/has/HAS.FileAppRouter?datasetname=GFSGRB24&subqueryby=STATION&applname=&outdest=FILE.

The ICs may be pre-staged on disk by the user. Alternatively, the ICs may be
automatically downloaded by the workflow from the NOMADS data server if
available for the date specified.

Forecast model
==============

The prognostic model in the UFS MR Weather App is the atmospheric component
of the UFS Weather Model, which employs the Finite-Volume Cubed-Sphere (FV3)
dynamical core. The atmospheric model in this release is an updated version
of the atmospheric model that is being used in the operational GFS v15.
A User’s Guide for the UFS Weather Model is here:
https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/.

Supported grid configurations for this release are the global meshes with
resolutions of C96 (~100km), C192 (~50km), C384 (~25km), and C768 (~13km),
all with 64 vertical levels. The Geophysical Fluid Dynamics Laboratory website
provides more information about FV3 and its grids here:
https://www.gfdl.noaa.gov/fv3.  Additional information about the FV3 dynamical
core is at https://noaa-emc.github.io/FV3_Dycore/html/.
Interoperable atmospheric physics, along with the Noah land surface model, are
supported through the use of the Common Community Physics Package (CCPP;
described at https://dtcenter.org/community-code/common-community-physics-package-ccpp). There are two physics suites supported for the release. The first is an updated version of the physics suite used in the operational GFS v15, and the second is an experimental suite that includes a subset of the developments for the next version of GFS, GFS v16. A scientific description of the parameterization and suites can be found at https://dtcenter.org/GMTB/v4.0/sci_doc/, and technical documentation about the CCPP is at https://readthedocs.org/projects/ccpp-techdoc/.
The model namelists for the two physics suites differ in ways that go beyond
the physics to optimize various aspects of the model for use with each of the
suites.
The use of stochastic processes to represent model uncertainty is an option
in this release, although the option is off by default in both of the
supported physics suites. Three methods are supported for use separately or in
combination: Stochastic Kinetic Energy Backscatter (SKEB), Stochastically
Perturbed Physics Tendencies (SPPT), and Specific Humidity perturbations (SHUM). A User’s Guide for the use of stochastic physics is at https://stochastic-physics.readthedocs.io/en/latest.
The UFS Weather Model ingests files produced by chgres_cube and outputs files
in NetCDF format on a Gaussian grid in the horizontal and model levels in the
vertical.

Post-processor and visualization
================================

The MR Weather App is distributed with two post-processing tools, the Unified
Post Processor (UPP) and wgrib2. The Unified Post Processor (UPP) converts the
native NetCDF output from the model to the GRIB2 format on standard isobaric
coordinates in the vertical. The UPP can also be used to compute a variety of
useful diagnostic fields. The wgrib2 utility performs horizontal interpolation
onto a regular latitude-longitude grid for these GRIB2 files.

These output formats can be used with visualization, plotting and verification
packages, or for further downstream post-processing, e.g. statistical
post-processing techniques. More information about UPP can be found here and
the wgrib utility is described at
https://www.cpc.ncep.noaa.gov/products/wesley/wgrib2/.

Verification and Examples
=========================

A comprehensive example is provided, including output data sets. It is possible
to do a visual check to verify that the application is set up correctly and
producing correct results.

Workflow and Build System
=========================
The MR Weather App has a user-friendly workflow and a portable build system that
invokes the CMake build software before compiling the codes. This release is
supported for use with Linux and Mac operating systems, with Intel and GNU
compilers. There is a small set of system libraries that are assumed to be
present on the target computer, including CMake, a compiler, and the MPI
library that enables parallelism.

A few select computational platforms have been preconfigured for the release,
meaning that the NCEP Libraries, along with the pre- and post-processing tools,
have been built by the App developers and are available as modules. In
preconfigured platforms, users can proceed directly to the using the `CIME`_ 
workflow, as described in the Quick Start chapter. In platforms that have not
been preconfigured, users have to build the NCEP Libraries and pre- and
post-processing tools first. Examples of preconfigured platforms are the NOAA
research Hera system, the National Center for Atmospheric Research (NCAR)
Cheyenne system, and the National Science Foundation Stampede2 system.

CONSIDER MOVING THIS ELSEWHERE
See the :ref:`platforms`, :ref:`supported-compsets`, and
:ref:`supported-grids` for currently supported platforms, model
configurations and resolutions.

The workflow leverages the Common Infrastructure for Modeling the Earth (CIME)
Case Control System (CCS). CIME comes with two default configurations, or
Component Sets (CompSets), associated with the two physics suites. It provides
ways to choose the grid resolution, as well as to change namelist options,
such as history file frequency. It also allows for configuration of other
elements of the workflow; for example, whether to run some or all of the
pre-processing, forecast model, and post-processing steps. The CIME-CCS builds
the forecast model and the workflow itself, but not the NCEP Libraries or the
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

Centralized list of documentation
UFS MR Weather App v1.0 User’s Guide: https://ufs-mrapp.readthedocs.io/en/latest/
chgres_cube User's Guide
UFS Weather Model v1.0 User’s Guide: https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/
FV3 Documentation
CCPP Scientific Documentation
CCPP Technical Documentation: https://ccpp-techdoc.readthedocs.io/en/latest/
Stochastic Physics User’s Guide: https://stochastic-physics.readthedocs.io/en/ufs_public_release/
UPP User’s Guide

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
