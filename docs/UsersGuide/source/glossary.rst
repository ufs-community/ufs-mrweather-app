.. _Glossary:

*************************
Glossary
*************************

.. glossary::

   CCPA
      Climatology-Calibrated Precipitation Analysis (CCPA) data. This data is required for METplus precipitation verification tasks within the SRW App. The most recent 8 days worth of data are publicly available and can be accessed `here <https://ftp.ncep.noaa.gov/data/nccf/com/ccpa/prod/>`__. 

   CCPP
      The `Common Community Physics Package <https://dtcenter.org/community-code/common-community-physics-package-ccpp>`_ is a forecast-model agnostic, vetted collection of codes containing atmospheric physical parameterizations and suites of parameterizations for use in Numerical Weather Prediction (NWP) along with a framework that connects the physics to the host forecast model.

   CESM
   Community Earth System Model
      The `Community Earth System Model <https://www.cesm.ucar.edu/>`__ is a community climate model centered at the National Center for Atmospheric Research (:term:`NCAR`). 

   chgres_cube
       The preprocessing software used to create initial condition files to "coldstart" the forecast
       model. The initial conditions are created from either GFS :term:`GRIB2` or :term:`NEMSIO` data.

   CIME
      The `Common Infrastructure for Modeling Earth <https://github.com/ESMCI/cime>`__ (CIME - pronounced "SEAM") consists of a Case Control System (CCS) that supports the configuration, compilation, execution, system testing, and unit testing of an Earth System Model. The CIME CCS is used in :term:`CESM` and was previously used in the Medium-Range Weather (MRW) Application. View the CIME documentation `here <https://esmci.github.io/cime/versions/master/html/index.html>`__.


   Component
      A software element that has a clear function and interface. In Earth system models, components are often single portions of the Earth system (e.g. atmosphere, ocean, or land surface) that are assembled to form a whole.

   Compset
   Compsets
      A component set. It refers to a particular mix of components, along with a component-specific configuration and/or namelist settings.

   CONUS
      Continental United States

   Coupled
   Coupled model
   Coupled models
      A coupled model joins two or more weather or climate model components into one larger Earth systems model for more accurate predictions. Fully-coupled models contain an atmospheric model, an ocean model, a land model, and a sea ice model. 
   
      ..
         COMMENT: Is this accurate?

   DA
   Data Assimilation
      Data assimilation is the combining of diverse data, possibly sampled at different times and intervals and different locations, into a unified and consistent description of a physical system, such as the state of the atmosphere or the Earth system.

   Dycore
   Dynamical core
      Global atmospheric model based on fluid dynamics principles, including Euler's equations of motion.

   echo top
      The radar-indicated top of an area of precipitation. Specifically, it contains the height of the 18 dBZ reflectivity value.

   FMS
      The Flexible Modeling System (FMS) is a software framework for supporting the efficient
      development, construction, execution, and scientific interpretation of atmospheric,
      oceanic, and climate system models.

   free-forecast
      Free-forecast mode means that the application is running without data assimilation/data cycling capabilities. 

   FV3
      The Finite-Volume Cubed-Sphere :term:`Dynamical Core` (dycore). Developed at NOAA's Geophysical 
      Fluid Dynamics Laboratory (GFDL), it is a scalable and flexible dycore capable of both 
      hydrostatic and non-hydrostatic atmospheric simulations. It is the dycore used in the 
      UFS Weather Model.

   GFS
      `Global Forecast System <https://www.ncei.noaa.gov/products/weather-climate-models/global-forecast>`_. The GFS is a National Centers for Environmental Prediction (NCEP) weather forecast model that generates data for dozens of atmospheric and land-soil variables, including temperatures, winds, precipitation, soil moisture, and atmospheric ozone concentration. The system couples four separate models (atmosphere, ocean model, land/soil model, and sea ice) that work together to accurately depict weather conditions.

   GRIB2 
      The second version of the World Meterological Organization's (WMO) standard for distributing gridded data. 

   HPC-Stack
      The `HPC-Stack <https://github.com/NOAA-EMC/hpc-stack>`__ is a repository that provides a unified, shell script-based build system for building the software stack required for numerical weather prediction (NWP) tools such as the `Unified Forecast System (UFS) <https://ufscommunity.org/>`__ and the `Joint Effort for Data assimilation Integration (JEDI) <https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/>`__ framework.

   HPSS
      High Performance Storage System (HPSS).

   IC
   ICs
      Initial conditions

   MRMS
      Multi-Radar/Multi-Sensor (MRMS) System Analysis data. This data is required for METplus composite reflectivity or :term:`echo top` verification tasks within the SRW App. A two-day archive of precipitation, radar, and aviation and severe weather fields is publicly available and can be accessed `here <https://mrms.ncep.noaa.gov/data/>`__.

   MPI
      MPI stands for Message Passing Interface. An MPI is a standardized communication system used in parallel programming. It establishes portable and efficient syntax for the exchange of messages and data between multiple processors that are used by a single computer program. An MPI is required for high-performance computing (HPC).

   NAM
      `North American Mesoscale Forecast System <https://www.ncei.noaa.gov/products/weather-climate-models/north-american-mesoscale>`_. NAM generates multiple grids (or domains) of weather forecasts over the North American continent at various horizontal resolutions. Each grid contains data for dozens of weather parameters, including temperature, precipitation, lightning, and turbulent kinetic energy. NAM uses additional numerical weather models to generate high-resolution forecasts over fixed regions, and occasionally to follow significant weather events like hurricanes.

   NCAR
      The `National Center for Atmospheric Research <https://ncar.ucar.edu/>`__. 

   NCEP
      National Centers for Environmental Prediction, an arm of the National Weather Service.

   NCEPLIBS
      The NCEP library source code and utilities required for chgres_cube, the UFS Weather Model, and UPP.

   NCEPLIBS-external
      A collection of third-party libraries required to build NCEPLIBS, chgres_cube, the UFS Weather Model, and UPP.

   NCL
      An interpreted language designed specifically for scientific data analysis and visualization.
      More information can be found at https://www.ncl.ucar.edu.

   NDAS
      :term:`NAM` Data Assimilation System (NDAS) data. This data is required for METplus surface and upper-air verification tasks within the SRW App. The most recent 1-2 days worth of data are publicly available in PrepBufr format and can be accessed `here <ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rap/prod>`__. The most recent 8 days of data can be accessed `here <https://nomads.ncep.noaa.gov/pub/data/nccf/com/nam/prod/>`__.

   NEMS
      The NOAA Environmental Modeling System - a software infrastructure that supports
      NCEP/EMC's forecast products.

   NEMSIO
      A binary format for atmospheric model output on the native gaussian grid.

   NetCDF
      NetCDF (`Network Common Data Form <https://www.unidata.ucar.edu/software/netcdf/>`__) is a file format and community standard for storing multidimensional scientific data. It includes a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data.

   NWP
   Numerical Weather Prediction
      Numerical Weather Prediction (NWP) takes current observations of weather and processes them with computer models to forecast the future state of the weather. 

   Repository
      A central location in which files (e.g., data, code, documentation) are stored and managed. 

   spack-stack
      The `spack-stack <https://github.com/NOAA-EMC/spack-stack>`__ is a collaborative effort between the NOAA Environmental Modeling Center (EMC), the UCAR Joint Center for Satellite Data Assimilation (JCSDA), and the Earth Prediction Innovation Center (EPIC). *spack-stack* is a repository that provides a Spack-based method for building the software stack required for numerical weather prediction (NWP) tools such as the `Unified Forecast System (UFS) <https://ufscommunity.org/>`__ and the `Joint Effort for Data assimilation Integration (JEDI) <https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/latest/>`__ framework. spack-stack uses the Spack package manager along with custom Spack configuration files and Python scripts to simplify installation of the libraries required to run various applications. The *spack-stack* can be installed on a range of platforms and comes pre-configured for many systems. Users can install the necessary packages for a particular application and later add the missing packages for another application without having to rebuild the entire stack.

   Stochastic physics
      1. Stochastics physics schemes are physics packages that apply randomized perturbations to the physical tendencies or the physical parameters of a model in order to compensate for model uncertainty. 
      2. Stochastic Physics also refers to the specific package of stochastic schemes used alongside the CCPP to represent model uncertainty: SKEB (Stochastic Kinetic Energy Backscatter), SPPT (Stochastically Perturbed Physics Tendencies), SHUM (Specific Humidity), SPP (Stochastically Perturbed Parameterizations), and LSM SPP (Land Surface Model SPP).  

   Suite
      A collection of primary physics schemes and interstitial schemes that are known to work
      well together

   UFS
      A Unified Forecast System (UFS) is a community-based, coupled comprehensive Earth
      system modeling system. The UFS numerical applications span local to global domains
      and predictive time scales from sub-hourly analyses to seasonal predictions. It is
      designed to support the Weather Enterprise and to be the source system for NOAA's
      operational numerical weather prediction applications

   Umbrella repository
      A repository that houses external code, or "externals," from additional repositories.

   Uncoupled
   Uncoupled model
   Uncoupled models
      An uncoupled model contains just one weather or climate model, unlike :term:`coupled models`, which bundle together two or more different weather/climate model components. 

   UPP
   Unified Post Processor
      The `Unified Post Processor <https://dtcenter.org/community-code/unified-post-processor-upp>`__ is software developed at :term:`NCEP` and used operationally for models maintained by NCEP. The UPP processes raw model output from a variety of :term:`NCEP`'s NWP models, including the FV3.

   Weather Enterprise
      Individuals and organizations from public, private, and academic sectors that contribute to the research, development, and production of weather forecast products; primary consumers of these weather forecast products.

   Weather Model
      A prognostic model that can be used for short- and medium-range research and
      operational forecasts. It can be an atmosphere-only model or be an atmospheric
      model coupled with one or more additional components, such as a wave or ocean model.