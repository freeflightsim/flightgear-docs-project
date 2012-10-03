#!/usr/bin/env python


import os
import sys
import operator
from optparse import OptionParser
import shutil

import yaml
import simplejson as json

import git
import pysvn


## Handle Command Args
usage = "usage: %prog [options] show|build|clean|nuke proj1 proj2 .. projn"
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

V = opts.v
"""Verbose"""


if V > 2:
	print "========================================================="
	print "options=", opts, opts.v
	print "args=", args


if not opts.all and len(args) == 0:
	parser.error("Need to supply a command")
	sys.exit(0)

command = args[0]
if V > 1:
	print "#> command=", command

if not command in ['build', 'buildall', 'view', 'clean', 'nuke']:
	parser.error("Need a command")
	sys.exit(0)





## PATH constants - Please note these all have a TRAILING SLASH foo/
ROOT = os.path.abspath( os.path.dirname(__file__) ) + "/"
ETC = ROOT + "etc/"
TEMP = ROOT + "temp/"
BUILD = ROOT + "build/"
DEFAULT_DOXY = "doxy-default.conf"
INFO_JSON = "info.json"


#####################################################################################################	
def read_file(path_to_file):
	fob = open( path_to_file, "r")
	file_content = fob.read()
	fob.close()
	return file_content
	
def write_file(path_to_file, contents):
	fob = open( path_to_file, "w")
	fob.write(contents)
	fob.close()
	return
	
def write_info_file(proj, version, conf):
	dic = dict(color= conf['color'] if 'color' in conf else 'blue',
				version=version,
				title=conf['title'],
				project=proj
			)
	if proj == "fg-docs":
		fn = BUILD + INFO_JSON
	else:
		fn = BUILD + proj  +  "/" + INFO_JSON
	write_file(fn, json.dumps(dic) )
	
## Load Config
yaml_str = read_file( ROOT + "config.yaml" )
#print yaml_str
conf = yaml.load( yaml_str )


def make_projects_table():
	s = '<table id="projects_index">\n'
	s += "<tr>\n"
	s += "\t<th>Browse Html</th><th>Zip</th><th>Version</th><th>Updated</th><th>Repo</th><th>Checkout</th>"
	s += "\n</tr>\n"
	for proj in conf:
		pconf = conf[proj]
		is_main = proj == "fg-docs"
		js_filen =  BUILD + INFO_JSON if is_main else BUILD + proj + "/" + INFO_JSON
		data = None
		if os.path.exists(js_filen):
			json_str = read_file(js_filen)
			data = json.loads(json_str)
		print data
		#if c != "fg-docs":
		color = pconf['color'] if 'color' in pconf else "blue"
		version = data['version'] if data else pconf['version']['number']
		title = pconf['title']
		repo = pconf['repo']
		checkout = pconf['checkout']
		#v = conf[proj]
		s += '\n<tr>\n\t<td><a class="lnk" href="%s/" style="border-left: 10px solid %s;">' % (proj, color)
		s += '%s</a></td>' % (title)
		s += '\n<td><a target="_blank" href="%s/%s.zip">%s.zip</a></td>' % (proj, proj, proj)
		s += '\n<td>%s</td><td>%s</td>' % (version, "date")
		s += '\n<td>%s</td><td>%s</td>\n</tr>\n' % (repo, checkout)
	s += "</table>"
	return s

