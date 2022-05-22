# UFS Medium-Range Weather App

This repository contains the model code and external links needed to
build the UFS Medium-Range Weather Application, which focuses on
atmospheric behavior out to about two weeks. This application will
includes a full workflow, with pre-processing (preparation of inputs),
a forecast model, and post-processing.

Details at:
https://github.com/ufs-community/ufs-mrweather-app/wiki

Getting started

1. Clone ufs-mrweather-app and check out global-workflow

```
git clone https://github.com/ufs-community/ufs-mrweather-app
cd ufs-mrweather-app
```

```
./manage_externals/checkout_externals
```


2. Build UFS model and global-workflow components

```
sh build_global-workflow.sh [-a UFS_app] [-c build_config] [-v]  [-h]
-a: S2SWA (default), ATM, ATMA, S2S, and S2SW
-c: build_config instead of the default config
-v: build verbose option
-h: print usesage and exit
(e.g.: sh build_global-workflow.sh will build the default option, S2SWA)sh build_global-workflow.sh [-c]
```

3. Run experiment generator script

```
cd ush/rocoto
./setup_expt.py forecast-only --pslot test --idate 2020010100 --edate 2020010118 --resdet 384 --gfs_cyc 4 --comrot /some_large_disk_area/comrot --expdir /some_safe_disk_area/expdir 
```

4. ufs-mrweather-app directory tree

```
ufs-mrweather-app/
├── build_global-workflow.sh
├── describe_version
├── docs
│   └── UsersGuide
├── Externals.cfg
├── Externals.cfg.v1.0
├── global-workflow
│   ├── docs
│   ├── driver
│   ├── ecflow
│   ├── env
│   ├── exec
│   ├── Externals.cfg
│   ├── fix
│   ├── gempak
│   ├── jobs
│   ├── modulefiles
│   ├── parm
│   ├── README.md
│   ├── scripts
│   ├── sorc
│   ├── ush
│   └── util
├── LICENSE.md
├── manage_externals
│   ├── checkout_externals
│   ├── LICENSE.txt
│   ├── manic
│   └── README.md
├── plotting_scripts
│   ├── plot_mrw_cloud_diff.py
│   ├── plot_mrw.py
│   ├── python_plotting_documentation.txt
│   └── sample_output.pdf
└── README.md
```

5. global-workflow directory tree

