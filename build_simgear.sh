#!/bin/bash

ROOT=`pwd`
DIR="simgear"
CONF="docx/doxy.conf"
CHECKOUT="https://git.gitorious.org/~ffs/fg/ffss-simgear.git"

echo "===================================================="
echo "Building SimGear docs from ./externals/$DIR"

git submodule init

rm -f -r ./docs/$DIR

cd ./externals/$DIR
rm -f -r build_docs/




git checkout next
git pull
git checkout next

mkdir build_docs/
cp -f $ROOT/etc/fg_docx_header.html docx/
cp -f $ROOT/etc/fg_docx_footer.html docx/

## use the default doxygen stylesheet.css so it works cutom and default
cp -f $ROOT/etc/fg_docx_style.css docx/stylesheet.css


#TODO - Make the version from /version ??
VER=`cat version`
echo "VER=$VER" 
( cat $CONF ; 
	echo "PROJECT_NUMBER=$VER"; \
	echo "HTML_HEADER = docx/fg_docx_header.html";  \
	echo "HTML_FOOTER = docx/fg_docx_footer.html";  \
	echo "HTML_STYLESHEET = docx/stylesheet.css";  \
	#echo "GENERATE_TREEVIEW = NO";  \
	) | doxygen -

## Copy logo file after build
cp $ROOT/etc/logo-23.png build_docs/

cp README build_docs/html/
cp README.* build_docs/html/
cp INSTALL build_docs/html/
cp COPYING build_docs/html/

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
   --title="SimGear" --git="$CHECKOUT" --color="#DEDE45"

cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./


