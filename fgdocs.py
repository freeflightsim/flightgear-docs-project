#!/usr/bin/env python


## @package fgdocs
# This script does all the handling of the docs build process
#
# @author Pete Morgan 
# @version 0.1
# 


import os
import sys
import operator
import datetime
from optparse import OptionParser
import shutil

import yaml
import simplejson as json

import git
import pysvn


from fgdocs.config import Config
from fgdocs.project import Project


## Handle Command Args
usage = "usage: %prog [options] COMMAND proj1 proj2 .. projn\n"
usage += "    commands are\n"
usage += "       view  - to view the config\n"
usage += "       build proj1 proj2 - Build one or more projects\n"
usage += "       buildall - Build all projects\n"
parser = OptionParser(usage=usage)
parser.add_option(	"-z", "--zip", 
					action="store_false", dest="zip", default=False, 
					help="Create zip file"
					)            
parser.add_option(	"-v", "--verbose", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()

## Verbose
V = opts.v



if V > 2:
	print "========================================================="
	print "options=", opts, opts.v
	print "args=", args


if len(args) == 0:
	parser.error("Need to supply a command")
	#parser.print_help()
	sys.exit(0)

## The command executed is the first var
command = args[0]
if V > 1:
	print "#> command=", command

if not command in ['build', 'buildall', 'view', 'clean', 'nuke']:
	parser.error("Need a command")
	sys.exit(0)








## Write out json encoded info file to \ref INFO_JSON_FILE
#  @param proj the project dir
#  @param version the version
#  @param conf the yaml config file
def write_info_file(proj, version, conf):
	dic = dict(color= conf['color'] if 'color' in conf else 'blue',
				version=version,
				title=conf['title'],
				project=proj,
				date_updated=datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y-%m-%d %H:%M:%S")
			)
	if proj == "fg-docs":
		fn = BUILD + INFO_JSON_FILE
	else:
		fn = BUILD + proj  +  "/" + INFO_JSON_FILE
	write_file(fn, json.dumps(dic) )

##############################################################################





		
		
"""
##print yaml_str
yaml_str = read_file( ROOT + CONFIG_FILE )
conf = yaml.load( yaml_str )
"""


	
## Get the projects index as a list of dicts. This loops thru the projects and reads the INFO_JSON_FILE_FILE
def get_projects_index():
	ret = []
	for proj in sorted(conf.keys()):
		pconf = conf[proj]
		is_main = proj == "fg-docs"
		js_filen =  BUILD + INFO_JSON_FILE if is_main else BUILD + proj + "/" + INFO_JSON_FILE
		data = None
		if os.path.exists(js_filen):
			json_str = read_file(js_filen)
			data = json.loads(json_str)
		print data
		#if c != "fg-docs":
		p = XObject()
		p.proj = proj
		p.color = pconf['color'] if 'color' in pconf else "blue"
		p.version = data['version'] if data else pconf['version']['number']
		p.title = pconf['title']
		p.repo = pconf['repo']
		p.checkout = pconf['checkout']
		p.date_updated = data["date_updated"] if "date_updated" in data else ""
		ret.append( p )
	return ret



	
def make_projects_pages_cpp():
	projects = get_projects_index()
	
	l = []
	for p in projects:
		
		l.append( " * \section project_%s %s" % (p.proj, p.title) )
		l.append( " * - Version: \b%s" % p.version)
		l.append( " * - repo: \b%s" % p.repo)
		l.append( " * - checkout: \b%s" % p.checkout)
		l.append( " *")
	s = "/**\n * \page Projects Projects\n *\n"
	s += "\n".join(l)
	s += "/\n"
	print s
	return s
	
	
	
	
	
	
	
#####################################################################################################

##
conf = Config(verbose=V)

print "> ROOT: %s" % conf.ROOT


## Create temp and build dirs
if not os.path.exists(conf.TEMP):
	if V > 0:
		print "\t\t Created working dir: temp/"
	os.mkdir(conf.TEMP)

if not os.path.exists(conf.BUILD):
	if V > 0:
		print "\t\t Created working dir: build/"
	os.mkdir(conf.BUILD)	

	
	




#############################################################
if command == "view":
	conf.print_view(True)
	conf.print_view()
	sys.exit(0)

if command == "clean":
	shutil.rmtree(BUILD)
	print "> Nuked build: %s" % BUILD
	sys.exit(0)
	
#############################################################	
if command == "build":
	projects = args[1:]
	print projects
	## Check that the project args are in config
	errs = []
	for a in projects:
		if not conf.has_project(a):
			errs.append(a)
	if len(errs):
		print "Error: project%s not exist: %s" % ( "s" if len(errs) > 0 else "", ", ".join(errs))
		sys.exit(0)

	for proj in projects:
		projObj = Project( conf.project(proj) )
		projObj.build_project()
	

if command == "buildall":
	
	ulist = []
	for proj in conf:
		dic = conf[proj]
		dic['runlevel'] = int(dic['runlevel']) if  'runlevel' in dic else 0
		dic['proj'] = proj
		ulist.append(dic)
	compile_list = sorted(ulist, key=operator.itemgetter('runlevel'))	
	for p in compile_list:
		print p['proj'] , p['runlevel']
	
	#for proj in conf:
	#	if proj != "fg-docs":
	#		build_project(proj, conf[proj])
	#build_project("fg-docs", conf["fg-docs"])
	


