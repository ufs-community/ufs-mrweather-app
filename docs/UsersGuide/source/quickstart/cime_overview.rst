.. _cime_overview:

===================
Brief CIME Overview
===================

Not sure where this section belongs.

All compiler flags are defined in
cime/config/ufs/machines/config_compilers.xml. This file list all
supported compilers and the specific compiler flags to be used for
building with that compiler.  There is a general section that
describes compiler flags for each compiler that are valid on all
systems, there can be machine or OS (useful to generalize over eg
MacOS or Cray systems) dependent flags.  Environment variables and
module operations are defined in file config_machines.xml in the same
directory.  These are sorted by machine name and can be subset for
compiler, mpilib, debug, etc.

CIMEs case.setup script reads the config_compilers.xml file and
creates a Macros.make and Macros.cmake file in the case directory.
The Macros.cmake file is used by the FV3/cime/cime_config/buildlib.
It is included by file configure_cime.cmake and there the compiler
flag names are translated to those used by the FV3GFS cmake build.  If
CCPP is used the ccpp_precompile script and ccpp cmake are called
prior to calling the cmake for the model.  Finally gmake is called and
all the libraries are built, verbose records of the build are written
to the atm.bldlog.timestamp file in the case EXEROOT.

The cime build looks in the SourceMods/src.fv3gfs directory for any
source file matching the name of any source file in the build. (FMS,
CCPP, stochastic_physics, FV3) If it finds a match it will use the
file in SourceMods/src.fv3gfs instead of the matching file in src.  If
a file is removed from SourceMods then the next build will again use
the file in src.

We should create a test to compare the cime build to the cmake
standalone build on those systems where both are supported, making
sure that all of the switches allowed by the cmake build are working
correctly in cime.
