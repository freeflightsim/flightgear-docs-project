#!/bin/bash

ROOT=`pwd`
DIR="terragear"
CONF="doxygen-src.conf"


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



../../etc/write_info.py  -o build_docs/html/ -v "$VER" -d $DIR -t "TerraGear" -g "git://gitorious.org/fg/terragear.git"

#cp -r build_docs/ $ROOT/docs/$DIR/
# SimGear
zip -r -j $ROOT/zips/$DIR.zip build_docs/html/


