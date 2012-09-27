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

#doxygen -w html media/header media/footer media/style.css  $CONF


../../etc/write_info.py  -o build_docs/ -v "$VER" -d $DIR -t "TerraGear" 

cp -r build_docs/ $ROOT/docs/$DIR/

