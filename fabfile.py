## Visit api-docs.freeflightsim.org
# maintainer pete@freeflightsim.org
#
# Checkouts all the flightgear repos and uses doxygen to compile docs
# this is serielised to a build directory = static html = website
#
# Notes
# the only active changes are epected to be simgear + flightgear
# the whole build is done every two hours or so
import sys
import os
import yaml

from fabric.api import env, local, run, cd, lcd, sudo, warn_only

from fgdocx.project import ProjectBuilder
from fgdocx.config import Config

ROOT = "/home/fg/flightgear-docs-project"
ETC = 	ROOT + "/etc"
TEMP = ROOT + "/temp"

FG = TEMP + "/flightgear"
SG = TEMP + "/simgear"
FGDATA = TEMP + "/fgdata"
OSG = TEMP + "/osg"

## Read a text file and return its contents
def read_file(path_to_file):
    fob = open( path_to_file, "r")
    file_content = fob.read()
    fob.close()
    return file_content

## Write text string to file path
def write_file(path_to_file, contents):
    fob = open( path_to_file, "w")
    fob.write(contents)
    fob.close()
    return

conf = Config(1)
		
#conf = yaml.load( read_file( ETC + "/projects.config.yaml" ) )
#print conf.keys()


def checkoutall():
	with lcd(TEMP):
		local("git clone git://gitorious.org/fg/simgear.git")
		local("git clone git://gitorious.org/fg/flightgear.git")
		local("svn co https://plib.svn.sourceforge.net/svnroot/plib/trunk plib")
		

def osg():
	with lcd(OSG):
		local("cp %s/%s, %s" % (ETC, "DoxyMain-osg.cpp", TEMP + "/osg/" + "DoxyMain-osg.cpp"))
		



def sg():
	projConf = conf.get_project_config_object("simgear")
	projObj = ProjectBuilder(conf, projConf)
	projObj.prepare()
	projObj.build()
	#p# = ProjectBuilder( "simgear", conf)
	#p.prepare()
	with lcd(SG):
		pass
		#local("git pull")
		
def plib():
	projConf = conf.get_project_config_object("plib")
	projObj = ProjectBuilder(conf, projConf)
	projObj.prepare()
	projObj.build()
	#p# = ProjectBuilder( "simgear", conf)
	#p.prepare()
	with lcd(SG):
		pass
		#local("git pull")
		


def fgdata_status():
	with lcd(FGDATA):
		out = local("git diff --raw origin/master ")
		
		print "out=", out
		return out
	
	
def status():
	
	ok = fgdata_status()
	print "ok", ok
