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
mkdir ./externals/nasal/build_docs/html/

./externals/flightgear/scripts/python/nasal_api_doc.py parse ./externals/fgdata/Nasal


mv $ROOT/nasal_api_doc.html ./externals/nasal/build_docs/html/index.html

./etc/write_info.py  --out ./externals/nasal/build_docs/ --version "$VER" --dir=$DIR \
--title="Nasal" --svn="$CHECKOUT" --color="#555588"

rm $ROOT/zips/$DIR.zip 
cd ./externals/nasal/build_docs/

zip -r  $ROOT/zips/$DIR.zip ./



