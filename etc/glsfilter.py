#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#

# Copyright notice: 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import getopt          # get command-line options
import os.path         # getting extension from file
import string          # string manipulation
import sys             # output and stuff
import re              # for regular expressions


## extract doxygen-tag class
re_doxy_class = re.compile('(?<=[@]class\s)\w+', re.I | re.VERBOSE)
## extract doxygen-tag namespace
re_doxy_namespace = re.compile('(?<=[@]namespace\s)[^\s]+', re.I | re.VERBOSE)
re_blockcode_start = re.compile('(?<=[\*]class\s)\w+', re.I | re.VERBOSE)

##
# @package glslfilter
# @brief A Doxygen filter to document GLSL-Shader, based on a vb-filter from Basti Grembowietz
# @author Sebastian SchÃ¤fer
# @date 02/2012
# @version 0.1
# @copyright GNU Public License.
# 
# @details The shader file is wrapped into a class and namespace that can be set with 
# doxygen-tags.
# 
# Usage:
# - shader file:
#   - set doxygen name for class name -> defaults to filename
#   - set doxygen namespace for namespace (pseudo category) -> defaults to GLSL
# - doxygen file:
#   - add FILE_PATTERNS: *.frag, *.vert
#   - add FILTER_PATTERNS: "*.frag=glslfilter.py", "*.vert=glslfilter.py"
# latest version on <a href="http://www.grasmo.de">www.grasmo.de</a>

##run regex on a single line
# @returns either a found result or None
def getRegSearchLine(str, regex):
	search = regex.search(str)
	if search is not None:
		return search.group(0)
	return None

##run regex on an string array
# @returns either a found result or None
def getRegSearch(txt, regex):
	for str in txt:
		search = regex.search(str)
		if search is not None:
			return search.group(0)
	return None

# generate a class name from filename
# @return just the filename - no extension and no path
def generateName(filename):
	root, ext = os.path.splitext(filename)
	head, tail = os.path.split(root)
	return tail
	
def writeLine(txt):
	sys.stdout.write(txt + "\n")
	
## parse a shader and generate needed information along on the way
## - if comments contain a namespace move it the classname
def parseShader(filename, txt, type = None):
	# extract name from doxygen-tag or use generic GLSL namespace
	namespace = getRegSearch(txt, re_doxy_namespace)
	if namespace is None:
		namespace = "GLSL"
	else:
		#remove namespace line from txt
		txt = [str for str in txt if getRegSearchLine(str, re_doxy_namespace) is None]

	# extract className from doxygen-tag or use filename
	className = getRegSearch(txt, re_doxy_class)
	if className is None:
		className = generateName(filename)
	else:
		#remove calssName line from txt
		txt = [str for str in txt if getRegSearchLine(str, re_doxy_class) is None]
	
	comment = []
	if len(txt) > 0:
		if txt[0].find("/*") >=0:
			line = txt.pop(0)
			while (line.find("*/") < 0) and (len(txt) > 0):
				comment.append(line)
				line = txt.pop(0)
			comment.append(line)
				
	

	# dump the file and pad it with namespace/name class information
	# 1st: namespace + class padding, also declare everything public
	writeLine("/** @namespace " + namespace + " */")
	writeLine("public class " + namespace+"::"+className + "{")
	writeLine("public:")
	# 2nd: dump original commentblock
	showLines(comment)
	# 3rd: add type-remark and classname
	if type is not None:
		writeLine("/** @remark <b>" + type + "</b> */")
	writeLine("/** @class " + namespace+"::"+className + " */")
	# 4th: dump remaining file 
	showLines(txt)
	# 5th: close dummy class
	writeLine("}")

## @returns the complete file content as an array of lines
def readFile(filename):
	f = open(filename)
	r = f.readlines()
	f.close()
	return r
	
## dump all lines to stdout
def showLines(r):
	for s in r:
		sys.stdout.write(s)
		
## main method - open a file and see what can be done
def filter(filename):
	try:
		root, ext = os.path.splitext(filename)
		txt = readFile(filename)
		if (ext.lower() == ".frag"):
			parseShader(filename, txt, "Fragment-Shader")
		elif (ext.lower() == ".vert"):
			parseShader(filename, txt, "Vertex-Shader")
		else:
			showLines(txt)
	except IOError,e:
		sys.stderr.write(e[1]+"\n")

if len(sys.argv) != 2:
	print "usage: ", sys.argv[0], " filename"
	sys.exit(1)

filename = sys.argv[1] 
filter(filename)
sys.exit(0)
