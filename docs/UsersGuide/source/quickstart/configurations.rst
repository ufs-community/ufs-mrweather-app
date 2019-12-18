.. _configurations:

======================
Model Configurations
======================

The mrweather app currently can be configured at four out of the box resolutions
and one preprocessed initial conditions for each resolution.


Supported component sets
----------------------------

   .. todo:: Define what a compset is for the UFS

To determine what out of the box MR Weather Application compsets are available in the release, do
the following:
::

      > cd $SRCROOT/cime/scripts
      > ./query_config --compsets


Supported grids
---------------

The MR Weather Application currently supports four out of the box grids.

* C96 (~100km)
* C192 (~50km),
* C384 (~25km)
* C768 (~13km),

all with 64 vertical levels.CIME supports numerous out-of-the box model resolutions. To see the
grids that are supported, call `query_config <../Tools_user/query_config.html>`_ as shown below.
::

      > cd $SRCROOT/cime/scripts
      > ./query_config --grids


Supported platforms and compilers
---------------------------------

To see the list of supported out of the box platforms, issue the following commands:
::

      > cd $SRCROOT/cime/scripts
      > ./query_config --machines


Supported machines have machine specific files and settings
scripts and are machines that should run MR Weather Application cases
out-of-the-box. Machines are supported on an individual basis
and are usually listed by their common site-specific name. To add a new
machine local batch, run, environment, and compiler information must be configured
added in the $SRCROOT/cime/config/ufs/machines directory.
The machine name "userdefined" machines refer to any machine
that the user defines and requires that a user edit the resulting xml
files to fill in information required for the target platform. This
functionality is handy in accelerating the porting process and quickly
getting a case running on a new platform. For more information on
porting, see the `CIME porting guide
<http://esmci.github.io/cime/users_guide/porting-cime.html>`_.


Validating your port
--------------------

Although the MR Weather Application can be run out-of-the-box for a variety of resolutions,
component combinations, and machines, MOST combinations of component
sets, resolutions, and machines have not undergone rigorous scientific validation.

  .. todo:: Define the port validation process
