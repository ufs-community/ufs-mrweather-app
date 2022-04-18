# UFS Medium-Range Weather App

This repository contains the model code and external links needed to
build the UFS Medium-Range Weather Application, which focuses on
atmospheric behavior out to about two weeks. This application will
includes a full workflow, with pre-processing (preparation of inputs),
a forecast model, and post-processing.

Details at:
https://github.com/ufs-community/ufs-mrweather-app/wiki

Getting started

# 1. Check out the code:
git clone -b feature/global_workflow https://github.com/jkbk2004/ufs-mrweather-app


```
git clone -b feature/global_workflow https://github.com/jkbk2004/ufs-mrweather-app
cd ufs-mrweather-app
```

Then, check out the global-workflow. 

```
./manage_externals/checkout_externals
```

# 2. Build the global-workflow

```
sh build_global-workflow.sh
```