#####################################################################################################
def process_project(proj, pvals):
	if V > 0:
		print "---------------------------"
		print "# Processing: %s" % proj
	
	is_main = proj == "fg-docs"
	
	work_dir = TEMP + proj + "/"
	
	if is_main:
		build_dir = BUILD 
	else:
		build_dir = BUILD + proj + "/"
		
	##===========================================
	if V > 1:
		print "\tchecking if temp/work_dir exists: %s" % work_dir
	if not os.path.exists(work_dir):
		if V > 1:
			print "\t\tcreating temp/work_dir path: %s" % work_dir
		os.mkdir(work_dir)
	else:
		if V > 1:
			print "\t\tpath Exists temp/work_dir path: %s" % work_dir	
	
	##===========================================

		
	# nuke and recreate build:
	if not is_main:
		if V > 0:
			print "\t checking build directory exits: %s" % build_dir
		if os.path.exists(build_dir):
			if V > 1:
				print "\t nuking build directory: %s" % build_dir
			#shutil.rmtree(build_dir)
		if V > 1:
			print "\t creating build directory: %s" % build_dir
		
		#os.mkdir(build_dir)
	
	########################################################
	## Git Check
	if not is_main:
		
		if pvals['repo'] == "git":
		
			print "  > Checking is git repos at: %s" % work_dir + "/.git"
		
			#rep = git.Repo(work_dir)
			if not os.path.exists(work_dir + "/.git/"):
				#os.chdir(TEMP)
				print "Cloning new Repo"
				shutil.rmtree( work_dir )
				#print "work_dir=", work_dir
				#cmd = "git clone %s %s" % (pvals['git'], proj )
				#print "git clone= ", cmd
				#os.system(cmd)
				os.chdir(TEMP)
				g = git.Git( TEMP )
				g.clone(pvals['git'], proj)
			
			
			branch = pvals['branch'] if "branch" in pvals else "master"
			print "\t\t\tCheckout branch: %s" % branch
			g = git.Git( TEMP + proj)
			print g.checkout(branch)
			print g.pull()
		
		elif pvals['repo'] == "svn":
			
			if not os.path.exists(work_dir + "/.svn/"):
				print "Checkout out svn"
				svn = pysvn.Client()
				print pvals
				print svn.checkout( pvals['checkout'] , work_dir, recurse=True)
			else:
				print "SVN update"
				svn = pysvn.Client()
				svn.update( work_dir, recurse=True )
		#sys.exit(0)
		#print rep.is_dirty
		#print rep.git.status()
	else:
		pass
		## ITS MAIN, so make up the site
		#if os.path.exists(work_dir + "docx/"):
		#	shutil.rmtree(work_dir + "docx/")
		#os.mkdir(work_dir + "docx/")
		
		#shutil.copytree( ROOT + "docx/"  , work_dir + "docx"  )
		#shutil.copyfile( ROOT + "py_update.py", work_dir + "py_update.py")
		
	## Copy file
	if 'copy' in pvals:
		print pvals['copy']
		for f in pvals['copy']:
			source = ROOT + f
			head, tail = os.path.split(source)
			print "  > cp " + ROOT + f + " >> " +  work_dir + tail
			shutil.copyfile( ROOT + f, work_dir + tail)
	
	
	#print nav_str
	#sys.exit(0)
	
	#### copy required file
	if V > 0:
		print "> Copying build files:"
	for f in ["fg_xstyle.css"]:
		if V > 0:
			print ">   copied: %s" % f
		shutil.copyfile( ETC + f , work_dir + f )
	
	#### Make the page template ###
	## Create Navigation
	nav_str = ""
	if is_main:
		nav_str += '<li><a href="index.html">Home</a></li>\n'
	else:
		nav_str += '<li><a href="../">Home</a></li>\n' 
	link_prefix = "" if is_main else "../"
	for c in conf:
		if c != "fg-docs":
			nav_str += '<li><a href="%s%s/">%s</a></li>\n' % (link_prefix, c, c)
			
	template_header = read_file( ETC + "fg_docx_header.html" )
	template_header = template_header.replace("___NAV_ITEMS___", nav_str)
	write_file( work_dir + "fg_docx_header.html", template_header)
	
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
		dox_default = read_file(ETC + DEFAULT_DOXY)
		if V > 0:
			print "  > using default fg-docs file: etc/%s"  % DEFAULT_DOXY

	## Add the extra stuff doxy vars from config
	if V > 0:
		print "> Checking doxy vars from config.yaml"
	xover = []
	if 'doxy_args' in pvals: 
		for dox in pvals['doxy_args']:
			xover.append( "%s = %s" % (dox, pvals['doxy_args'][dox]) )
	else:
		if V > 0:
			print "  > No vars"
	
	if is_main:
		write_file(work_dir + "projects_index.html", make_projects_table())
	
	## Append and override the main settings from here
	xover.append('PROJECT_NAME="%s"' % proj)
	
	## get version no from yaml, or source file
	version = "-na-"
	if 'version' in pvals:
		if 'number' in pvals['version']:
			version = pvals['version']['number']
			
		elif 'file' in pvals['version']:
			version = read_file( work_dir + pvals['version']['file'] ).strip()
	xover.append('PROJECT_NUMBER="%s"' % version)
	xover.append('PROJECT_BRIEF="%s"' % pvals['title'])
		
	xover.append('OUTPUT_DIRECTORY=' + build_dir )
	xover.append('HTML_OUTPUT=%s' %  "./")
	xover.append('GENERATE_TAGFILE=' + build_dir + proj + ".tag")
	xover.append('HTML_HEADER = fg_docx_header.html')
	xover.append('HTML_EXTRA_STYLESHEET = "fg_xstyle.css"')
	dox_override = "\n".join(xover)
	
	if V > 0:
		print "> Overides for fg-docs output"
		for oo in xover:
			print "  > " + oo
	
	## make config string and write to file
	dox_config_str = dox_default + dox_override
	#print dox_config_str
	temp_doxy_file = "fg_temp_doxy.conf"
	temp_config_full_path = work_dir +  temp_doxy_file
	if os.path.exists( temp_config_full_path ):
		os.remove(temp_config_full_path)
	write_file( temp_config_full_path, dox_config_str)
	if V > 0:
		print "> Wrote temp doy file: %s" % temp_config_full_path
	
	print "\n> Compile: "
	os.chdir(work_dir)
	if V > 0:
		print "  > curdir: %s" % os.path.abspath( os.curdir )
	
	dox_cmd =  "doxygen ./%s " % temp_doxy_file 
	if V > 0:
		print "  > command: %s" % dox_cmd
	os.system( dox_cmd  )
	
	if V > 0:
		print "> Copying extra files:"
	for f in ["logo-23.png"]:
		if V > 0:
			print ">   copied: %s" % f
		shutil.copyfile( ETC + f , build_dir + f )
	
	## write info json
	write_info_file(proj, version, pvals)
	
	print "< Done: %s" % proj
	
	
	
#####################################################################################################


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

	
	


print "> Loaded config: %s" % " ".join( conf.keys() )

#############################################################
if command == "view":
	print yaml_str
	
	for c in conf:
		print "----------------------------"
		print c
		print conf[c]
	
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
	if not opts.all:
		for a in projects:
			if not a in conf:
				errs.append(a)
	if len(errs):
		print "Error: project%s not exist: %s" % ( "s" if len(errs) > 0 else "", ", ".join(errs))
		sys.exit(0)


	if opts.all:
		for proj in conf:
			print "proj", proj
	else:
		for proj in projects:
			process_project(proj, conf[proj])
	

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
	#		process_project(proj, conf[proj])
	#process_project("fg-docs", conf["fg-docs"])
	


