#!/usr/bin/env python


import os
import sys
from optparse import OptionParser
import shutil
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
def process_project(proj, pvals):
	if V > 0:
		print "---------------------------"
		print "# Processing: %s" % proj
	
	is_main = proj == "fg-docs"
	
	if is_main:
		work_dir = ROOT + ""
	else:
		work_dir = TEMP + proj + "/"
	
	##===========================================
	
	if not is_main: 
		git_exists = False
		if V > 1:
			print "\tchecking if temp/work_dir exists: %s" % work_dir
		if not os.path.exists(work_dir):
			if V > 1:
				print "\t\tcreating temp/work_dir path: %s" % work_dir
				#os.mkdir(work_dir)
		else:
			if V > 1:
				print "\t\tpath Exists temp/work_dir path: %s" % work_dir	
	
	##===========================================
	build_dir = BUILD + proj + "/"
	# nuke and recreate build:
	if V > 0:
		print "\t checking build directory exits: %s" % build_dir
	if os.path.exists(build_dir):
		if V > 1:
			print "\t nuking build directory: %s" % build_dir
		shutil.rmtree(build_dir)
	if V > 1:
		print "\t creating build directory: %s" % build_dir
	os.mkdir(build_dir)
	
	########################################################
	## Git Check
	if not is_main:
		print "\t\tChecking is git repos at: %s" % work_dir
		
		#rep = git.Repo(work_dir)
		if not os.path.exists(TEMP + proj):
			#os.chdir(TEMP)
			print "Cloning new Repo"
			#print "work_dir=", work_dir
			#cmd = "git clone %s %s" % (pvals['git'], proj )
			#print "git clone= ", cmd
			#os.system(cmd)
			g = git.Git( TEMP )
			g.clone(pvals['git'], proj)
		
		
		branch = pvals['branch'] if "branch" in pvals else "master"
		print "\t\t\tCheckout branch: %s" % branch
		g = git.Git( TEMP + proj)
		print g.checkout(branch)
		print g.pull()
		
		#print rep.is_dirty
		#print rep.git.status()
		
	## copy the templates
	if V > 0:
		print "> Copying essential files:"
	for f in ["fg_docx_header.html", "logo-23.png"]:
		if V > 0:
			print ">   copied: %s" % f
		shutil.copyfile( ROOT + "etc/" + f , work_dir + f )
	
	##############################################
	## Create temp doxy string and write to file
	
	## READ default
	if V > 0:
		print "> Checking doxy file"
	if 'doxy_file' in pvals and pvals['doxy_file']:
		if V > 0:
			print "  > using %s project doxy file: %s" % (proj, pvals['doxy_file'])
		dox_default = read_file(work_dir + pvals['doxy_file'])
		
	else:
		dox_default = read_file(ETC + "default-doxy.conf")
		if V > 0:
			print "  > using default fg-docs file: etc/default-doxy.conf" 

	## Add the extra stuff doxy vars from config
	if V > 0:
		print "> Checking doxy vars from config.yaml"
	xover = []
	if 'doxy' in pvals: 
		for dox in vals['doxy']:
			xover.append( "%s = %s" % (dox, pvals['doxy'][dox]) )
	else:
		if V > 0:
			print "  > No vars"
	
	## Append and override the main settings from here
	xover.append("PROJECT_NAME=%s" % proj)
	
	## get version no from yaml, or source file
	version = "-na-"
	if 'version' in pvals:
		if 'no' in pvals['version']:
			version = pvals['version']['no']
			
		elif 'file' in pvals['version']:
			version = read_file( work_dir + pvals['version']['file'] ).strip()
	xover.append("PROJECT_NUMBER=%s" % version)
	xover.append("PROJECT_BRIEF=%s" % pvals['title'])
		
	xover.append("OUTPUT_DIRECTORY=" + build_dir )
	xover.append("HTML_OUTPUT=%s" %  "./")
	xover.append("GENERATE_TAGFILE=" + build_dir + proj + ".tag")
	dox_override = "\n".join(xover)
	
	if V > 0:
		print "> Overides for fg-docs output"
		for oo in xover:
			print "  > " + oo
	
	## make config string and write to file
	dox_config_str = dox_default + dox_override
	temp_doxy_file = "_fg_temp_doxy.conf"
	temp_config_full_path = work_dir +  temp_doxy_file
	fwrite = open(temp_config_full_path, "w")
	fwrite.write(dox_config_str)
	fwrite.close()
	if V > 0:
		print "> Wrote temp doy file: %s" % temp_config_full_path
	
	
	os.chdir(work_dir)
	print "curdir", os.path.abspath( os.curdir )
	dox_cmd =  "doxygen %s " % temp_doxy_file 
	print "dox_cmd=", dox_cmd
	os.system( "doxygen ./%s " % temp_doxy_file  )
	
	
	print "\t\t Done: %s" % proj
	
#####################################################################################################
## Load Config
yaml_str = read_file( ROOT + "config.yaml" )
#print yaml_str
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
	




