.. _cime_overview:

=================================
Additional information about CIME
=================================

All compiler flags are defined in
``cime/config/ufs/machines/config_compilers.xml``. This file contains
all supported compilers and the specific compiler flags to be used for
building with that
compiler. ``cime/config/ufs/machines/config_compilers.xml`` contains
compiler flags for each target compiler. In general, flags are not
system dependent and are valid on all systems. However, there can be
machine or OS (useful to generalize over eg MacOS or Cray systems)
dependent flags.

All environment variables and module operations are defined in
``cime/config/ufs/machines/config_machines.xml``.  The environment
variables are sorted by machine name and can be subset for compiler,
mpilib, debug, etc.

The following describes how the xml files in the ``cime/config/ufs/machines/``
directory are utilized in the case directory that is created for you
when you invoke **create_newcase**.

.. note::

   It is important to point out that for
   a model component to be CIME CCS compliant, it needs to have a
   directory ``cime_config/`` that contains a ``buildlib`` script that
   tells CIME how to build that component and a ``buildnml`` script that
   tells CIME how to generate namelists for your target component
   configuration.

- CIMEs ``case.setup script`` reads the ``config_compilers.xml`` file and
  creates a ``Macros.make`` and ``Macros.cmake`` file in youe case directory.
- The ``Macros.cmake`` file is then used by the file ``FV3/cime/cime_config/buildlib`` to build your model component.
  ``Macros.cmake`` is included by file ``configure_cime.cmake`` and there the compiler
  flag names are translated to those used by the FV3GFS cmake build.  If
  CCPP is used the ccpp_precompile script is called
  prior to calling the cmake for the model.  Finally gmake is called and
  all the libraries are built, verbose records of the build are written
  to the atm.bldlog.timestamp file in the case EXEROOT.

When you create an MR Weather Application case, CIME will create a
``$CASEROOT`` directory for you.  It will also create a
``$CASEROOT/SourceMods/src.fv3gfs`` directory where you can put in
modified source code that you can use for your experiment.  The CIME
build will look in the ``$CASEROOT/SourceMods/src.fv3gfs`` directory
for any source file matching the name of any source file in the
build. (FMS, CCPP, stochastic_physics, FV3) If it finds a match it
will use the file in ``SourceMods/src.fv3gfs`` instead of the matching
file in your checked out code sandbox.  If a file is removed from
``SourceMods/src.fv3gfs`` then the next build will again use the
original file your checked out code base.  For best interaction with
the git repository it is recommended that you edit source files in the
source tree and do not use the SourceMods mechanism, however keep in
mind that source files changed in this way will affect *all* cases
associated with the source tree.
