#!/bin/bash

ROOT=`pwd`
DIR="terragear"
CONF="doxygen-src.conf"
CHECKOUT="https://git.gitorious.org/~ffs/fg/ffss-terragear.git"

echo "===================================================="
echo "Building TerraGear docs from ./externals/$DIR"

rm -f -r ./docs/$DIR

git submodule init
git submodule update

cd ./externals/$DIR

git pull
git checkout master


#TODO - Make the version from /version ??
VER=`next`
#echo "VER=$VER" -return @version@.. umm
( cat $CONF ; echo "PROJECT_NUMBER=$VER" ) | doxygen -



../../etc/write_info.py  -o build_docs/html/ -v "$VER" -d $DIR -t "TerraGear" -g "$CHECKOUT"

#cp -r build_docs/ $ROOT/docs/$DIR/

zip -r -j $ROOT/zips/$DIR.zip build_docs/html/