```
global-workflow/
├── docs
│   ├── archive
│   ├── doxygen
│   ├── note_fixfield.txt
│   ├── Release_Notes.gfs_downstream.v15.2.0.txt
│   ├── Release_Notes.gfs_downstream.v16.0.0.txt
│   ├── Release_Notes.gfs.v15.2.0.txt
│   ├── Release_Notes.gfs.v15.2.2.txt
│   ├── Release_Notes.gfs.v16.0.0.md
│   └── Release_Notes.gfs.v16.1.0.txt
├── driver
│   ├── gdas
│   ├── gfs
│   └── product
├── ecflow
│   └── ecf
├── env
│   ├── gfs.ver
│   ├── HERA.env
│   ├── JET.env
│   ├── ORION.env
│   ├── WCOSS_C.env
│   └── WCOSS_DELL_P3.env
├── exec
│   ├── calc_analysis.x -> ../sorc/gsi.fd/exec/calc_analysis.x
│   ├── calc_increment_ens_ncio.x -> ../sorc/gsi.fd/exec/calc_increment_ens_ncio.x
│   ├── calc_increment_ens.x -> ../sorc/gsi.fd/exec/calc_increment_ens.x
│   ├── emcsfc_ice_blend -> ../sorc/ufs_utils.fd/exec/emcsfc_ice_blend
│   ├── emcsfc_snow2mdl -> ../sorc/ufs_utils.fd/exec/emcsfc_snow2mdl
│   ├── enkf_chgres_recenter_nc.x -> ../sorc/install/bin/enkf_chgres_recenter_nc.x
│   ├── enkf_chgres_recenter.x -> ../sorc/install/bin/enkf_chgres_recenter.x
│   ├── fbwndgfs -> ../sorc/install/bin/fbwndgfs.x
│   ├── fv3nc2nemsio.x -> ../sorc/install/bin/fv3nc2nemsio.x
│   ├── gaussian_sfcanl.exe -> ../sorc/install/bin/gaussian_sfcanl.x
│   ├── gdas2gldas -> ../sorc/gldas.fd/exec/gdas2gldas
│   ├── getsfcensmeanp.x -> ../sorc/gsi.fd/exec/getsfcensmeanp.x
│   ├── getsigensmeanp_smooth.x -> ../sorc/gsi.fd/exec/getsigensmeanp_smooth.x
│   ├── getsigensstatp.x -> ../sorc/gsi.fd/exec/getsigensstatp.x
│   ├── gfs_bufr -> ../sorc/install/bin/gfs_bufr.x
│   ├── gfs_ncep_post -> ../sorc/gfs_post.fd/exec/upp.x
│   ├── gldas2gdas -> ../sorc/gldas.fd/exec/gldas2gdas
│   ├── gldas_forcing -> ../sorc/gldas.fd/exec/gldas_forcing
│   ├── gldas_model -> ../sorc/gldas.fd/exec/gldas_model
│   ├── gldas_post -> ../sorc/gldas.fd/exec/gldas_post
│   ├── gldas_rst -> ../sorc/gldas.fd/exec/gldas_rst
│   ├── global_cycle -> ../sorc/ufs_utils.fd/exec/global_cycle
│   ├── global_enkf.x -> ../sorc/gsi.fd/exec/global_enkf.x
│   ├── global_gsi.x -> ../sorc/gsi.fd/exec/global_gsi.x
│   ├── interp_inc.x -> ../sorc/gsi.fd/exec/interp_inc.x
│   ├── ncdiag_cat.x -> ../sorc/gsi.fd/exec/ncdiag_cat.x
│   ├── oznmon_horiz.x -> ../sorc/gsi.fd/exec/oznmon_horiz.x
│   ├── oznmon_time.x -> ../sorc/gsi.fd/exec/oznmon_time.x
│   ├── radmon_angle.x -> ../sorc/gsi.fd/exec/radmon_angle.x
│   ├── radmon_bcoef.x -> ../sorc/gsi.fd/exec/radmon_bcoef.x
│   ├── radmon_bcor.x -> ../sorc/gsi.fd/exec/radmon_bcor.x
│   ├── radmon_time.x -> ../sorc/gsi.fd/exec/radmon_time.x
│   ├── recentersigp.x -> ../sorc/gsi.fd/exec/recentersigp.x
│   ├── reg2grb2.x -> ../sorc/install/bin/reg2grb2.x
│   ├── regrid_nemsio -> ../sorc/install/bin/regrid_nemsio.x
│   ├── supvit -> ../sorc/install/bin/supvit.x
│   ├── syndat_getjtbul -> ../sorc/install/bin/syndat_getjtbul.x
│   ├── syndat_maksynrc -> ../sorc/install/bin/syndat_maksynrc.x
│   ├── syndat_qctropcy -> ../sorc/install/bin/syndat_qctropcy.x
│   ├── tave.x -> ../sorc/install/bin/tave.x
│   ├── tocsbufr -> ../sorc/install/bin/tocsbufr.x
│   ├── ufs_model -> ../sorc/ufs_model.fd/build/ufs_model
│   ├── vint.x -> ../sorc/install/bin/vint.x
│   ├── ww3_gint
│   ├── ww3_grib
│   ├── ww3_grid
│   ├── ww3_ounf
│   ├── ww3_ounp
│   ├── ww3_outf
│   ├── ww3_outp
│   ├── ww3_prep
│   └── ww3_prnc
├── Externals.cfg
├── fix
│   ├── fix_aer -> /work/noaa/global/glopara/fix_NEW/fix_aer
│   ├── fix_am -> /work/noaa/global/glopara/fix_NEW/fix_am
│   ├── fix_chem -> /work/noaa/global/glopara/fix_NEW/fix_chem
│   ├── fix_cice -> /work/noaa/global/glopara/fix_NEW/fix_cice
│   ├── fix_cpl -> /work/noaa/global/glopara/fix_NEW/fix_cpl
│   ├── fix_fv3_fracoro -> /work/noaa/global/glopara/fix_NEW/fix_fv3_fracoro
│   ├── fix_fv3_gmted2010 -> /work/noaa/global/glopara/fix_NEW/fix_fv3_gmted2010
│   ├── fix_gldas -> /work/noaa/global/glopara/fix_NEW/fix_gldas
│   ├── fix_gsi -> ../sorc/gsi.fd/fix
│   ├── fix_lut -> /work/noaa/global/glopara/fix_NEW/fix_lut
│   ├── fix_mom6 -> /work/noaa/global/glopara/fix_NEW/fix_mom6
│   ├── fix_orog -> /work/noaa/global/glopara/fix_NEW/fix_orog
│   ├── fix_reg2grb2 -> /work/noaa/global/glopara/fix_NEW/fix_reg2grb2
│   ├── fix_sfc_climo -> /work/noaa/global/glopara/fix_NEW/fix_sfc_climo
│   ├── fix_ugwd -> /work/noaa/global/glopara/fix_NEW/fix_ugwd
│   ├── fix_verif -> /work/noaa/global/glopara/fix_NEW/fix_verif
│   ├── fix_wave -> /work/noaa/global/glopara/fix_NEW/fix_wave
│   ├── gdas
│   └── product
├── gempak
│   ├── dictionaries
│   ├── fix
│   └── ush
├── jobs
│   ├── JGDAS_ATMOS_ANALYSIS_DIAG -> ../sorc/gsi.fd/jobs/JGDAS_ATMOS_ANALYSIS_DIAG
│   ├── JGDAS_ATMOS_CHGRES_FORENKF -> ../sorc/gsi.fd/jobs/JGDAS_ATMOS_CHGRES_FORENKF
│   ├── JGDAS_ATMOS_GEMPAK
│   ├── JGDAS_ATMOS_GEMPAK_META_NCDC
│   ├── JGDAS_ATMOS_GLDAS -> ../sorc/gldas.fd/jobs/JGDAS_ATMOS_GLDAS
│   ├── JGDAS_ATMOS_VERFOZN -> ../sorc/gsi.fd/util/Ozone_Monitor/nwprod/gdas_oznmon/jobs/JGDAS_ATMOS_VERFOZN
│   ├── JGDAS_ATMOS_VERFRAD -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/gdas_radmon/jobs/JGDAS_ATMOS_VERFRAD
│   ├── JGDAS_ATMOS_VMINMON -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/gdas.v1.0.0/jobs/JGDAS_ATMOS_VMINMON
│   ├── JGDAS_ENKF_DIAG -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_DIAG
│   ├── JGDAS_ENKF_ECEN -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_ECEN
│   ├── JGDAS_ENKF_FCST -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_FCST
│   ├── JGDAS_ENKF_POST -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_POST
│   ├── JGDAS_ENKF_SELECT_OBS -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_SELECT_OBS
│   ├── JGDAS_ENKF_SFC -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_SFC
│   ├── JGDAS_ENKF_UPDATE -> ../sorc/gsi.fd/jobs/JGDAS_ENKF_UPDATE
│   ├── JGFS_ATMOS_AWIPS_20KM_1P0DEG
│   ├── JGFS_ATMOS_AWIPS_G2
│   ├── JGFS_ATMOS_CYCLONE_GENESIS
│   ├── JGFS_ATMOS_CYCLONE_TRACKER
│   ├── JGFS_ATMOS_FBWIND
│   ├── JGFS_ATMOS_FSU_GENESIS
│   ├── JGFS_ATMOS_GEMPAK
│   ├── JGFS_ATMOS_GEMPAK_META
│   ├── JGFS_ATMOS_GEMPAK_NCDC_UPAPGIF
│   ├── JGFS_ATMOS_GEMPAK_PGRB2_SPEC
│   ├── JGFS_ATMOS_PGRB2_SPEC_NPOESS
│   ├── JGFS_ATMOS_POSTSND
│   ├── JGFS_ATMOS_VMINMON -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/gfs.v1.0.0/jobs/JGFS_ATMOS_VMINMON
│   ├── JGLOBAL_ATMOS_ANALYSIS -> ../sorc/gsi.fd/jobs/JGLOBAL_ATMOS_ANALYSIS
│   ├── JGLOBAL_ATMOS_ANALYSIS_CALC -> ../sorc/gsi.fd/jobs/JGLOBAL_ATMOS_ANALYSIS_CALC
│   ├── JGLOBAL_ATMOS_EMCSFC_SFC_PREP
│   ├── JGLOBAL_ATMOS_NCEPPOST -> ../sorc/gfs_post.fd/jobs/JGLOBAL_ATMOS_NCEPPOST
│   ├── JGLOBAL_ATMOS_POST_MANAGER -> ../sorc/gfs_post.fd/jobs/JGLOBAL_ATMOS_POST_MANAGER
│   ├── JGLOBAL_ATMOS_TROPCY_QC_RELOC
│   ├── JGLOBAL_FORECAST
│   ├── JGLOBAL_WAVE_GEMPAK
│   ├── JGLOBAL_WAVE_INIT
│   ├── JGLOBAL_WAVE_POST_BNDPNT
│   ├── JGLOBAL_WAVE_POST_BNDPNTBLL
│   ├── JGLOBAL_WAVE_POST_PNT
│   ├── JGLOBAL_WAVE_POST_SBS
│   ├── JGLOBAL_WAVE_PRDGEN_BULLS
│   ├── JGLOBAL_WAVE_PRDGEN_GRIDDED
│   ├── JGLOBAL_WAVE_PREP
│   └── rocoto
├── modulefiles
│   ├── module_base.hera.lua
│   ├── module_base.jet.lua
│   ├── module_base.orion.lua
│   ├── module_base.wcoss_dell_p3.lua
│   ├── modulefile.ww3.hera.lua
│   ├── modulefile.ww3.orion.lua
│   ├── modulefile.ww3.wcoss_dell_p3.lua
│   ├── module-setup.csh.inc
│   ├── module-setup.sh.inc
│   ├── workflow_utils.hera.lua
│   ├── workflow_utils.jet.lua
│   ├── workflow_utils.orion.lua
│   └── workflow_utils.wcoss_dell_p3.lua
├── parm
│   ├── chem
│   ├── config
│   ├── gldas -> ../sorc/gldas.fd/parm
│   ├── mom6
│   ├── mon
│   ├── parm_fv3diag
│   ├── parm_wave
│   ├── post -> ../sorc/gfs_post.fd/parm
│   ├── product
│   ├── relo
│   ├── transfer_gdas_1a.list
│   ├── transfer_gdas_1b.list
│   ├── transfer_gdas_1c.list
│   ├── transfer_gdas_enkf_enkf_05.list
│   ├── transfer_gdas_enkf_enkf_10.list
│   ├── transfer_gdas_enkf_enkf_15.list
│   ├── transfer_gdas_enkf_enkf_20.list
│   ├── transfer_gdas_enkf_enkf_25.list
│   ├── transfer_gdas_enkf_enkf_30.list
│   ├── transfer_gdas_enkf_enkf_35.list
│   ├── transfer_gdas_enkf_enkf_40.list
│   ├── transfer_gdas_enkf_enkf_45.list
│   ├── transfer_gdas_enkf_enkf_50.list
│   ├── transfer_gdas_enkf_enkf_55.list
│   ├── transfer_gdas_enkf_enkf_60.list
│   ├── transfer_gdas_enkf_enkf_65.list
│   ├── transfer_gdas_enkf_enkf_70.list
│   ├── transfer_gdas_enkf_enkf_75.list
│   ├── transfer_gdas_enkf_enkf_80.list
│   ├── transfer_gdas_enkf_enkf_misc.list
│   ├── transfer_gdas_misc.list
│   ├── transfer_gfs_10a.list
│   ├── transfer_gfs_10b.list
│   ├── transfer_gfs_1.list
│   ├── transfer_gfs_2.list
│   ├── transfer_gfs_3.list
│   ├── transfer_gfs_4.list
│   ├── transfer_gfs_5.list
│   ├── transfer_gfs_6.list
│   ├── transfer_gfs_7.list
│   ├── transfer_gfs_8.list
│   ├── transfer_gfs_9a.list
│   ├── transfer_gfs_9b.list
│   ├── transfer_gfs_gempak.list
│   ├── transfer_gfs_misc.list
│   ├── transfer_gfs_wave_restart1.list
│   ├── transfer_gfs_wave_restart2.list
│   ├── transfer_gfs_wave_restart3.list
│   ├── transfer_gfs_wave_rundata.list
│   ├── transfer_gfs_wave_wave.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_1.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_2.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_3.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_4.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_5.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_6.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_7.list
│   ├── transfer_rdhpcs_gdas_enkf_enkf_8.list
│   ├── transfer_rdhpcs_gdas.list
│   ├── transfer_rdhpcs_gfs.list
│   ├── transfer_rdhpcs_gfs_nawips.list
│   ├── wave
│   └── wmo
├── README.md
├── scripts
│   ├── exemcsfc_global_sfc_prep.sh -> ../sorc/ufs_utils.fd/scripts/exemcsfc_global_sfc_prep.sh
│   ├── exgdas_atmos_chgres_forenkf.sh -> ../sorc/gsi.fd/scripts/exgdas_atmos_chgres_forenkf.sh
│   ├── exgdas_atmos_gempak_gif_ncdc.sh
│   ├── exgdas_atmos_gldas.sh -> ../sorc/gldas.fd/scripts/exgdas_atmos_gldas.sh
│   ├── exgdas_atmos_nawips.sh
│   ├── exgdas_atmos_nceppost.sh -> ../sorc/gfs_post.fd/scripts/exgdas_atmos_nceppost.sh
│   ├── exgdas_atmos_verfozn.sh -> ../sorc/gsi.fd/util/Ozone_Monitor/nwprod/gdas_oznmon/scripts/exgdas_atmos_verfozn.sh
│   ├── exgdas_atmos_verfrad.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/gdas_radmon/scripts/exgdas_atmos_verfrad.sh
│   ├── exgdas_atmos_vminmon.sh -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/gdas.v1.0.0/scripts/exgdas_atmos_vminmon.sh
│   ├── exgdas_enkf_ecen.sh -> ../sorc/gsi.fd/scripts/exgdas_enkf_ecen.sh
│   ├── exgdas_enkf_fcst.sh -> ../sorc/gsi.fd/scripts/exgdas_enkf_fcst.sh
│   ├── exgdas_enkf_post.sh -> ../sorc/gsi.fd/scripts/exgdas_enkf_post.sh
│   ├── exgdas_enkf_select_obs.sh -> ../sorc/gsi.fd/scripts/exgdas_enkf_select_obs.sh
│   ├── exgdas_enkf_sfc.sh -> ../sorc/gsi.fd/scripts/exgdas_enkf_sfc.sh
│   ├── exgdas_enkf_update.sh -> ../sorc/gsi.fd/scripts/exgdas_enkf_update.sh
│   ├── exgfs_aero_init_aerosol.py
│   ├── exgfs_atmos_awips_20km_1p0deg.sh
│   ├── exgfs_atmos_fbwind.sh
│   ├── exgfs_atmos_gempak_gif_ncdc_skew_t.sh
│   ├── exgfs_atmos_gempak_meta.sh
│   ├── exgfs_atmos_goes_nawips.sh
│   ├── exgfs_atmos_grib2_special_npoess.sh
│   ├── exgfs_atmos_grib_awips.sh
│   ├── exgfs_atmos_nawips.sh
│   ├── exgfs_atmos_nceppost.sh -> exgfs_nceppost_cpl.sh
│   ├── exgfs_atmos_postsnd.sh
│   ├── exgfs_atmos_vminmon.sh -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/gfs.v1.0.0/scripts/exgfs_atmos_vminmon.sh
│   ├── exgfs_nceppost_cpl.sh
│   ├── exgfs_pmgr.sh
│   ├── exgfs_prdgen_manager.sh
│   ├── exgfs_wave_init.sh
│   ├── exgfs_wave_nawips.sh
│   ├── exgfs_wave_post_gridded_sbs.sh
│   ├── exgfs_wave_post_pnt.sh
│   ├── exgfs_wave_prdgen_bulls.sh
│   ├── exgfs_wave_prdgen_gridded.sh
│   ├── exgfs_wave_prep.sh
│   ├── exglobal_atmos_analysis_calc.sh -> ../sorc/gsi.fd/scripts/exglobal_atmos_analysis_calc.sh
│   ├── exglobal_atmos_analysis.sh -> ../sorc/gsi.fd/scripts/exglobal_atmos_analysis.sh
│   ├── exglobal_atmos_pmgr.sh -> ../sorc/gfs_post.fd/scripts/exglobal_atmos_pmgr.sh
│   ├── exglobal_atmos_tropcy_qc_reloc.sh
│   ├── exglobal_diag.sh -> ../sorc/gsi.fd/scripts/exglobal_diag.sh
│   ├── exglobal_forecast.sh
│   ├── run_gfsmos_master.sh.cray
│   ├── run_gfsmos_master.sh.dell
│   ├── run_gfsmos_master.sh.hera
│   ├── run_reg2grb2.sh
│   ├── run_regrid.sh
│   └── vsdbjob_submit.sh
├── sorc
│   ├── build
│   ├── build_all.sh
│   ├── build_gfs_util.sh
│   ├── build_gfs_wafs.sh
│   ├── build_gldas.sh
│   ├── build_gsi.sh
│   ├── build_ncep_post.sh
│   ├── build_ufs.sh
│   ├── build_ufs_utils.sh
│   ├── build_workflow_utils.sh
│   ├── build_ww3prepost.sh
│   ├── calc_analysis.fd -> gsi.fd/util/netcdf_io/calc_analysis.fd
│   ├── calc_increment_ens.fd -> gsi.fd/util/EnKF/gfs/src/calc_increment_ens.fd
│   ├── calc_increment_ens_ncio.fd -> gsi.fd/util/EnKF/gfs/src/calc_increment_ens_ncio.fd
│   ├── checkout.sh
│   ├── cmake
│   ├── CMakeLists.txt
│   ├── cpl_build.cfg
│   ├── emcsfc_ice_blend.fd -> ufs_utils.fd/sorc/emcsfc_ice_blend.fd
│   ├── emcsfc_snow2mdl.fd -> ufs_utils.fd/sorc/emcsfc_snow2mdl.fd
│   ├── enkf_chgres_recenter.fd
│   ├── enkf_chgres_recenter_nc.fd
│   ├── fbwndgfs.fd
│   ├── fregrid.fd -> ufs_utils.fd/sorc/fre-nctools.fd/tools/fregrid
│   ├── fv3nc2nemsio.fd
│   ├── gaussian_sfcanl.fd
│   ├── gdas2gldas.fd -> gldas.fd/sorc/gdas2gldas.fd
│   ├── getsfcensmeanp.fd -> gsi.fd/util/EnKF/gfs/src/getsfcensmeanp.fd
│   ├── getsigensmeanp_smooth.fd -> gsi.fd/util/EnKF/gfs/src/getsigensmeanp_smooth.fd
│   ├── getsigensstatp.fd -> gsi.fd/util/EnKF/gfs/src/getsigensstatp.fd
│   ├── gfs_bufr.fd
│   ├── gfs_build.cfg
│   ├── gfs_ncep_post.fd -> gfs_post.fd/sorc/ncep_post.fd
│   ├── gfs_post.fd
│   ├── gldas2gdas.fd -> gldas.fd/sorc/gldas2gdas.fd
│   ├── gldas.fd
│   ├── gldas_forcing.fd -> gldas.fd/sorc/gldas_forcing.fd
│   ├── gldas_model.fd -> gldas.fd/sorc/gldas_model.fd
│   ├── gldas_post.fd -> gldas.fd/sorc/gldas_post.fd
│   ├── gldas_rst.fd -> gldas.fd/sorc/gldas_rst.fd
│   ├── global_cycle.fd -> ufs_utils.fd/sorc/global_cycle.fd
│   ├── global_enkf.fd -> gsi.fd/src/enkf
│   ├── global_gsi.fd -> gsi.fd/src/gsi
│   ├── gsi.fd
│   ├── install
│   ├── interp_inc.fd -> gsi.fd/util/netcdf_io/interp_inc.fd
│   ├── link_workflow.sh
│   ├── logs
│   ├── machine-setup.sh
│   ├── make_hgrid.fd -> ufs_utils.fd/sorc/fre-nctools.fd/tools/make_hgrid
│   ├── make_solo_mosaic.fd -> ufs_utils.fd/sorc/fre-nctools.fd/tools/make_solo_mosaic
│   ├── ncdiag_cat.fd -> gsi.fd/src/ncdiag
│   ├── ncl.setup
│   ├── oznmon_horiz.fd -> gsi.fd/util/Ozone_Monitor/nwprod/oznmon_shared/sorc/oznmon_horiz.fd
│   ├── oznmon_time.fd -> gsi.fd/util/Ozone_Monitor/nwprod/oznmon_shared/sorc/oznmon_time.fd
│   ├── partial_build.sh
│   ├── radmon_angle.fd -> gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/sorc/verf_radang.fd
│   ├── radmon_bcoef.fd -> gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/sorc/verf_radbcoef.fd
│   ├── radmon_bcor.fd -> gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/sorc/verf_radbcor.fd
│   ├── radmon_time.fd -> gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/sorc/verf_radtime.fd
│   ├── recentersigp.fd -> gsi.fd/util/EnKF/gfs/src/recentersigp.fd
│   ├── reg2grb2.fd
│   ├── regrid_nemsio.fd
│   ├── supvit.fd
│   ├── syndat_getjtbul.fd
│   ├── syndat_maksynrc.fd
│   ├── syndat_qctropcy.fd
│   ├── tave.fd
│   ├── tocsbufr.fd
│   ├── ufs_model.fd
│   ├── ufs_utils.fd
│   ├── verif-global.fd
│   └── vint.fd
├── ush
│   ├── calcanl_gfs.py -> ../sorc/gsi.fd/ush/calcanl_gfs.py
│   ├── calcinc_gfs.py -> ../sorc/gsi.fd/ush/calcinc_gfs.py
│   ├── cplvalidate.sh
│   ├── drive_makeprepbufr.sh
│   ├── emcsfc_ice_blend.sh -> ../sorc/ufs_utils.fd/ush/emcsfc_ice_blend.sh
│   ├── emcsfc_snow.sh -> ../sorc/ufs_utils.fd/ush/emcsfc_snow.sh
│   ├── fix_precip.sh -> ../sorc/gfs_post.fd/ush/fix_precip.sh
│   ├── forecast_det.sh
│   ├── forecast_postdet.sh
│   ├── forecast_predet.sh
│   ├── fv3gfs_downstream_nems_cpl.sh
│   ├── fv3gfs_downstream_nems.sh -> fv3gfs_downstream_nems_cpl.sh
│   ├── fv3gfs_driver_grid.sh -> ../sorc/ufs_utils.fd/ush/fv3gfs_driver_grid.sh
│   ├── fv3gfs_dwn_nems.sh -> ../sorc/gfs_post.fd/ush/fv3gfs_dwn_nems.sh
│   ├── fv3gfs_filter_topo.sh -> ../sorc/ufs_utils.fd/ush/fv3gfs_filter_topo.sh
│   ├── fv3gfs_make_grid.sh -> ../sorc/ufs_utils.fd/ush/fv3gfs_make_grid.sh
│   ├── fv3gfs_make_orog.sh -> ../sorc/ufs_utils.fd/ush/fv3gfs_make_orog.sh
│   ├── fv3gfs_nc2nemsio.sh
│   ├── fv3gfs_regrid_nemsio.sh
│   ├── fv3gfs_remap.sh
│   ├── fv3gfs_remap_weights.sh
│   ├── gaussian_sfcanl.sh
│   ├── getdump.sh
│   ├── getges.sh
│   ├── getncdimlen -> ../sorc/gsi.fd/ush/getncdimlen
│   ├── gfs_bfr2gpk.sh
│   ├── gfs_bufr_netcdf.sh
│   ├── gfs_bufr.sh
│   ├── gfs_nceppost.sh -> ../sorc/gfs_post.fd/ush/gfs_nceppost.sh
│   ├── gfs_sndp.sh
│   ├── gfs_transfer.sh -> ../sorc/gfs_post.fd/ush/gfs_transfer.sh
│   ├── gfs_truncate_enkf.sh
│   ├── gldas_archive.sh -> ../sorc/gldas.fd/ush/gldas_archive.sh
│   ├── gldas_forcing.sh -> ../sorc/gldas.fd/ush/gldas_forcing.sh
│   ├── gldas_get_data.sh -> ../sorc/gldas.fd/ush/gldas_get_data.sh
│   ├── gldas_liscrd.sh -> ../sorc/gldas.fd/ush/gldas_liscrd.sh
│   ├── gldas_post.sh -> ../sorc/gldas.fd/ush/gldas_post.sh
│   ├── gldas_process_data.sh -> ../sorc/gldas.fd/ush/gldas_process_data.sh
│   ├── global_cycle_driver.sh -> ../sorc/ufs_utils.fd/ush/global_cycle_driver.sh
│   ├── global_cycle.sh -> ../sorc/ufs_utils.fd/ush/global_cycle.sh
│   ├── global_extrkr.sh
│   ├── global_savefits.sh
│   ├── gsi_utils.py -> ../sorc/gsi.fd/ush/gsi_utils.py
│   ├── hpssarch_gen.sh
│   ├── icepost.ncl
│   ├── inter_flux.sh
│   ├── link_crtm_fix.sh -> ../sorc/gfs_post.fd/ush/link_crtm_fix.sh
│   ├── load_fv3gfs_modules.sh
│   ├── merge_fv3_aerosol_tile.py
│   ├── minmon_xtrct_costs.pl -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/minmon_shared.v1.0.1/ush/minmon_xtrct_costs.pl
│   ├── minmon_xtrct_gnorms.pl -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/minmon_shared.v1.0.1/ush/minmon_xtrct_gnorms.pl
│   ├── minmon_xtrct_reduct.pl -> ../sorc/gsi.fd/util/Minimization_Monitor/nwprod/minmon_shared.v1.0.1/ush/minmon_xtrct_reduct.pl
│   ├── mod_icec.sh -> ../sorc/gfs_post.fd/ush/mod_icec.sh
│   ├── nems.configure.atm_aero.IN
│   ├── nems.configure.atm.IN
│   ├── nems.configure.blocked_atm_wav.IN
│   ├── nems.configure.cpld_aero_wave.IN
│   ├── nems.configure.cpld.IN
│   ├── nems.configure.cpld_wave.IN
│   ├── nems.configure.leapfrog_atm_wav.IN
│   ├── nems_configure.sh
│   ├── ocnpost.ncl
│   ├── ozn_xtrct.sh -> ../sorc/gsi.fd/util/Ozone_Monitor/nwprod/oznmon_shared/ush/ozn_xtrct.sh
│   ├── parse-storm-type.pl
│   ├── parsing_model_configure_DATM.sh
│   ├── parsing_model_configure_FV3.sh
│   ├── parsing_namelists_CICE.sh
│   ├── parsing_namelists_FV3.sh
│   ├── parsing_namelists_MOM6.sh
│   ├── radmon_ck_stdout.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/ush/radmon_ck_stdout.sh
│   ├── radmon_err_rpt.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/ush/radmon_err_rpt.sh
│   ├── radmon_verf_angle.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/ush/radmon_verf_angle.sh
│   ├── radmon_verf_bcoef.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/ush/radmon_verf_bcoef.sh
│   ├── radmon_verf_bcor.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/ush/radmon_verf_bcor.sh
│   ├── radmon_verf_time.sh -> ../sorc/gsi.fd/util/Radiance_Monitor/nwprod/radmon_shared/ush/radmon_verf_time.sh
│   ├── rocoto
│   ├── scale_dec.sh
│   ├── syndat_getjtbul.sh
│   ├── syndat_qctropcy.sh
│   ├── trim_rh.sh -> ../sorc/gfs_post.fd/ush/trim_rh.sh
│   ├── tropcy_relocate_extrkr.sh
│   ├── tropcy_relocate.sh
│   ├── WAM_XML_to_ASCII.pl
│   ├── wave_grib2_sbs.sh
│   ├── wave_grid_interp_sbs.sh
│   ├── wave_grid_moddef.sh
│   ├── wave_outp_cat.sh
│   ├── wave_outp_spec.sh
│   ├── wave_prnc_cur.sh
│   ├── wave_prnc_ice.sh
│   └── wave_tar.sh
└── util
    ├── modulefiles
    ├── sorc
    └── ush
```




