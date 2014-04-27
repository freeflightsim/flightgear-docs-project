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
* The documentation is currently generated on a lan workstation and scp
  to the server as debian squqeeze does not have the correct doxygen

----------------------------------------------------------------
The Concepts Ideas and Snagz
----------------------------------------------------------------
The idea is to auto generate documentation from source,
and spool this out on a regular basis.
So a change in the api or source code as a git commit, a little
spelling check, or adding some helpful comment etc would
automatically be auto gen.. a few moments later.. even on post commit triggers etc..

Also it would be nice for developers to have an official source to point to
with dealing with a manual that is constantly being updated.

There are many ways to skin a cat, but one of the easiest is to use the
tried and tested doxygen.

== The Doxygen Generation process ==
Using doxygen, a config file is needed with a few directives and options
which include the INPUT  and the OUTPUT_DIRECTORY
and then running the command to Docs>Gen
doxygen ./doxy-my-stuff.conf

Doxygen quite hapilly walks through all the files and tree and source
and extract all the relevant stuff and then spools out to a html or etc..

Changes to the comments in the code, changes the output of the auto docs process.

One of the important outs of the build process is a tag file. This is something that can be
pointed to by another documentation build for API interpolation and linking.

And this leads to the main snag of building from the existing docuentation.. options et all.
its easier to set up our own "template version" and then override some vars..


Indeed a lot of the build comments, and vital stuff is in the source..

So this project uses doxygen to automatically create documentation from source.

Doxygen is a pretty clever tool, and any kinda file can be read,
inc bllshit by forcing a java parser to extract a .frag or .vert file

-----------------------------------
How It works atmo
-----------------------------------
This is all in  a container project flightgear-docs-project
This is currently checked out on
* the Deleopers workstation
* A Hosting server with nginx
* A Lan Server behind firewall

The Docs umentation os split down into little parts such as

plib - this pulls the svn, copies a dpreperades config+content from etc, then builds
osg - Pulls the latest svn and generate tag file. This must be run before simgear for linking
simgear - Its a git external checkout from a custom branch and a custom build script, also tags to osg, plib





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





