## @package config
# @author Peter Morgan

import os
import yaml
import json
from optparse import OptionParser

import helpers as h

class ConfigCore(object):
    
    ## This project itself    
    SELF_PROJ = "fg-docs"
    
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
    CONFIG_FILE = "config.yaml"
    
    TEMP_DOXY = "fg_docs_temp_doxy.conf"
    
## Project Configuration
class ProjectConfig(ConfigCore):
    
    
    def __init__(self,  proj, dic):
        """
        self.ROOT = Config.ROOT
        self.TEMP = Config.TEMP
        self.BUILD = Config.BUILD
        self.ETC = Config.ETC
        """
        self.proj = proj
        self.is_main = proj == Config.SELF_PROJ
        
        self.abbrev = dic['abbrev']
        self.version = dic['version']
        self.title = dic['title']
        self.color = dic['color'] if 'color' in dic else "#004499"
        
        self.runlevel = int(dic['runlevel']) 
        
        self.repo = dic['repo']
        self.checkout = dic['checkout']
        self.is_git = self.repo == "git"
        self.is_svn = self.repo == "svn"
       
        if self.is_main:
            self.build_dir = self.ROOT 
        else:    
            self.build_dir = self.ROOT + self.proj + "/"
        
        self.work_dir = self.TEMP + self.proj + "/"
         

        ## Files to copy 
        self.copy = None
        if 'copy' in dic and len(dic['copy']) > 0:
            self.copy = []
            for co in dic['copy']:
                self.copy.append(co)
        
        ## Extra foxy args        
        self.doxy_args = None
        if 'doxy_args' in dic:
            self.doxy_args = [] 
            for dox in dic['doxy_args']:
                self.doxy_args.append( "%s = %s" % (dox, dic['doxy_args'][dox]) )
        
        self.doxy_file = None
        
        self.official = None
        self.date_updated = None
        
        self.version_no = None
        if 'number' in dic['version']:
                self.version_no = dic['version']['number']
        
        self.version_file = None        
        if 'file' in dic['version']:
            self.version_file = dic['version']['file'].strip()
        
 
        
        self.temp_doxy_path = self.work_dir + self.TEMP_DOXY

        if self.is_main:
            self.json_info_path = self.BUILD +  self.INFO_JSON_FILE
        else:
            self.json_info_path = self.BUILD + self.proj  +  "/" + self.INFO_JSON_FILE


## Load the config file and access as objects
class Config(ConfigCore):
    
    ## Load the default config from CONFIG_FILE
    def __init__(self, verbose=0):
        
        self._V = verbose
        self.raw_yaml_str = h.read_file( self.ROOT + self.CONFIG_FILE )
        
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
    
    def get_projects_info(self):
        info = []
        for proj in sorted(self.conf.keys()):
            proj =  self.get_project_config_object(proj)
            if os.path.exists(proj.json_info_path):
                json_str = h.read_file(proj.json_info_path)
                
                data = json.loads(json_str)
                #print json_str, data
                proj.version = data['version']
                if 'date_updated' in data:
                    proj.date_updated = data['date_updated']
            info.append(proj)
        
        return info

    def get_project_keys(self, runlevel=False):
        return self.conf.keys()
    
    def projects(self):
        ulist = []
        for proj in self.conf:
            dic = self.conf[proj]
            dic['runlevel'] = int(dic['runlevel']) if  'runlevel' in dic else 0
            dic['proj'] = proj
            ulist.append(dic)
        compile_list = sorted(ulist, key=operator.itemgetter('runlevel'))    
        for p in compile_list:
            print p['proj'] , p['runlevel']
          
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
        
    ## Get the projects index as a list of dicts. This loops thru the projects and reads the INFO_JSON_FILE_FILE
    @staticmethod
    def get_projects_index(self):
        ret = []
        for proj in sorted(self.conf.keys()):
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
        