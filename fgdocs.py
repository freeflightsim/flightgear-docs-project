#!/usr/bin/env python


## @package fgdocs
# This script does all the handling of the docs build process
#
# @author Pete Morgan 
# @version 0.1
# 


import os

from optparse import OptionParser





from fgdocs.builder import DocsBuilder


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


docsBuilder = DocsBuilder(parser, opts, args)














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
#conf = Config(verbose=V)

#print "> ROOT: %s" % conf.ROOT



	
	





	


	
	#for proj in conf:
	#	if proj != "fg-docs":
	#		build_project(proj, conf[proj])
	#build_project("fg-docs", conf["fg-docs"])
	


