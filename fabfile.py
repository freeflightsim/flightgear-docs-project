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
import fgdocx.helpers as _h

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


def plib():
	"""plib build docs"""
	projObj = _ProjectBuilder(conf, "plib")
	with lcd(projObj.wd()):
		projObj.prepare()
		local( projObj.get_build_cmd() )
		projObj.post_build()

def osg():
	"""OpenSceneGraph build docs"""
	projObj = _ProjectBuilder(conf, "osg")
	with lcd(projObj.wd()):
		projObj.prepare()
		local( projObj.get_build_cmd() )
		projObj.post_build()



def sg():
	"""simgear docs build"""
	projObj = _ProjectBuilder(conf, "simgear")
	with lcd(projObj.wd()):
		local("git pull")
		projObj.prepare()
		local( projObj.get_build_cmd() )
		projObj.post_build()
		
def tg():
	"""TerraGear docs build"""
	projObj = _ProjectBuilder(conf, "terragear")
	with lcd(projObj.wd()):
		projObj.prepare()
		local( projObj.get_build_cmd() )
		projObj.post_build()

def fg():
	"""flightgear docs build"""
	projObj = _ProjectBuilder(conf, "flightgear")
	with lcd(projObj.wd()):
		local("git pull")

		projObj.prepare()
		local( projObj.get_build_cmd() )
		projObj.post_build()

def index():
	"""Updates Main webpages ie fgdocx  build after others"""
	projObj = _ProjectBuilder(conf, "fgdocx")
	with lcd(projObj.wd()):
		projObj.prepare()
		local( projObj.get_build_cmd() )
		projObj.post_build()

def site():
	local("cp %s %s" % (conf.ETC + "robots.txt", conf.BUILD))
	local("cp %s %s" % (conf.ETC + "logo-23.png", conf.BUILD))
	local("cp %s %s" % (conf.ETC + "favicon.ico", conf.BUILD))

def sitemap():
	s = '<?xml version="1.0" encoding="utf-8"?>\n'
	s += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
	s += "\t<url>\n"
	s += "\t\t<loc>http://api-docs.freeflightsim.org</loc>\n"
	s += "\t\t<changefreq>daily</changefreq>\n"
	s += "\t\t<priority>0.2</priority>\n"
	s += "\t</url>\n"
	for page in conf.get_projects_list():
		#print page
		s  += "\t<url>\n"
		s  += "\t\t<loc>http://api-docs.freeflightsim.org/%s/</loc>\n" % page['proj']
		s  += "\t\t<lastmod>{{ site.time | date_to_xmlschema }}</lastmod>\n"
		s  += "\t\t<changefreq>daily</changefreq>\n"
		s  += "\t\t<priority>0.3</priority>\n"
		s += "\t</url>\n"

	s += "</urlset>\n"
	#print s
	#print conf.BUILD + "sitemap.xml"
	_h.write_file(conf.BUILD + "sitemap.xml", s)

def all():
	"""Build all"""
	plib()
	osg()
	sg()
	tg()
	fg()
	site()
	sitemap()
