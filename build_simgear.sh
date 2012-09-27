#!/bin/bash

ROOT=`pwd`
DIR="simgear"
CONF="Doxyfile"


echo "===================================================="
echo "Building SimGear docs from ./externals/$DIR"

git submodule init

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git pull
git checkout next

#TODO - Make the version from /version ??
VER=`cat version`
echo "VER=$VER" 
( cat $CONF ; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

cp README build_docs/html/
cp README.* build_docs/html/
cp INSTALL build_docs/html/
cp COPYING build_docs/html/


../../etc/write_info.py  -o build_docs/ -v "$VER" -d $DIR -t "SimGear" -g "https://git.gitorious.org/~ffs/fg/ffss-simgear.git"


zip -r -j $ROOT/zips/$DIR.zip build_docs/html/


