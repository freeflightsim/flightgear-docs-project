#!/bin/bash

ROOT=`pwd`
DIR="plib"
CONF="doxy-plib.conf"
CHECKOUT="https://plib.svn.sourceforge.net/svnroot/plib/trunk plib externals/plib"


#svn co https://plib.svn.sourceforge.net/svnroot/plib/trunk plib externals/plib




echo "===================================================="
echo "Building Plib docs from ./externals/$DIR"

rm ./externals/$DIR/trunk/doxy-plib.conf
rm ./externals/$DIR/trunk/src/DoxyMain-plib.cpp
cp ./etc/doxy-plib.conf ./externals/$DIR/trunk/doxy-plib.conf
cp ./etc/DoxyMain-plib.cpp ./externals/$DIR/trunk/src/DoxyMain-plib.cpp

#rm -f -r ./docs/$DIR

cd ./externals/$DIR/trunk/
rm -f -r build_docs/
mkdir build_docs/



#TODO - Make the version from /version ??
VER="1.8.5"
echo "VER=$VER" 
doxygen doxy-plib.conf

mkdir build_docs/html/doc/
cp -v -r doc/* build_docs/html/doc/

cp INSTALL README README.* AUTHORS build_docs/html/

../../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="PLIB" --svn="$CHECKOUT" --color="blue"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
