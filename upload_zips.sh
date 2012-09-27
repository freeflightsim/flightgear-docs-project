#!/bin/bash





if [ $1 == "all" ];
then
	echo "Upload all"
	scp zips/*.zip fgx@docs.freeflightsim.org:/home/fgx/upload_docs/
else
	echo "Upload selected"
	for F
	do scp zips/$F.zip fgx@docs.freeflightsim.org:/home/fgx/upload_docs/
	done
fi
