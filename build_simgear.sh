#!/bin/bash

ROOT=`pwd`
DIR="simgear"
CONF="Doxyfile"


echo "===================================================="
echo "Building SimGear docs from ./externals/$DIR"

git submodule init

rm -f -r ./_builds/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git pull
git checkout next

#TODO - Make the version from /version ??
VER=`cat version`
echo "VER=$VER" 
( cat $CONF ; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -



cp -r build_docs/ $ROOT/_builds/$DIR/

