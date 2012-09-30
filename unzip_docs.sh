#!/bin/bash


files=( "fgms-1" "simgear"  "terragear" "fgdata" "flightgear" "osg" "flightgear-extras") 

if [ $1 == "all" ];
then
	echo "Unzip  all"
	for F in "${files[@]}"
	do
	rm -f -r ./www_root/$F/
	unzip -u ../upload_docs/$F.zip   -d ./$F/
	cp ../upload_docs/$F.zip ./$F/$F.zip
	done;
else
	echo "Unzip selected"
	for F
	do 
	rm -f -r ./www_root/$F/
	unzip -q -u ../upload_docs/$F.zip   -d ./www_root/$F/
	cp ../upload_docs/$F.zip ./www_root/$F/$F.zip
	done
fi


