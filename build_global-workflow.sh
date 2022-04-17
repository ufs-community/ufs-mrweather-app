#!/usr/bin/bash

set -x

UFS_BUILD_OPTION=""

while getopts "c" flag;

do
        case "${flag}" in
	    c)
		echo "Received -c flag, building ufs-weather-model for S2SW app"
		UFS_BUILD_OPTION=-c
		break
		;;	    
        esac
done

# set current and working paths ---------------------------------------------------
echo "current path" $(pwd);
CUR_PWD=$(pwd)
cd global-workflow/sorc; WRK_PWD=$(pwd)

# checkout components -------------------------------------------------------------
sh checkout.sh                                                                                                                               

# turn off gsi build option -------------------------------------------------------                                                                                                                   
sed -i '6s/yes/no/g' fv3gfs_build.cfg                                                                                                        

# build and link components -------------------------------------------------------                                                           
if [ $UFS_BUILD_OPTION == "-c" ]; then
  sh build_all.sh -c                                                                                                                         
  logfile="logs/build_ufs.log"
  if [[ -f $logfile ]] ; then
    target=$(grep 'target=' $logfile | awk -F. '{print $1}' | awk -F= '{print $2}')
    sh link_workflow.sh emc $target coupled; cd $CUR_PWD; exit 0
  fi
else
  sh build_all.sh                                                                                                                            
  logfile="logs/build_ufs.log"
  if [[ -f $logfile ]] ; then
    target=$(grep 'target=' $logfile | awk -F. '{print $1}' | awk -F= '{print $2}')
    sh link_workflow.sh emc $target; cd $CUR_PWD; exit 0
  fi
fi

[[ -f "$WRK_PWD/logs/build_ufs.log" ]] && cd $CUR_PWD; echo "Error: logs/build_ufs.log does not exist." >&2; exit 1
