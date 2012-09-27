#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#

import sys
import datetime
import simplejson as json
from optparse import OptionParser

parser = OptionParser()
parser.add_option( "--out", dest="out",
                  help="dir to write out info.js to")
parser.add_option("--version",
                  dest="version",
                  help="file verion of build")
parser.add_option("--dir",
                  dest="dir",
                  help="directory of build")              
parser.add_option("--title",
                  dest="title",
                  help="title of project")   
parser.add_option("--git",
                  dest="git",
                  help="Git repos url")   
parser.add_option("--svn",
                  dest="svn",
                  help="SVN repos url")
parser.add_option("--color",
                  dest="color",
                  help="dex color")   
(options, args) = parser.parse_args()

#print options
#print args



if  options.out == None or options.dir == None or options.version == None or options.title == None or options.color == None:
	print "oops run with -h", 
	sys.exit(1)
if options.git == None and options.svn == None:
	print "neef git or svn"
	sys.exit(1)
	
repo = "git" if options.git else "svn"
checkout = options.git if options.git else options.svn

	
dic = dict(version=options.version,
			title=options.title,
			dir=options.dir,
			color=options.color,
			repo=repo, checkout=checkout,
			last_updated=datetime.datetime.strftime( datetime.datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
			)
			
json_str = json.dumps(dic)
f = open(options.out + "/info.json", "w")
f.write(json_str)
f.close()

print "json=", json_str
	