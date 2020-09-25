.. _testing:
  
=======
Testing
=======

There are several tests available as part of the regression testing suite to ensure the system is installed correctly and works properly. The regression test also confirms that code upgrades do not have side effects on existing functionalities and ensures that the system still works after code changes are made. The regression test can only be run on Cheyenne, Orion, and Stampede. 

Pre-existing baselines are not provided for this App. Users can run the tests without using a baseline (just to certify that the tests run to completion) or create their own baseline (to compare future runs against).

`create_test <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/Tools_user/create_test.html>`_ is the CIME tool used to execute the regression tests.
It can be used as an easy way to run a single basic test or an entire suite of tests.  
`create_test <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/Tools_user/create_test.html>`_ runs a test suite in parallel for improved performance.  
It is the driver behind the automated nightly testing of cime-driven models.

More information about CIME testing can be found on `CIME: Testing <https://esmci.github.io/cime/versions/ufs_release_v1.1/html/users_guide/testing.html>`_.

Test requirements
=================

In order to run the tests, NCEPLIBS and NCEPLIBS-external need to be installed (see :numref:`Chapter %s <config_new_platform>` for instructions). These libraries have been preinstalled on Cheyenne, but not on Stampede and Orion.

The code must have been downloaded before the regression tests can be run. This can be done with the following commands: ::

    mkdir -p $myUFS_INPUT/ufs_inputdata/icfiles/201908/20190829  # Create subdirectory for raw ICs
    git clone https://github.com/ufs-community/ufs-mrweather-app.git -b ufs-v1.1.0 my_ufs_sandbox
    cd my_ufs_sandbox
    ./manage_externals/checkout_externals

Several environment variables need to be set before running the regression tests. The instructions below provide quick information on how to set up the environment variables (for complete information, users should refer to :numref:`Chapter %s <quickstart>`). ::

    export myUFS_INPUT=my_directory	# Directory for staging input datasets
    export UFS_SCRATCH=my_scratch_space  # Directory for output files
    export PROJECT=your_compute_project 	# Project you can use to conduct runs in your platform
    export UFS_DRIVER=nems		# Do not change
    export CIME_MODEL=ufs			# Do not change


The input data required for the tests needs to be on disk before the tests are submitted. It is already staged on Cheyenne since it is a preconfigured platform. On Orion and Stampede, data must be acquired from the ftp site and staged on disk before proceeding with the test. The instructions below provide quick information on how to stage data on disk (for complete information, users should refer to :numref:`Chapter %s <inputs_and_outputs>`). ::

    mkdir -p $myUFS_INPUT/ufs_inputdata/icfiles/201908/20190829  # Create subdirectory for raw ICs
    cd $myUFS_INPUT/ufs_inputdata/icfiles/201908/20190829
    wget https://ftp.emc.ncep.noaa.gov/EIB/UFS/inputdata/201908/20190829/gfs_4_20190829_0000_000.grb2
    ln -s gfs_4_20190829_0000_000.grb2 atm.input.ic.grb2 # Link raw ICs to expected name


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
for UFS, the components, and projects. The available tests for Cheyenne: ::

    prealpha   : SMS_Lh3.C96.GFSv15p2.cheyenne_intel          
    prealpha   : SMS_Lh3.C96.GFSv15p2.cheyenne_gnu            
    prealpha   : SMS_Lh3.C96.GFSv16beta.cheyenne_intel        
    prealpha   : SMS_Lh3.C96.GFSv16beta.cheyenne_gnu          
    prealpha   : SMS_Lh3_D.C96.GFSv15p2.cheyenne_intel        
    prealpha   : SMS_Lh3_D.C96.GFSv15p2.cheyenne_gnu          
    prealpha   : SMS_Lh3_D.C96.GFSv16beta.cheyenne_intel      
    prealpha   : SMS_Lh3_D.C96.GFSv16beta.cheyenne_gnu        
    prealpha   : ERS_Lh11.C96.GFSv15p2.cheyenne_intel         
    prealpha   : ERS_Lh11.C96.GFSv15p2.cheyenne_gnu           
    prealpha   : ERS_Lh11.C96.GFSv16beta.cheyenne_intel       
    prealpha   : ERS_Lh11.C96.GFSv16beta.cheyenne_gnu         
    prealpha   : PET_Lh11.C96.GFSv15p2.cheyenne_intel         
    prealpha   : PET_Lh11.C96.GFSv15p2.cheyenne_gnu           
    prealpha   : SMS_Lh3.C192.GFSv15p2.cheyenne_intel         
    prealpha   : SMS_Lh3.C192.GFSv15p2.cheyenne_gnu           
    prealpha   : SMS_Lh3.C192.GFSv16beta.cheyenne_intel       
    prealpha   : SMS_Lh3.C192.GFSv16beta.cheyenne_gnu         
    prealpha   : SMS_Lh3_D.C192.GFSv15p2.cheyenne_intel       
    prealpha   : SMS_Lh3_D.C192.GFSv15p2.cheyenne_gnu         
    prealpha   : SMS_Lh3_D.C192.GFSv16beta.cheyenne_intel     
    prealpha   : SMS_Lh3_D.C192.GFSv16beta.cheyenne_gnu       
    prealpha   : SMS_Lh3.C384.GFSv15p2.cheyenne_intel         
    prealpha   : SMS_Lh3.C384.GFSv15p2.cheyenne_gnu           
    prealpha   : SMS_Lh3.C384.GFSv16beta.cheyenne_intel       
    prealpha   : SMS_Lh3.C384.GFSv16beta.cheyenne_gnu         
    prealpha   : SMS_Lh3_D.C384.GFSv15p2.cheyenne_intel       
    prealpha   : SMS_Lh3_D.C384.GFSv15p2.cheyenne_gnu         
    prealpha   : SMS_Lh3_D.C384.GFSv16beta.cheyenne_intel     
    prealpha   : SMS_Lh3_D.C384.GFSv16beta.cheyenne_gnu       
    prealpha   : SMS_Lh3.C768.GFSv15p2.cheyenne_intel         
    prealpha   : SMS_Lh3.C768.GFSv15p2.cheyenne_gnu           
    prealpha   : SMS_Lh3.C768.GFSv16beta.cheyenne_intel       
    prealpha   : SMS_Lh3.C768.GFSv16beta.cheyenne_gnu         
    prealpha   : SMS_Lh3_D.C768.GFSv15p2.cheyenne_intel       
    prealpha   : SMS_Lh3_D.C768.GFSv15p2.cheyenne_gnu         
    prealpha   : SMS_Lh3_D.C768.GFSv16beta.cheyenne_intel     
    prealpha   : SMS_Lh3_D.C768.GFSv16beta.cheyenne_gnu       

