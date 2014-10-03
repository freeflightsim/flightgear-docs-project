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

from fgdocx.project import ProjectBuilder as _ProjectBuilder
from fgdocx.config import Config as _Config

"""
ROOT = "/home/fg/flightgear-docs-project"
ETC = 	ROOT + "/etc"
TEMP = ROOT + "/temp"

FG = TEMP + "/flightgear"
SG = TEMP + "/simgear"
FGDATA = TEMP + "/fgdata"
OSG = TEMP + "/osg"
"""

conf = _Config(1)



def checkoutall():
	with lcd(conf.TEMP):
		local("svn co http://www.openscenegraph.org/svn/osg/OpenSceneGraph/tags/OpenSceneGraph-3.2.1 osg")
		local("git clone git://gitorious.org/fg/simgear.git")
		local("git clone git://gitorious.org/fg/flightgear.git")
		local("svn co https://svn.code.sf.net/p/plib/code/trunk plib")
		

def osg():
	projObj = _ProjectBuilder(conf, "osg")
	with lcd(projObj.wd()):
		projObj.prepare()
		local( projObj.get_build_cmd() )
		



def sg():
	"""simgear docs build"""
	projObj = _ProjectBuilder(conf, "simgear")
	with lcd(projObj.wd()):
		local("git pull")
		projObj.prepare()
		local( projObj.get_build_cmd() )
		
def tg():
	"""TerraGear docs build"""
	projObj = _ProjectBuilder(conf, "terragear")
	with lcd(projObj.wd()):
		projObj.prepare()
		local( projObj.get_build_cmd() )
		

def fg():
	"""flightgear docs build"""
	projObj = _ProjectBuilder(conf, "flightgear")
	with lcd(projObj.wd()):
		local("git pull")

		projObj.prepare()
		local( projObj.get_build_cmd() )


def www():
	"""Updates Main webpages ie fgdocx  build"""
	projObj = _ProjectBuilder(conf, "fgdocx")
	with lcd(projObj.wd()):


		projObj.prepare()
		local( projObj.get_build_cmd() )
