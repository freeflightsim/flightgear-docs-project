#!/bin/bash

ROOT=`pwd`
DIR="fgdata"
DOXY="doxy-fgdata.conf"
CHECKOUT="http://svn.freeflightsim.org/fgdata/master/"

echo "===================================================="
echo "Building FGDATA docs from ./externals/$DIR"

#mkdir ./externals/nasal/
#svn co http://svn.freeflightsim.org/fgdata/master/Nasal/ ./externals/nasal/Nasal/

#cd ./externals/nasal/
#rm -f -r  ./externals/nasal/build_docs/
#mkdir ./externals/nasal/build_docs/
#mkdir ./externals/nasal/build_docs/html/



rm ./externals/fgdata/$DOXY
cp ./etc/$DOXY ./externals/fgdata/$DOXY
cp ./etc/glsfilter.py ./externals/fgdata/
cp ./etc/DoxyMain-fgdata.cpp ./externals/fgdata/DoxyMain-fgdata.cpp

cd ./externals/fgdata/

VER=`cat version`
echo "VER=$VER" 
( cat $DOXY; echo "PROJECT_NUMBER=$VER"; echo "" ) | doxygen -

$ROOT/externals/flightgear/scripts/python/nasal_api_doc.py parse ./Nasal
cp ./nasal_api_doc.html build_docs/html/nasal-api-doc.html


rm -f -r build_docs/html/Docs/
cp -r Docs/ build_docs/html/Docs/


$ROOT/etc/write_info.py  --out ./build_docs/ --version "$VER" --dir=$DIR \
--title="FG Data" --svn="$CHECKOUT" --color="#CD4141"


rm $ROOT/zips/$DIR.zip 
cd build_docs/

zip -r  $ROOT/zips/$DIR.zip ./



