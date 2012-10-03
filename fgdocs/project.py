## @package fgdocs


import os
import sys
import datetime

import json
import shutil
import git
import pysvn

import helpers as h

## Builds a project
class ProjectBuilder:
	
	## Initialze the project builder from configs
	# @param mainConf - a config.Config instance
	# @param projObj - a config.ProjectConfig instance
	# @param verbose - verbosity of output
	def __init__(self, mainConf, projObj, verbose=1):
		
		## Verbosity 0-4
		self.V = verbose
		
		## Config object
		self.main_conf = mainConf
		
		## ProjectConfig  object
		self.conf = projObj 
		
	## Prepare the project, copying files, setting up doxy etc    
	def prepare(self):
		if self.V > 0:
			print "---------------------------"
			print "# Processing: %s" % self.conf.proj
				
		##===========================================
		if self.V > 1:
			print "\tchecking if temp/work_dir exists: %s" % self.conf.work_dir
		if not os.path.exists(self.conf.work_dir):
			if self.V > 1:
				print "\t\tcreating temp/work_dir path: %s" % self.conf.work_dir
			os.mkdir(self.conf.work_dir)
		else:
			if self.V > 1:
				print "\t\tpath Exists temp/work_dir path: %s" % self.conf.work_dir    
		
		##===========================================
	
			
		# nuke and recreate build:
		if not self.conf.is_main:
			if self.V > 0:
				print "\t checking build directory exits: %s" % self.conf.build_dir
			if os.path.exists(self.conf.build_dir):
				if self.V > 1:
					print "\t nuking build directory: %s" % self.conf.build_dir
				#shutil.rmtree(build_dir)
			if self.V > 1:
				print "\t creating build directory: %s" % self.conf.build_dir
			
			#os.mkdir(build_dir)
		
		########################################################
		## Git Check
		if self.conf.is_main:
			pass
			
		else:
			
			if self.conf.is_git:
				self.process_git()
				
			elif self.conf.is_svn:
				self.process_svn()


			
		## Copy file 
		# @ see copy_config
		self.copy_files()
		
		#print nav_str
		#sys.exit(0)
		
		#### copy required file
		if self.V > 0:
			print "> Copying build files:"
		for f in ["fg_xstyle.css", "fg_docx_footer.html"]:
			if self.V > 0:
				print ">   copied: %s" % f
			shutil.copyfile( self.conf.ETC + f , self.conf.work_dir + f )
		
		self.write_header_html()   
		
		##############################################
		## Create temp doxy string and write to file
		
		## READ default
		dox_file_contents = self.get_doxy_file()
	
		## Add the extra stuff doxy vars from config
		if self.V > 0:
			print "> Checking doxy vars from config.yaml"
			
		
		xover = self.get_doxy_args()
		
		## MAIN project extras
		if self.conf.is_main:
			h.write_file(self.conf.work_dir + "projects_index.html", self.get_projects_table_html())
			h.write_file( self.conf.work_dir + "project_pages.cpp",  self.get_projects_pages_cpp())
			
		## Append and override the main settings from here
		xover.append('PROJECT_NAME="%s"' % self.conf.proj)
		
		## get version no from yaml, or source file
		self.version = self.get_version()     
				
		xover.append('PROJECT_NUMBER="%s"' % self.version)
		xover.append('PROJECT_BRIEF="%s"' % self.conf.title)
			
		xover.append('OUTPUT_DIRECTORY=' + self.conf.build_dir )
		xover.append('HTML_OUTPUT=%s' %  "./")
		xover.append('GENERATE_TAGFILE=' + self.conf.build_dir + self.conf.proj + ".tag")
		xover.append('HTML_HEADER = fg_docx_header.html')
		xover.append('HTML_FOOTER = fg_docx_footer.html')
		xover.append('HTML_EXTRA_STYLESHEET = "fg_xstyle.css"')
		xover.append('TREEVIEW_WIDTH = 120')
		#xover.append('FILTER_SOURCE_FILES: YES')
		py_processor =  self.conf.ETC + "doxypy.py"
		xover.append( 'FILTER_PATTERNS = "*.py=%s"' % py_processor )
		#xover.append('INPUT_FILTER: "%sdoxypy.py" ' % self.conf.ROOT)
	
		if self.conf.tags:
			tag_list = []
			for t in self.conf.tags:
				tag_list.append( self.conf.BUILD + t + "/" + t + ".tag=../" + t  )
			xover.append("TAGFILES = %s \n" % " ".join(tag_list) )
		
		dox_override = "\n".join(xover)
		
		if self.V > 0:
			print "> Overides for fg-docs output"
			for oo in xover:
				print "  > " + oo
		
		## make config string and write to file
		dox_config_str = dox_file_contents + dox_override
		#print dox_config_str
		self.write_temp_doxy(dox_config_str)
		
	def build(self):
		print "\n> Compile: "
		os.chdir(self.conf.work_dir)
		if self.V > 0:
			print "  > curdir: %s" % os.path.abspath( os.curdir )
		
		dox_cmd =  "doxygen ./%s " % self.conf.TEMP_DOXY
		if self.V > 0:
			print "  > command: %s" % dox_cmd
		os.system( dox_cmd  )
		
		if self.V > 0:
			print "> Copying extra files:"
		for f in ["logo-23.png"]:
			if self.V > 0:
				print ">   copied: %s" % f
			shutil.copyfile( self.conf.ETC + f , self.conf.build_dir + f )
		
		## write info json
		self.write_info_file()
		
		print "< Done: %s" % self.conf.proj


	def process_svn(self):
			
		if not os.path.exists(self.conf.work_dir + "/.svn/"):
			self.svn_checkout()
		else:
			self.svn_update()
			
	def svn_checkout(self):
		print "Checkout out svn"
		svn = pysvn.Client()
	
		print svn.checkout( self.conf.checkout  , self.conf.work_dir, recurse=True)
	
	def svn_update(self):
		
		print "SVN update"
		svn = pysvn.Client()
		svn.update( self.conf.work_dir, recurse=True )
					
	## Process this project is its git
	def process_git(self):
		print "  > Checking is git repos at: %s" % self.conf.work_dir + "/.git"       
		if not os.path.exists(self.conf.work_dir + "/.git/"):
			#os.chdir(TEMP)
			self.git_clone()
					
	## Clones a git repository
	# @see \ref repo_config
	# @see \ref checkout_config
	def git_clone(self):
		if self.V > 0:
			print "Cloning new Repo: %s" % self.conf.checkout
		shutil.rmtree( self.conf.work_dir )
		os.chdir( self.conf.TEMP )
		g = git.Git( self.conf.TEMP )
		g.clone(self.conf.checkout, self.conf.proj)
			
	## Pulls latest git
	# @see \ref repo_config
	# @see \ref branch_config
	def git_pull(self):
		if self.V > 0:
			print "  > Pull and checkout branch: %s" % branch
		g = git.Git( self.conf.work_dir )
		print g.checkout(self.conf.branch)
		print g.pull()
				
	## Copies the files and paths in \ref copy_config
	def copy_files(self):
		if self.conf.copy:
			print self.conf.copy 
			for f in self.conf.copy:
				source = self.conf.ROOT + f
				
				
				if os.path.isdir(source):
					target = self.conf.work_dir + f
					if os.path.exists(target):
						shutil.rmtree(target)
					shutil.copytree( source, target)
				else:
					
					head, tail = os.path.split(source)
					target = self.conf.work_dir + tail
					print "  > cp " + source + " >> " +  target
					
					shutil.copyfile( self.conf.ROOT + f, target)
		
	## Top navigation list
	# @return str Hmtl nav list
	def get_navigation(self):
		nav_str = ""
		if self.conf.is_main:
			nav_str += '<li><a href="index.html">Home</a></li>\n'
		else:
			nav_str += '<li><a href="../">Home</a></li>\n' 
		link_prefix = "" if self.conf.is_main else "../"
		for p in self.main_conf.get_projects_index():
			if not p.is_main:
				nav_str += '<li><a href="%s%s/">%s</a></li>\n' % (link_prefix, p.proj, p.abbrev)
	
		return nav_str
	
	## Writes out the html header file
	def write_header_html(self):
		
		template_header = h.read_file( self.conf.ETC + "fg_docx_header.html" )
		template_header = template_header.replace("___NAV_ITEMS___", self.get_navigation() )
		h.write_file( self.conf.work_dir + "fg_docx_header.html", template_header)
	
	## Return the contents of the doxy file  
	def get_doxy_file(self):
		if self.V > 0:
			print "> Checking doxy file"
		if self.conf.doxy_file:
			if self.V > 0:
				print "  > using %s project doxy file: %s" % (self.conf.proj, self.conf.doxy_file)
			dox_contents = h.read_file(self.conf.work_dir + self.conf.doxy_file)
			
		else:
			dox_contents = h.read_file(self.conf.ETC + self.conf.DEFAULT_DOXY)
			if self.V > 0:
				print "  > using default fg-docs file: etc/%s"  % self.conf.DEFAULT_DOXY
		return dox_contents
	
	def get_doxy_args(self):
		
		if not self.conf.doxy_args:
			if self.V > 0:
				print "  > No vars"
			return []
		
		xover = []
		for dox in self.conf.doxy_args:
			xover.append(dox )
		return xover


	
	def get_version(self):
		
		version = "-na-"
		if self.conf.version_no:
			version = self.conf.version_no
			
		if self.conf.version_file:
			version = h.read_file( self.conf.work_dir + self.conf.version_file ).strip()
		return version
	
	## Write out temp doxy file
	# @param contents  The doxy string
	def write_temp_doxy(self, contents):
		
		if os.path.exists( self.conf.temp_doxy_path):
			os.remove(self.conf.temp_doxy_path)
		h.write_file( self.conf.temp_doxy_path, contents)
		if self.V > 0:
			print "> Wrote temp doy file: %s" % self.conf.temp_doxy_path
			
	## Write out json encoded info file to config.Config.INFO_JSON_FILE
	def write_info_file(self):
		dic = dict(color= self.conf.color,
					version=self.get_version(),
					title=self.conf.title,
					project=self.conf.proj,
					date_updated=datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y-%m-%d %H:%M:%S")
				)  
		h.write_file(self.conf.json_info_path, json.dumps(dic) )

	def get_projects_pages_cpp(self):
		projects = self.main_conf.get_projects_index()
		
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
				
		return s
	
	## Return the html index page. This is included in \ref mainpage
	# @retval str The table contents
	def get_projects_table_html(self):
		s = '<table id="projects_index">\n'
		s += "<tr>\n"
		s += "\t<th>Project</th><th>Zip</th><th>Version</th><th>Updated</th><th>More..</th>"
		s += "\n</tr>\n"
		for p in self.main_conf.get_projects_index(load_info=True):
			s += '\n<tr>\n\t<td><a class="lnk" href="%s/" style="border-left: 10px solid %s;">' % (p.proj, p.color)
			s += '%s</a></td>' % (p.title)
			s += '\n<td><a target="_blank" href="%s/%s.zip">%s.zip</a></td>' % (p.proj, p.proj, p.proj)
			s += '\n<td>%s</td><td>%s</td>' % (p.version, p.date_updated)
			s += '<td><a href="projects.html#%s">%s</a></td>' % (p.proj, p.proj)
			s += '</tr>\n'
		s += "</table>"
		return s

			