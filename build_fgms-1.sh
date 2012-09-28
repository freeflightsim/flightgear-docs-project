#!/bin/bash

ROOT=`pwd`
DIR="fgms-1"
CONF="Doxyfile"
CHECKOUT="https://git.gitorious.org/~ffs/fgms/ffs-docs-fgms-1-x.git"

echo "===================================================="
echo "Building fgms-1 docs from ./externals/$DIR"

git submodule init

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/

git pull
git checkout master

#TODO - Make the version from /version ??
VER="1.future"
echo "VER=$VER" 
( cat $CONF ; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

cp README build_docs/html/
cp INSTALL build_docs/html/
cp COPYING build_docs/html/
cp TODO build_docs/html/
cp AUTHORS build_docs/html/
cp src/server/fgms-example.conf build_docs/html/fgms-example.conf.xml
cp mp-proto-spec.xml build_docs/html/mp-proto-spec.xml

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
	--title="FGMS-1"  --git="$CHECKOUT" --color="#A684AC"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r $ROOT/zips/$DIR.zip ./


#cp -r build_docs/ $ROOT/docs/$DIR/

