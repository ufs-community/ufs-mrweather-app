.. _overview:

============
Overview
============

What is the UFS Medium-Range Weather Application
================================================

The Unified Forecast System (UFS) can be configured into multiple
applications. The first of these to be released to the community is
the UFS Medium-Range (MR) Weather Application, which targets
predictions of atmospheric behavior out to about two weeks.  The MR
Weather Application 1.0 includes a prognostic atmospheric model, pre-
and post-processing, and a community workflow, but does not include
data assimilation.

The release is available on `GitHub <https://github.com/ufs-community/ufs-mrweather-app/>`__
and is designed to be a code that the research community can
run and improve. It is portable to a set of commonly used
platforms. Specific configurations of the release (e.g. specific model
resolutions and physics options) are documented and supported.

More information about the UFS Medium-Range Weather Model can be found
in `here <https://ufs-mr-weather-app.readthedocs.io/projects/ufs-weather-model/en/latest/>`_.

Workflow and Build System
=========================

The MR Weather Application has a user-friendly workflow and a portable
build system.  The workflow leverages the Common Infrastructure for
Modeling Earth (CIME) Case Control System (CCS) `CIME framework
<http://github.com/ESMCI/cime>`_. This established community workflow
is familiar to many through its use in the Community Earth System
Model (CESM). CIME generates a default namelist for the atmospheric
model and provides a way to change namelist options, such as history
file frequency. It also allows for configuration of other elements of
the workflow; for example, whether to run some or all of the
pre-processing, forecast model, and post-processing steps.

In this release, the CIME-CCS only builds the forecast model using
pre-existing `NCEPLIBS <https://github.com/NOAA-EMC/NCEPLIBS/tree/ufs_release_v1.0>`_ package
that includes the prerequisite libraries for the application, along with pre-
and post-processing softwares. There is a small set of system libraries
that are assumed to be present on the target computer: the cmake build
software, compiler, and MPI library.

The MR Weather Application can be run on both Linux and Mac operating systems with
Intel and GNU compilers. The application can be run out of the box on a number of 
different hardware platforms such as the National Oceanic and Atmospheric Administration (NOAA)
research `HERA <https://www.dev.noaa.gov/organization/information-technology/hera>`_, 
the National Center for Atmospheric Research (NCAR) `Cheyenne 
<https://www2.cisl.ucar.edu/resources/computational-systems/cheyenne>`_, 
Texas Advanced Computing Center (TACC), The University of Texas at Austin `Stampede 
<https://www.tacc.utexas.edu/systems/stampede>`_ systems, Mac and Linux laptops and desktops.

See the `supported component sets <https://ufs-mrapp.readthedocs.io/en/latest/quickstart/configurations.html#supported-component-sets>`_,
`supported model resolutions <https://ufs-mrapp.readthedocs.io/en/latest/quickstart/configurations.html#supported-grids>`_ and `supported
machines <https://ufs-mrapp.readthedocs.io/en/latest/quickstart/configurations.html#supported-platforms-and-compilers>`_ for a complete
list of UFS Medium-Range Weather Application supported component sets, grids and computational platforms.

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

Software/Operating System Prerequisites
---------------------------------------------

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

-  `CMake 2.8.6 or newer <http://www.cmake.org/>`_

.. _CIME: http://esmci.github.io/cime
