.. _repos_and_directories:

=========================================
Code repositories and directory structure
=========================================

This chapter describes the code repositories that comprise the MR Weather App,
without describing, in detail, any of the components.


Directory Structure
-------------------

The directory structure on disk for users of the MR Weather App depends on whether one is using
a pre-configured platform. Users working on pre-configured platforms will only have the
files associated with the ufs-mrweather-app in their disk space. The directory structure is set
in configuration file ``Externals.cfg``, which is in the top directory where the umbrella repository
has been cloned. 

The directory structures for the standalone UFS Weather Model and the UFS Weather Model included with
the MR Weather App are equal in that they contain subdirectories for :term:`FMS`, :term:`FV3`, :term:`NEMS`
and stochastic_physics. However, in the MR Weather App, subdirectories are located under ``src/model``.
The MR Weather App also includes directories for CIME, such as the ``src/model/FV3/cime`` and
``src/model/NEMS/cime`` directories.

Users working outside of preconfigured platforms will have additional files on disk associated with
the libraries, pre- and post-processing.  The resulting directory structure is determined by the path
settings in the NCEPLIBS ``.gitmodules`` file.
