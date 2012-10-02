#!/usr/bin/env python


import os
import sys
from optparse import OptionParser
import yaml
import git

## Handle Command Args
usage = "usage: %prog [options] prog1 prog2 .. progN"
parser = OptionParser(usage=usage)
parser.add_option(	"-a", "--all", 
					action="store_true", dest="all", default=False, 
					help="Generate all builds"
					)
parser.add_option(	"-z", "--zip", 
					action="store_false", dest="zip", default=False, 
					help="Create zip file"
					)            
parser.add_option(	"-v", "--verbose", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()

print "========================================================="
print "options=", opts, opts.v
print "args=", args


if not opts.all and len(args) == 0:
	parser.error("Error: need to supply a list of repo, or all")
	sys.exit(0)
	
	
############################################################################
print "---------------"

V = opts.v

## PATH constants 
## - Please note these all have a TRAILING SLASH foo/
ROOT = os.path.abspath( os.path.dirname(__file__) ) + "/"
ETC = ROOT + "etc/"
TEMP = ROOT + "temp/"
BUILD = ROOT + "build/"


print "> ROOT: %s" % ROOT


## Create temp and build dirs
if not os.path.exists(TEMP):
	if V > 0:
		print "\t\t Created working dir: temp/"
	os.mkdir(TEMP)

if not os.path.exists(BUILD):
	if V > 0:
		print "\t\t Created working dir: build/"
	os.mkdir(BUILD)	

	
def read_file(path_to_file):
	fob = open( path_to_file, "r")
	file_content = fob.read()
	fob.close()
	return file_content
	

#####################################################################################################
def process_project(proj, vals):
	if V > 0:
		print "\t Processing: %s" % proj
	
	is_main = proj == "fg-docs"
	
	if is_main:
		work_dir = ""
	else:
		work_dir = TEMP + proj
	
	git_exists = False
	if not is_main: 
		print "\t\tChecking if temp/work_dir exists: %s" % work_dir
		if not os.path.exists(work_dir):
			print "\t\t\tCreating temp/work_dir path: %s" % work_dir
			os.mkdir(work_dir)
		else:
			print "\t\t\tPath Exists temp/work_dir path: %s" % work_dir	
	
	#print "\t\tChecking is git repos at: %s" % pth
	
	
	## READ default
	dox_default = read_file(ETC + "fg_doxy.conf")

	## Add the extra stuff doxy vars from config
	xover = []
	for dox in vals['doxy']:
		#print dox, vals['doxy'][dox]
		xover.append( "%s = %s" % (dox, vals['doxy'][dox]) )
	
	## Append and override the main settings
	xover.append("PROJECT_NAME=%s" % proj)
	xover.append("PROJECT_NUMBER=%s" % vals['version'])
	xover.append("PROJECT_BRIEF=%s" % vals['title'])
	
	xover.append("OUTPUT_DIRECTORY=" + BUILD + proj + "/")
	xover.append("HTML_DIRECTORY=%s" % "/")
	
	
	dox_override = "\n".join(xover)
	print dox_override
	dox_config_str = dox_default + dox_override
	
	temp_doxy_file = "_fg_temp_doxy.conf"
	temp_config_full_path = "%s/%s" % (work_dir, temp_doxy_file)
	print "temp_config_full_path=%s" % temp_config_full_path
	fwrite = open(temp_config_full_path, "w")
	fwrite.write(dox_config_str)
	fwrite.close()
	
	
	print "work_dir=", work_dir
	os.chdir(work_dir)
	print "curdir", os.path.abspath( os.curdir )
	dox_cmd =  "doxygen %s " % temp_doxy_file 
	print "dox_cmd=", dox_cmd
	os.system( "doxygen ./%s " % temp_doxy_file  )
	
	
	print "\t\t Done: %s" % proj
	
#####################################################################################################
## Load Config
yaml_str = read_file( ROOT + "config.yaml" )
print yaml_str
conf = yaml.load( yaml_str )

print "> Loaded config: %s" % " ".join( conf.keys() )


## Check that the project args are in config
errs = []
if not opts.all:
	for a in args:
		if not a in conf:
			errs.append(a)
if len(errs):
	print "Error: project%s not exist: %s" % ( "s" if len(errs) > 0 else "", ", ".join(errs))
	sys.exit(0)


if opts.all:
	for proj in conf:
		print "proj", proj
else:
	for proj in args:
		process_project(proj, conf[proj])
	




