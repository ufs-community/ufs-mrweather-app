.. _testing:
  
=======
Testing
=======

There are around 38 test cases available for the regression testing to ensure the system is installed correctly and works fine. The regression testing (RT) also make sure that new code upgrades should not have side effects on the existing functionalities. It ensures that the system still works once the latest code changes are done. The RT can be run on Cheyenne, Orion, and Stampede. There is no preexist baseline and the users need to create the baseline by themselves.

`create_test <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/Tools_user/create_test.html>`_ is the tool that is used to do the regression testing.
It can be used as an easy way to run a single basic test or an entire suite of tests.  
`create_test <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/Tools_user/create_test.html>`_ runs a test suite in parallel for improved performance.  
It is the driver behind the automated nightly testing of cime-driven models.

More information about CIME testing can be found on `CIME: Testing <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/testing.html>`_.

Test requirements
=================
In order to run the tests, NCEPLIB and NCEPLIBS-external need to be installed (see :numref:`Chapter %s <config_new_platform>` for instructions). These libraries have been preinstalled on Cheyenne, but not on Stampede and Orion.

The input data needed for the tests are staged on preconfigured machine Cheyenne. On Orion and Stampede, data must be acquired from the ftp site and staged on disk (see :numref:`Chapter %s <inputs_and_outputs>`). Then setting the running environment according to :numref:`Chapter %s <quickstart>`. 


Testname syntax
===============

Tests are named with the following forms, [ ]=optional::

  TESTTYPE[_MODIFIERS].GRID.COMPSET[.MACHINE_COMPILER][.GROUP-TESTMODS]

where:

- ``TESTTYPE`` defines the general type of test, e.g. SMS. Following is the list of tests that are supported by `Medium-Range Weather Application <https://github.com/ufs-community/ufs-mrweather-app>`_.

  * SMS: Smoke startup test (default 5 days).
         | Do a 5 day initial test. (file suffix: base)

  * ERS: Exact restart from startup (default 6 days + 5 days)
         | Do an 11 day initial test - write a restart at day 6.    (file suffix: base)
         | Do a 5 day restart test, starting from restart at day 6. (file suffix: rest)
         | Compare component history files '.base' and '.rest' at day 11. They should be identical.
  * PET: Modified threading OPENMP bit for bit test (default 5 days)
         | Do an initial run where all components are threaded by default. (file suffix: base) Do another initial run with NTHRDS=1 for all components. (file suffix: single_thread) Compare base and single_thread.

- ``MODIFIERS`` changes to the default settings for the test.
- ``GRID`` The model grid (can be an alias). Currently, ``C96``, ``C192``, ``C384`` and ``C768`` are supported.
- ``COMPSET`` alias of the compset, or long name, if no ``--xml`` arguments are used. It can be ``GFSv15p2`` or ``GFSv16beta``.
- ``MACHINE`` This is optional; if this value is not supplied, `create_test <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/Tools_user/create_test.html>`_ will probe the underlying machine.
- ``COMPILER`` If this value is not supplied, use the default compiler for ``MACHINE``.
- ``GROUP-TESTMODS`` This is optional. This points to a directory with  ``user_nl_xxx`` files or a ``shell_commands`` that can be used to make namelist and ``XML`` modifications prior to running a test.

Query list of supported tests
=============================

**$CIMEROOT/scripts/query_testlists** gathers descriptions of the tests and testlists available
for UFS, the components, and projects.

The ``--xml-{compiler,machine,category,testlist}`` arguments can be used 
as in create_test (above) to focus the search.
The 'category' descriptor of a test can be used to run a group of associated tests at the same time.
The available categories, with the tests they encompass, can be listed by::

    cd $SRCROOT/cime/scripts
    ./query_testlists --define-testtypes

The ``--show-options`` argument does the same, but displays the 'options' defined for the tests,
such as queue, walltime, etc..

Using **create_test** 
==============================

To run a Smoke startup test::

    cd $SRCROOT/cime/scripts
    ./create_test SMS_D_Lh5.C96.GFSv15p2 --workflow ufs-mrweather_wo_post --test-id try

This will build and run the test in ``/glade/scratch/$USER/SMS_D_Lh5.C96.GFSv15p2.cheyenne_intel.try`` and this directory 
is called as **CASEROOT**. The run directory is in **CASEROOT/run** and the build is in **CASEROOT/bld**.

In this case, the C96 resolution model case with CCPP suite version v15p2 is created and runs 5 hours (**Lh5**) without post-processing step.

To run a test with baseline comparisons against baseline name 'master'::

    cd $SRCROOT/cime/scripts
    ./create_test SMS_Lh5.C96.GFSv15p2 --workflow ufs-mrweather_wo_post --test-id try --compare master --baseline-root $BASELINE_ROOT

To run a Exact restart test::

    cd $SRCROOT/cime/scripts
    ./create_test ERS_Lh11.C96.GFSv15p2 --workflow ufs-mrweather_wo_post --test-id try

This will build and run the test that includes two runs, first an 11 hour initial run (cold start) with a restart written at hour 6 and then a restart run (warm start) starting from hour 6 and compare the outputs written at hour 11. The output of the runs must be same.  

To run a threaded test::

    cd $SRCROOT/cime/scripts
    ./create_test PET_Lh11.C96.GFSv15p2 --workflow ufs-mrweather_wo_post --test-id try

To run entire test suite::

    cd $SRCROOT/cime/scripts
    ./create_test --xml-testlist ../../src/model/FV3/cime/cime_config/testlist.xml --xml-machine MACHINE --generate GENERATE --baseline-root BASELINE_ROOT --workflow ufs-mrweather_wo_post  

This will run entire test suite on specified machine ``MACHINE`` such as Stampede2 and generates the baseline under ``BASELINE_ROOT`` directory with a name of ``GENERATE``. 

