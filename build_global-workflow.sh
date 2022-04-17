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

echo "current path" $(pwd);
CUR_PWD=$(pwd);

cd global-workflow/sorc
sh checkout.sh

# turn off gsi build option
sed -i '6s/yes/no/g' fv3gfs_build.cfg

if [ $UFS_BUILD_OPTION == "-c" ]
then
    sh build_all.sh -c
    [[ -f log/build_ufs.log ]] && cd $CUR_PWD; echo "Error: log/build_ufs.log doesn't exist." >&2; exit 1
    target=$(grep 'target=' build_ufs.log | awk -F. '{ print $1 }' | awk -F= '{print $2}' )
    sh link_workflow.sh emc $target coupled
else
    sh build_all.sh
    [[ -f log/build_ufs.log ]] && cd $CUR_PWD; echo "Error: log/build_ufs.log doesn't exist." >&2; exit 1
    target=$(grep 'target=' build_ufs.log | awk -F. '{ print $1 }' | awk -F= '{print $2}' )
    sh link_workflow.sh emc $target
fi

cd $CUR_PWD
