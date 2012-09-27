#!/bin/bash

ROOT=`pwd`
DIR="flightgear"
CONF="doxygen-fgfs-src.conf"


echo "===================================================="
echo "Building FlightGear docs from ./externals/$DIR"

git submodule init
git submodule update

rm -f -r ./_builds/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git pull origin docs
git checkout docs

#TODO - Make the version from /version ??
VER=`cat version`
echo "VER=$VER" 
( cat $CONF ; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

cp README build_docs_fgfs/html/
cp README.* build_docs_fgfs/html/
cp INSTALL build_docs_fgfs/html/
cp COPYING build_docs_fgfs/html/


cp -r build_docs_fgfs/ $ROOT/_builds/$DIR/

