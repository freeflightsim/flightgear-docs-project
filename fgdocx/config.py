## @namespace fgdocs
# @package config
# @author Peter Morgan

import os
import sys
import yaml
import json
from optparse import OptionParser
import operator


import helpers as h

## The base config class inherited by Config and ProjectConfig
# The core class creates class constants such as the project root, temp paths etc
class ConfigCore(object):
	
	## This project itself    
	SELF_PROJ = "fgdocx"
	
	## Absolute directory path to location of this file with trailing /
	ROOT = os.path.abspath( os.path.dirname(__file__) + "/../" ) + "/"
	
	## Location of etc/ dir with trailing /
	ETC = ROOT + "etc/"
	
	## Location of the temp/ directory with trailing /
	TEMP = ROOT + "temp/"
	
	## Location of the build/ output directory with trailing /
	BUILD = ROOT + "build/"
	
	## Name of the default doxygen file
	DEFAULT_DOXY = "doxy-default.conf"
	
	## Name of the json encoded 
	INFO_JSON_FILE = "info.json"
	
	## Name of the config file
	CONFIG_FILE = "projects.config.yaml"
	
	TEMP_DOXY = "fg_docs_temp_doxy.conf"
	
	
## Project Configuration
# This class loads the configuration and settings for a project
class ProjectConfig(ConfigCore):
	
	## Load project configuration
	# @param proj The project key
	# @param dic The project dictionary
	def __init__(self,  proj, dic):

		## The project key
		self.proj = proj
		
		## Whether this is the main/self config
		# This affect mainly to build target which is not a subdirectory
		self.is_main = proj == self.SELF_PROJ
		
		## Abbreviation
		self.abbrev = dic['abbrev']
		
		
		## Project Title 
		# @see \ref title_config
		self.title = dic['title']
		
		## Project color - This is output in the index
		# @see \ref color_config
		self.color = dic['color'] if 'color' in dic else "#004499"
		
		## The runlevel
		# @see \ref runlevel_config
		self.runlevel = int(dic['runlevel']) 
		
		## The repo type
		# @see \ref repo_config
		self.repo = dic['repo']
		
		## The checkout url
		# @see \ref checkout_config
		self.checkout = dic['checkout']
		
		## True is \b repo: is git
		self.is_git = self.repo == "git"
		
		## True if \b repo: is svn
		self.is_svn = self.repo == "svn"
		
		## The git branch (defaults to \b master_
		# @see \ref branch_config
		self.branch = None
		if self.is_git:
			self.branch = dic['branch'] if "branch" in dic else "master"
	
		if self.is_main:
			self.build_dir = self.BUILD 
		else:    
			self.build_dir = self.BUILD + self.proj + "/"
		
		self.work_dir = self.TEMP + self.proj + "/"
		

		## Files to copy 
		self.copy = None
		if 'copy' in dic and len(dic['copy']) > 0:
			self.copy = []
			for co in dic['copy']:
				self.copy.append(co)
		
		## Extra doxy args   
		# @see \ref doxy_args_conf     
		self.doxy_args = None
		if 'doxy_args' in dic:
			self.doxy_args = [] 
			for dox in dic['doxy_args']:
				v = dic['doxy_args'][dox]
				if isinstance(v, bool):
					v = "YES" if v else "NO"
				self.doxy_args.append( "%s = %s" % (dox, v) )
		
		## The doxy file to use if present
		#  A project might not have a doxy file
		self.doxy_file = None
		
		## Whether this is an official upstream repository
		self.official = None
		
		## Date of last build
		self.date_updated = None
		
		## The version No
		# @see \ref version_config 
		self.version_no = None
		if 'number' in dic['version']:
				self.version_no = dic['version']['number']
				
		## The version file. 
		# @see \ref version_config
		self.version_file = None        
		if 'file' in dic['version']:
			self.version_file = dic['version']['file'].strip()
		
		## Placeholde Version. populated by:
		self.version = None
		
		## The full path to the temp doxy file
		self.temp_doxy_path = self.work_dir + self.TEMP_DOXY

		## The full path to the json encoded info file config.ConfigCore.INFO_JSON_FILE
		self.json_info_path = self.BUILD + self.proj  +  "/" + self.INFO_JSON_FILE
		if self.is_main:
			self.json_info_path = self.BUILD +  self.INFO_JSON_FILE
		
		## The tag files to include
		# @see \ref tags_config
		self.tags = None
		if 'tags' in dic:
			self.tags = []
			parts = dic['tags'].split()
			for p in parts:
				self.tags.append(p)
			
		


## Load the config file and access as objects
class Config(ConfigCore):
	
	## Load the default config from CONFIG_FILE
	def __init__(self, verbose=0):
		
		self._V = verbose
		self.raw_yaml_str = h.read_file( self.ETC + self.CONFIG_FILE )
		
		self.conf = yaml.load(self.raw_yaml_str)
		if self._V > 0:
			print "> Loaded configs: %s" % " ".join( self.conf.keys() )
		
			
	## Return project details
	# @param proj the project key
	# @retval dict Project dictinary or None if project to exist
	def get_project_dict(self, proj):
		if not self.has_project(proj):
			return None
		
		dic =  self.conf[proj]
		dic['proj'] = proj
		return dic
	
	## Return ProjectConfig instance
	# @param proj the project key
	# @retval ProjectConfig instance or None
	def get_project_config_object(self, proj):
		if not self.has_project(proj):
			return None
		projConf = ProjectConfig(proj, self.get_project_dict(proj))
		return projConf
	
	def get_projects_list(self):
		lst = []
		for c in self.conf:
			dic = self.conf[c].copy()
			dic['proj'] = c
			lst.append(dic)
		return lst
	
	## Return the project index 
	def get_projects_index(self, load_info=True, runlevel=False):
		
		#if runlevel:
		#	proj_list = self.get_projects_list()
		#	proj_keys = sorted( proj_list, key=lambda k: k['runlevel'])
		#else:
		proj_keys = sorted( self.conf.keys() )
		
		proj_lst = []
		for proj in proj_keys:
			proj =  self.get_project_config_object(proj)
			data = self.load_json_info(proj.json_info_path)
			if data != None:
				proj.version = data['version']
				if 'date_updated' in data:
					proj.date_updated = data['date_updated']
			proj_lst.append(proj)
		return proj_lst
		
	## Loads a json encoded fiel from path
	# @param file_path to json encoded file
	# @retval dict of values if file exists and readable, else None
	def load_json_info(self, file_path):
		if os.path.exists(file_path):
			json_str = h.read_file(file_path)  
			dic = json.loads(json_str)
			return dic
		return None
		
		
	## Return is configuration available for project
	# @param proj the project key
	# @retval bool True if config exists
	def has_project(self, proj):
		return proj in self.conf
	
	## Print the configuration
	## @param yaml_str outputs the raw yaml string, otherwise nice
	def print_view(self, yaml_str=False):
		
		if yaml_str:
			print self.raw_yaml_str
		
		else:
			s = ""
			for proj in self.projects(runlevel=True):
				s += proj + "\n"
				for v in self.conf[proj]:
					s += "  %s: %s\n" % (v, self.conf[proj][v])
			print s
		

		