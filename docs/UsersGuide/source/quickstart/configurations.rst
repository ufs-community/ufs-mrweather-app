.. _configurations:

======================
Model Configurations
======================

The mrweather app currently can be configured at four out of the box resolutions
and one preprocessed initial conditions for each resolution.


supported component sets
----------------------------

Describe component sets here. Running **query_config**
with the ``--compsets`` option will also provide a listing of the
supported out-of-the-box component sets for the local version of CESM.


supported grids
---------------

The mrweather app currently supports four out of the box grids. Give description.
grid with three poles that are all centered over land.
Describe how you will query the grid.


supported platforms and compilers
---------------------------------

Scripts for `supported machines
<http://www.cesm.ucar.edu/models/cesm2/cesm/machines.html>`_ and
userdefined machines are provided with the CESM release. Supported
machines have machine specific files and settings added to the CESM
scripts and are machines that should run CESM cases
out-of-the-box. Machines are supported in CESM on an individual basis
and are usually listed by their common site-specific name. To get a
machine ported and functionally supported in CESM, local batch, run,
environment, and compiler information must be configured in the CESM
scripts. The machine name "userdefined" machines refer to any machine
that the user defines and requires that a user edit the resulting xml
files to fill in information required for the target platform. This
functionality is handy in accelerating the porting process and quickly
getting a case running on a new platform. For more information on
porting, see the `CIME porting guide
<http://esmci.github.io/cime/users_guide/porting-cime.html>`_.  The
list of available machines are documented in `CESM supported machines
<http://www.cesm.ucar.edu/models/cesm2/cesm/machines.html>`_.
Running **query_config** with the ``--machines`` option will also show
the list of all machines for the current local version of
CESM. Supported machines have undergone the full CESM porting
process. The machines available in each of these categories changes as
access to machines change over time.


validation
----------

Although CESM can be run out-of-the-box for a variety of resolutions,
component combinations, and machines, MOST combinations of component
sets, resolutions, and machines have not undergone rigorous scientific
climate validation. Control runs accompany `scientifically supported
<http://www.cesm.ucar.edu/models/scientifically-supported.html>`_
component sets and resolutions and are documented on the release page.
These control runs should be scientifically reproducible on the
original platform or other platforms. Bit-for-bit reproducibility
cannot be guaranteed due to variations in compiler or system
versions. Users should carry out their own `port validations
<http://esmci.github.io/cime/users_guide/porting-cime.html#validating-your-port>`_
on any platform prior to doing scientific runs or scientific analysis
and documentation.
