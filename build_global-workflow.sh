#!/usr/bin/bash

set -x

usage() {
  set +x
  echo
  echo "Usage: $0 -a <UFS_app> | -c <build_config> | -v | -h "
  echo
  echo "  -a  Build a specific UFS_app instead of the default"
  echo "  -c  Selectively build based on the provided build_config instead of the default config"
  echo "  -v  Execute all build scripts with -v option"
  echo "  -h  print this help message and exit"
  echo
  set -x
  exit 1
}

build_ufs_option=""
build_v_option=""

while getopts ":a:c:v:h" flag;

do
        case "${flag}" in
	        a) build_ufs_option+="-a ${OPTARG} ";;
		c) build_ufs_option+="-c ${OPTARG} ";;
                v) build_v_option+="-v";;
		h) usage;;
		*) echo "Invalid options: -$flag" ;;	    
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
