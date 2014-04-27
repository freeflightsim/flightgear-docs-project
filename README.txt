+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+ FlightGear Documentation Project          
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

API Docs generated from this project at
http://docs.freeflightsim.org/

Project Code:
https://github.com/FreeFlightSim/flightgear-docs-project

Current Maintainer:
Pedro Morgan - #peteffs on irc  

---------------------------------------------------------------------
Introduction
---------------------------------------------------------------------

The idea is to create an automated system to generate the docs.

This project is a collection of scripts that:-

* checkouts git repos with git externals
* checks our other repos via wget, ftp svn etc

* Most of the repositories are forks, with docifications to doxy files.


---------------------------------------------------------------------
SOURCE
---------------------------------------------------------------------
* etc/* - some helper functions
* build_* - scripts to create the docs
* zips/ -  temp location of the zips
* externals/* - directories for all the checkouts and sources


---------------------------------------------------------------------
TODO
---------------------------------------------------------------------
* Interlink the apis, eg flightgear to simgear
  Needs teh tags on import
* Generate OSM, plib, OpenAL and others


---------------------------------------------------------------------
ISSUES
---------------------------------------------------------------------
* doxygen on server  needs ?
* gestart generation ??
* Missing libs ?





