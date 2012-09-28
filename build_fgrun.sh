#!/bin/bash

ROOT=`pwd`
DIR="fgrun"
DOXY="Doxyfile"
CHECKOUT="https://gitorious.org/~ffs/fg/ffss-fgrun"


#svn co https://plib.svn.sourceforge.net/svnroot/plib/trunk plib externals/plib

git submodule init




echo "===================================================="
echo "Building FGRUN docs from ./externals/$DIR"



cd ./externals/$DIR

git checkout master
git pull
git checkout master

rm -f -r build_docs/
mkdir build_docs/




VER=`cat version`
echo "VER=$VER" 
( cat $DOXY; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -



cp NEWS README ABOUT-NLS COPYING AUTHORS build_docs/html/

$ROOT/etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="FG Run" --svn="$CHECKOUT" --color="#BAC7E1"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
