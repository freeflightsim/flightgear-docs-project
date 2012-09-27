#!/bin/bash

ROOT=`pwd`
DIR="fgms-1"
CONF="Doxyfile"


echo "===================================================="
echo "Building fgms-1 docs from ./externals/$DIR"

git submodule init

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git pull
git checkout master

#TODO - Make the version from /version ??
VER="1.x"
echo "VER=$VER" 
( cat $CONF ; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

cp README build_docs/html/
cp INSTALL build_docs/html/
cp COPYING build_docs/html/
cp TODO build_docs/html/

../../etc/write_info.py  -o build_docs/ -v "$VER" -d $DIR -t "FG MultiPlayer Server (1.x.future)" 


cp -r build_docs/ $ROOT/docs/$DIR/

