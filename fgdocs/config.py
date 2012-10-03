## @package config
# @author Peter Morgan

import os
import yaml


import helpers as h

## Project Configuration
class ProjectConfig(object):
    pass
    



## Load the config file and access as objects
class Config:
        
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
    def project(self, proj):
        if not self.has_project(proj):
            return None
        
        dic = self.conf[proj]
        
        p = ProjectConfig()
        p.proj = proj
        p.is_main = proj == self.SELF_PROJ 
        
        
        p.abbrev = dic['abbrev']
        p.title = dic['title']

        if p.is_main:
            p.build_dir = self.ROOT 
        else:    
            p.build_dir = self.ROOT + proj + "/"
        
        p.work_dir = self.TEMP + proj + "/"
        
        p.repo = dic['repo']
        p.is_git = p.repo == "git"
        p.is_svn = p.repo == "svn"
        p.checkout = dic['checkout']
        
        
        
        return p
        
    def projects(self, runlevel=False):
        return self.conf.keys()
        
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
        
        
        