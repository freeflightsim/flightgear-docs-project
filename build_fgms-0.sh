#!/bin/bash

ROOT=`pwd`
DIR="fgms-0"
DOXY="docx/doxy.conf"
CHECKOUT="https://git.gitorious.org/~ffs/fgms/ffss-fgms-0-x.git"

echo "===================================================="
echo "Building fgms-0 docs from ./externals/$DIR"

git submodule init

rm -f -r ./docs/$DIR

cd ./externals/$DIR/
rm -f -r build_docs/

git pull
git checkout master


cp -f $ROOT/etc/fg_docx_header.html docx/
cp -f $ROOT/etc/fg_docx_footer.html docx/

## use the default doxygen stylesheet.css so it works cutom and default
cp -f $ROOT/etc/fg_docx_style.css docx/stylesheet.css


#TODO - Make the version from /version ??
VER="1.stable"
echo "VER=$VER" 
( cat $DOXY ; 
	echo "PROJECT_NUMBER=$VER"; \
	echo "HTML_HEADER = docx/fg_docx_header.html";  \
	echo "HTML_FOOTER = docx/fg_docx_footer.html";  \
	echo "HTML_STYLESHEET = docx/stylesheet.css";  \
	) | doxygen -

## Copy logo file after build
cp $ROOT/etc/logo-23.png build_docs/

../../etc/write_info.py  --out=build_docs/ --version="$VER" --dir=$DIR \
	--title="FGMS-0"  --git="$CHECKOUT" --color="#A684AC"
exit
rm $ROOT/zips/$DIR.zip
cd build_docs/
zip -r $ROOT/zips/$DIR.zip ./


#cp -r build_docs/ $ROOT/docs/$DIR/