The results indicate that there are tests available on Cheyenne for two compilers (Intel and GNU). Furthermore, the results indicate that all tests are part of a ``testlist`` called prealpha. ``Testlists`` are lists that aggregate a number of tests under a single umbrella. All tests contained in a ``testlist`` can be run with single command when the ``testlist`` is passed as an argument to the create_test command.

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

To run a SMS test::

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

The commands to run the regression test on Cheyenne, Orion, and Stampede are below. You must replace the compute projects listed (using variable ``PROJECT``) to a project you can use to run the tests. 

For Cheyenne: ::
    qcmd -l walltime=3:00:00 -- “export UFS_DRIVER=nems; CIME_MODEL=ufs; PROJECT=p48503002 ./create_test --xml-testlist ../../src/model/FV3/cime/cime_config/testlist.xml --xml-machine cheyenne --workflow ufs-mrweather_wo_post  --xml-category prealpha"

For Orion: ::
    export UFS_DRIVER=nems; CIME_MODEL=ufs; PROJECT=gmtb ./create_test --xml-testlist ../../src/model/FV3/cime/cime_config/testlist.xml --xml-machine orion --generate GENERATE --baseline-root BASELINE_ROOT --workflow ufs-mrweather_wo_post --xml-compiler intel --xml-category prealpha

On Stampede it is necessary to submit the tests divided in three ``testlists`` (`prealpha_p1`, `pre_alpha_p2`, and `prealpha_p3`) because there is a limit to the number of jobs a user can have in the queue at a given time. Users should submit each set of tests separately, and wait for all tests to finish before submitting the next set: ::
    export UFS_DRIVER=nems; CIME_MODEL=ufs; PROJECT=tg854445 ./create_test --xml-testlist ../../src/model/FV3/cime/cime_config/testlist.xml --xml-machine stampede2-skx --workflow ufs-mrweather_wo_post -j 4 --walltime 01:00:00 --xml-compiler intel --xml-category prealpha_p1
    export UFS_DRIVER=nems; CIME_MODEL=ufs; PROJECT=tg854445 ./create_test --xml-testlist ../../src/model/FV3/cime/cime_config/testlist.xml --xml-machine stampede2-skx --workflow ufs-mrweather_wo_post -j 4 --walltime 01:00:00 --xml-compiler intel --xml-category prealpha_p2
    export UFS_DRIVER=nems; CIME_MODEL=ufs; PROJECT=tg854445 ./create_test --xml-testlist ../../src/model/FV3/cime/cime_config/testlist.xml --xml-machine stampede2-skx --workflow ufs-mrweather_wo_post -j 4 --walltime 01:00:00 --xml-compiler intel --xml-category prealpha_p3 

The running status can be checked by the following command::

    ./cs.status

Test success is defined as no failures and no jobs left in pending (PEND) state.
