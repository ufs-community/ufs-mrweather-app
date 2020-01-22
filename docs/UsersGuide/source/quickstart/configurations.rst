.. _configurations:

======================
Model Configurations
======================

The UFS Medium-Range (MR) Weather Application can be configured at four out of the box resolutions
with two different Common Community Physics Package (`CCPP 
<https://ccpp-techdoc.readthedocs.io/en/latest/Overview.html>`_) physics suites (``GFSv15p2`` or ``GFSv16beta``).

Supported component sets
========================

The components of the modeling system can be combined in numerous ways to carry out various scientific or
software experiments. A particular mix of components, along with component-specific configuration and/or
namelist settings is called a component set or "compset". The UFS Medium-Range (MR) Weather Application 
has a shorthand naming convention for component sets that are supported out-of-the-box.

To determine what out of the box MR Weather Application compsets are available in the release, do
the following:

.. code-block:: console

    cd $SRCROOT/cime/scripts
    ./query_config --compsets

This should show a list of available compsets, as following:

.. code-block:: console

    Active component: ufsatm
           --------------------------------------
           Compset Alias: Compset Long Name 
           --------------------------------------
       GFSv15p2             : FCST_ufsatm%v15p2_SLND_SICE_SOCN_SROF_SGLC_SWAV
       GFSv16beta           : FCST_ufsatm%v16beta_SLND_SICE_SOCN_SROF_SGLC_SWAV

Supported grids
===============

The application currently supports four out of the box grids.

* C96 (~100km)
* C192 (~50km),
* C384 (~25km)
* C768 (~13km),

all with 64 vertical levels.CIME supports numerous out-of-the box model resolutions. To see the
grids that are supported, call you could call following command

.. code-block:: console

    cd $SRCROOT/cime/scripts
    ./query_config --grids

Supported platforms and compilers
=================================

To see the list of supported out of the box platforms, issue the following commands:

.. code-block:: console

    cd $SRCROOT/cime/scripts
    ./query_config --machines

Supported machines have machine specific files and settings scripts and are machines that should
run UFS Medium-Range (MR) Weather Application out-of-the-box (might need to download input files). 
Machines are supported on an individual basis and are usually listed by their common site-specific name.
To add a new machine local batch, run, environment, and compiler information must be configured
added in the $SRCROOT/cime/config/ufs/machines directory.

The machine name "userdefined" machines refer to any machine that the user defines and requires 
that a user edit the resulting xml files to fill in information required for the target platform. This
functionality is handy in accelerating the porting process and quickly
getting a case running on a new platform. For more information on porting, see the `CIME porting guide
<http://esmci.github.io/cime/users_guide/porting-cime.html>`_.

Validating your port
====================

Although the MR Weather Application can be run out-of-the-box for a variety of resolutions,
component combinations, and machines, MOST combinations of component
sets, resolutions, and machines have not undergone rigorous scientific validation.

  .. todo:: Define the port validation process
