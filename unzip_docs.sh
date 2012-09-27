#!/bin/bash


files=( "fgms-1" "simgear"  "terragear" "nasal" "flightgear" "osg") 

for F in "${files[@]}"
do
   rm -f -r ./doc_root/$F/
   unzip -u ../upload_docs/$F.zip   -d ./doc_root/$F/
   cp ../upload_docs/$F.zip ./doc_root/$F/$F.zip
done;