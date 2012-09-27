#!/bin/bash




echo "1=$1"

if [ $1 == "all" ];
then
	echo "Upload all"
	scp zips/*.zip fgx@docs.freeflightsim.org:/home/fgx/upload_docs/
else
	echo "Upload many"
	for F
	do scp zips/$F.zip fgx@docs.freeflightsim.org:/home/fgx/upload_docs/
	done
fi
