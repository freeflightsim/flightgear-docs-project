#!/bin/bash


files=("terragear" "fgms-1") # "simgear" "flightgear")

for F in "${files[@]}"
do
   unzip -u ../upload_docs/$F.zip -d ./doc_root/$F/
done;