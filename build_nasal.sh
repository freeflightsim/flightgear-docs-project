#!/bin/bash

ROOT=`pwd`
DIR="nasal"
#CONF="Doxyfile"
SVN="git@gitorious.org:~ffs/fg/ffss-simgear.git"

echo "===================================================="
echo "Building Nasal docs from ./externals/$DIR"

mkdir ./externals/nasal/
svn co http://svn.freeflightsim.org/fgdata/master/Nasal/ ./externals/nasal/Nasal/

cd ./externals/nasal/






