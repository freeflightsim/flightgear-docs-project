#!/bin/bash

ROOT=`pwd`
DIR="simgear"
CONF="Doxyfile"
CHECKOUT="https://git.gitorious.org/~ffs/fg/ffss-simgear.git"

echo "===================================================="
echo "Building SimGear docs from ./externals/$DIR"

git submodule init

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git checkout next
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

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
   --title="SimGear" --git="$CHECKOUT" --color="#DEDE45"

cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./


