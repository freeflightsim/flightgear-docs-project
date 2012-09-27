#!/bin/bash


files=( "fgms-1" "simgear"  "terragear" "nasal" "flightgear" "osg") 

if [ $1 == "all" ];
then
	echo "Unzip  all"
	for F in "${files[@]}"
	do
	rm -f -r ./doc_root/$F/
	unzip -u ../upload_docs/$F.zip   -d ./doc_root/$F/
	cp ../upload_docs/$F.zip ./doc_root/$F/$F.zip
	done;
else
	echo "Unzip selected"
	for F
	do 
	rm -f -r ./doc_root/$F/
	unzip -u ../upload_docs/$F.zip   -d ./doc_root/$F/
	cp ../upload_docs/$F.zip ./doc_root/$F/$F.zip
	done
fi


