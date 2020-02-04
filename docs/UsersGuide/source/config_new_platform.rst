.. _config_new_platform:

==========================
Configuring a new platform
==========================

Software/Operating System Prerequisites
---------------------------------------

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

Software stack requirements
---------------------------

Add details of software stack requirements (compiler vendor, versions, etc.)

Everything one needs to do to configure a platform
--------------------------------------------------

Porting CIME to a new machine
-----------------------------

To add a new machine local batch, run, environment, and compiler information must be added
in the CIME directly ``$SRCROOT/cime/config/ufs/machines directory``.

Detailed information on porting can be found in the `CIME porting guide
<http://esmci.github.io/cime/users_guide/porting-cime.html>`_.

The machine name "userdefined" refers to any machine that the user defines and requires
that a user edit the resulting xml files to fill in information required for the target platform. This
functionality is handy in accelerating the porting process and quickly
getting a case running on a new platform.
