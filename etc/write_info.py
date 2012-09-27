#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#

import sys
import datetime
import simplejson as json
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-o", "--out", dest="out",
                  help="dir to write out info.js to")
parser.add_option("-v", "--version",
                  dest="version",
                  help="file verion of build")
parser.add_option("-d", "--dir",
                  dest="dir",
                  help="directory of build")              
parser.add_option("-t", "--title",
                  dest="title",
                  help="title of project")   
(options, args) = parser.parse_args()

print options
print args



if  options.out == None or options.dir == None or options.version == None or options.title == None:
	print "oops", 
	sys.exit(1)
else:
	
	dic = dict(version=options.version,
				title=options.title,
				dir=options.dir,
				last_updated=datetime.datetime.strftime(, datetime.datetime.utcnow(), "%Y-%m-%d- %H%M%S")
				)
				
	json_str = json.dumps(dic)
	f = open(options.out + "/info.json", "w")
	f.write(json_str)
	f.close()
	