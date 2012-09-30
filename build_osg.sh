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

cp -f ./etc/fg_docx_header.html ./externals/$DIR/
cp -f ./etc/fg_docx_footer.html ./externals/$DIR/

## use the default doxygen stylesheet.css so it works cutom and default
cp -f ./etc/fg_docx_style.css ./externals/$DIR/stylesheet.css


cd ./externals/$DIR
rm -f -r build_docs/


#TODO - Make the version from /version ??
VER="3.1.3"
echo "VER=$VER"
( cat doxy-osg.conf; \
	echo "PROJECT_NUMBER=$VER"; \
	echo "HTML_HEADER = fg_docx_header.html";  \
	echo "HTML_FOOTER = fg_docx_footer.html";  \
	echo "HTML_STYLESHEET = stylesheet.css";  \
	) | doxygen -

cp AUTHORS.txt LICENSE.txt NEWS.txt README.txt build_docs/html/

## Copy logo file after build
cp $ROOT/etc/logo-23.png build_docs/

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
  --title="OSG" --svn="$CHECKOUT" --color="#B8C5E0"

rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r  $ROOT/zips/$DIR.zip ./
