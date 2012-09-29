#!/bin/bash

ROOT=`pwd`
DIR="osg"
CONF="doxy-osg.conf"
CHECKOUT="http://www.openscenegraph.org/svn/osg/OpenSceneGraph/tags/OpenSceneGraph-3.1.1"


svn checkout $CHECKOUT externals/osg




echo "===================================================="
echo "Building OSG docs from ./externals/$DIR"

rm ./externals/$DIR/doxy-osg.conf
rm ./externals/$DIR/src/DoxyMain-osg.cpp
cp ./etc/doxy-osg.conf ./externals/$DIR/doxy-osg.conf
cp ./etc/DoxyMain-osg.cpp ./externals/$DIR/src/DoxyMain-osg.cpp

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/



#TODO - Make the version from /version ??
VER="3.1.3"
echo "VER=$VER"
( cat doxy-osg.conf; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

cp AUTHORS.txt LICENSE.txt NEWS.txt README.txt build_docs/html/

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="OSG" --svn="$CHECKOUT" --color="#B8C5E0"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
