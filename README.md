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
git clone -b feature/global_workflow https://github.com/jkbk2004/ufs-mrweather-app
cd ufs-mrweather-app
```

```
./manage_externals/checkout_externals
```


2. Build UFS model and global-workflow components

```
sh build_global-workflow.sh [-c]
(Use the -c option to compile for coupled UFS)
```

3. Run experiment generator script

```
cd ush/rocoto
./setup_expt.py forecast-only --pslot test --idate 2020010100 --edate 2020010118 --resdet 384 --gfs_cyc 4 --comrot /some_large_disk_area/comrot --expdir /some_safe_disk_area/expdir 
```

4. ufs-mrweather-app directort tree

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



