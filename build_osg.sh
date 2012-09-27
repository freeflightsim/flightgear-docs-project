#!/bin/bash

ROOT=`pwd`
DIR="osg"
CONF="doxy-osg.conf"
CHECKOUT="http://www.openscenegraph.org/svn/osg/OpenSceneGraph/tags/OpenSceneGraph-3.0.1"


#svn checkout http://www.openscenegraph.org/svn/osg/OpenSceneGraph/tags/OpenSceneGraph-3.0.1 externals/osg




echo "===================================================="
echo "Building OSG docs from ./externals/$DIR"

rm ./externals/$DIR/doxy-osg.conf
cp ./etc/doxy-osg.conf ./externals/$DIR/doxy-osg.conf

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/



#TODO - Make the version from /version ??
VER="3.0.1"
echo "VER=$VER" 
doxygen doxy-osg.conf

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="OSG" --svn="$CHECKOUT" --color="blue"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
