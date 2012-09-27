#!/bin/bash

ROOT=`pwd`
DIR="terragear"
CONF="doxygen-src.conf"


echo "===================================================="
echo "Building TerraGear docs from ./externals/$DIR"

rm -f -r ./_builds/$DIR

cd ./externals/$DIR

#TODO - Make the version from /version ??
VER=`cat VERSION.in`
#echo "VER=$VER" -return @version@.. umm
#( cat $CONF ; echo "PROJECT_NUMBER=$VER" ) | doxygen -

doxygen $CONF

cp -r build_docs/ $ROOT/_builds/$DIR/

