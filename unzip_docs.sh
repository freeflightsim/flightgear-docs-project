#!/bin/bash


files=("simgear" "terragear" "fgms-1") # "simgear" "flightgear")

for F in "${files[@]}"
do
   unzip -u ../upload_docs/$F.zip -d ./doc_root/$F/
   cp ../upload_docs/$F.zip ./doc_root/$F.zip
done;