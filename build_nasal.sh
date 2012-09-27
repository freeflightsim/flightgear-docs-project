#!/bin/bash

ROOT=`pwd`
DIR="nasal"
#CONF="Doxyfile"
CHECKOUT="svn.freeflightsim.orgfgdata/master/"

echo "===================================================="
echo "Building Nasal docs from ./externals/$DIR"

#mkdir ./externals/nasal/
#svn co http://svn.freeflightsim.org/fgdata/master/Nasal/ ./externals/nasal/Nasal/

#cd ./externals/nasal/
rm -f -r  ./externals/nasal/build_docs/
mkdir ./externals/nasal/build_docs/

./externals/flightgear/scripts/python/ parse ./externals/fgdata/


mv $ROOT/nasal_api_doc.html build_docs/index.html

../../etc/write_info.py  -o build_docs/ -v "head" -d $DIR -t "Nasal" -s "$CHECKOUT"


zip -r -j $ROOT/zips/$DIR.zip build_docs/



