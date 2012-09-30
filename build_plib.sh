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

cp -f ./etc/fg_docx_header.html ./externals/$DIR/trunk/
cp -f ./etc/fg_docx_footer.html ./externals/$DIR/trunk/

## use the default doxygen stylesheet.css so it works cutom and default
cp -f ./etc/fg_docx_style.css ./externals/$DIR/trunk/stylesheet.css


cd ./externals/$DIR/trunk/
rm -f -r build_docs/


#TODO - Make the version from /version ??
VER="1.8.5"
echo "VER=$VER" 
( cat doxy-plib.conf; \
	echo "PROJECT_NUMBER=$VER"; \
	echo "HTML_HEADER = fg_docx_header.html";  \
	echo "HTML_FOOTER = fg_docx_footer.html";  \
	echo "HTML_STYLESHEET = stylesheet.css";  \
	) | doxygen -

## Copy logo file after build
cp $ROOT/etc/logo-23.png build_docs/


mkdir build_docs/html/doc/
cp -v -r doc/* build_docs/html/doc/

cp INSTALL README README.* AUTHORS build_docs/html/

../../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="PLIB" --svn="$CHECKOUT" --color="#539053"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
