.. _introduction:

============
Overview
============

What is the UFS Medium-Range Weather Application
------------------------------------------------------------

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

The prognostic model in the UFS MR Weather Application is the UFS
global atmosphere with the Finite Volume Cubed Sphere (FV3) dynamical
core. The dynamical core is the computational part of a model that
solves the equations of fluid motion. The version of the atmospheric
model in this release is an updated version of the same atmospheric
model that is being used in the operational Global Forecast System v15
(GFSv15). Interoperable atmospheric physics are supported through the
use of the Common Community Physics Package (CCPP). There are two
physics options supported for the release. The first is the physics
suite used in the operational GFS v15, and the second is an
experimental suite that includes the latest developments for the next
version of GFS, GFS v16.

There are four supported model resolutions that accompany the release:

* C96 (~100km)
* C192 (~50km),
* C384 (~25km)
* C768 (~13km),

all with 64 vertical levels.  The Geophysical Fluid Dynamics
Laboratory website provides more information about FV3 grids.


Workflow and Build System
------------------------------------------------------------

The MR Weather Application has a user-friendly workflow and a portable
build system.  The workflow leverages the Common Infrastructure for
Modeling Earth (CIME) Case Control System (CCS) `CIME framework
<http://github.com/ESMCI/cime>`_. This established community workflow
is familiar to many through its use in the Community Earth System
Model (CESM). CIME generates a default namelist for the atmospheric
model and provides a way to change namelist options, such as history
file frequency. It also allows for configuration of other elements of
the workflow; for example, whether to run some orf all of the
pre-processing, forecast model, and post-processing steps.

The CIME-CCS builds the forecast model and the workflow itself. There
is unified scripting available through the NCEPLIBS repository that
builds the prerequisite libraries for the application, along with pre-
and post-processing software. There is a small set of system libraries
that are assumed to be present on the target computer: the cmake build
software, compiler, and MPI library.

This release can be run with Linux and Mac operating systems with
Intel and GNU compilers.  The MR Weather Application can be run out of
the box on a number of different hardware platforms such as the NOAA
research Hera system, the National Center for Atmospheric Research
(NCAR) Cheyenne system, the National Science Foundation Stampede
system, and Mac laptops.

.. note::
   list hardware platforms and compilers

How To Use This Document
------------------------

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

Please feel free to provide feedback to the

`CESM forum <https://bb.cgd.ucar.edu/>`_ about how to improve the
documentation.


Software/Operating System Prerequisites
---------------------------------------------

The following are the external system and software requirements for
installing and running CESM2.

-  UNIX style operating system such as CNL, AIX or Linux

-  python >= 2.7

-  perl 5

-  subversion client (version 1.8 or greater but less than v1.11) for downloading CAM, POP, and WW3

-  git client (1.8 or greater)

-  Fortran compiler with support for Fortran 2003

-  C compiler

-  MPI (although CESM does not absolutely require it for running on one processor)

-  `NetCDF 4.3 or newer <http://www.unidata.ucar.edu/software/netcdf/>`_.

-  `ESMF 5.2.0 or newer (optional) <http://www.earthsystemmodeling.org/>`_.

-  `pnetcdf 1.7.0 is required and 1.8.1 is optional but recommended <http://trac.mcs.anl.gov/projects/parallel-netcdf/>`_

-  `Trilinos <http://trilinos.gov/>`_ may be required for certain configurations

-  `LAPACK <http://www.netlib.org/lapack/>`_ and `BLAS <http://www.netlib.org/blas/>`_

-  `CMake 2.8.6 or newer <http://www.cmake.org/>`_

.. _CIME: http://esmci.github.io/cime
