#!/bin/bash

ROOT=`pwd`
DIR="flightgear"
CONF="doxygen-fgfs-src.conf"
CHECKOUT="git://gitorious.org/~ffs/fg/ffss-flightgear2.git"

echo "===================================================="
echo "Building FlightGear docs from ./externals/$DIR"

git submodule init
git submodule update

rm -f -r ./_builds/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git checkout docs
git pull 
git checkout docs

#TODO - Make the version from /version ??
VER=`cat version`
echo "VER=$VER" 
( cat $CONF ; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

cp README build_docs_fgfs/html/
cp README.* build_docs_fgfs/html/
cp INSTALL build_docs_fgfs/html/
cp COPYING build_docs_fgfs/html/
mkdir build_docs_fgfs/html/docs-mini/
cp docs-mini/* build_docs_fgfs/html/docs-mini/

../../etc/write_info.py  --out=build_docs_fgfs/ --version="$VER" --dir=$DIR \
  --title="FlightGear" --git="$CHECKOUT" --color="#6280BA"

rm $ROOT/zips/$DIR.zip
cd build_docs_fgfs/
zip -r  $ROOT/zips/$DIR.zip ./


