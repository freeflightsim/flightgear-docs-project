#!/bin/bash

ROOT=`pwd`
DIR="nasal"
#CONF="Doxyfile"
CHECKOUT="http://svn.freeflightsim.org/fgdata/master/"

echo "===================================================="
echo "Building Nasal docs from ./externals/$DIR"

mkdir ./externals/nasal/
#svn co http://svn.freeflightsim.org/fgdata/master/Nasal/ ./externals/nasal/Nasal/

#cd ./externals/nasal/
rm -f -r  ./externals/nasal/build_docs/
mkdir ./externals/nasal/build_docs/

./externals/flightgear/scripts/python/nasal_api_doc.py parse ./externals/fgdata/Nasal


mv $ROOT/nasal_api_doc.html ./externals/nasal/build_docs/index.html

./etc/write_info.py  -o ./externals/nasal/build_docs/ -v "head" -d $DIR -t "Nasal" -s "$CHECKOUT"


zip -r -j $ROOT/zips/$DIR.zip ./externals/nasal/build_docs/



