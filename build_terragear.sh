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

git pull origin master
git checkout master


#TODO - Make the version from /version ??
VER=`next`
#echo "VER=$VER" -return @version@.. umm
( cat $CONF ; echo "PROJECT_NUMBER=$VER" ) | doxygen -



../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="TerraGear" --git "$CHECKOUT" --color="#9ECC9E"


rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
 

