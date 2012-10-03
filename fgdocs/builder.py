
import sys
import os
import shutil

from config import Config
from project import ProjectBuilder

## The docs builder is the class that runs things
# - It does this by checking the commands are sane
# - Then checking the commands and executing
# @param parser 
# @param opts The parser opts
# @param args 
class DocsBuilder:
    
    COMMANDS = ['build', 'buildall', 'view', 'clean', 'nuke']
    
    def __init__(self, parser, opts, args):
        
        ## Verbose
        self.V = opts.v
        
        ## Check there is a command
        if len(args) == 0:
            parser.error("Need to supply a command ")
            sys.exit(0)
  
        ## check commands exist
        if not args[0] in self.COMMANDS:
            parser.error("Command '%s' not recognised" % args[0] )
            sys.exit(0)
        self.command = args[0]
        
        
        
        """
        if self.V > 2:
            print "========================================================="
            print "options=", opts, opts.v
            print "args=", args
        
        """
        ## Initialse config
        self.conf = Config()
        
        self.check_enviroment()
        
        errs = []
        
                
        if len(args) == 0:
            parser.error("Need to supply a command")
            #parser.print_help()
            sys.exit(0)
        self.command = args[0]
        
        ## The command executed is the first var
        
        if self.V > 1:
            print "#> command=", self.command
            
        #############################################################
        if self.command == "view":
            self.do_view()
        
        if self.command == "clean":
            shutil.rmtree(self.conf.BUILD)
            print "> Nuked build: %s" % self.conf.BUILD
            sys.exit(0)
            
        #############################################################    
        if self.command == "build":
            if len(args) == 1:
               parser.error("build command needs a project" )
               sys.exit(0) 
            projects = args[1:]
            
            print projects, self.conf
            ## Check that the project args are in config
            errs = []
            for a in projects:
                if not self.conf.has_project(a):
                    errs.append(a)
            if len(errs):
                print "Error: project%s not exist: %s" % ( "s" if len(errs) > 0 else "", ", ".join(errs))
                sys.exit(0)
            
            
            for proj in projects:
                self.build_project(proj)
                
        if self.command == "buildall":
            self.do_build_all()
    
    def do_build_all(self):
        s_list = 'fgms-0 fgms-1 plib osg simgear flightgear fg-docs'
        proj_lst = s_list.split()
        for proj in proj_lst:
            self.build_project( proj )
            
    def build_project(self, proj):
        projConf = self.conf.get_project_config_object(proj)
        projObj = ProjectBuilder(self.conf, projConf)
        projObj.prepare()
        projObj.build()     
            
    def do_view(self):
        
        self.conf.print_view(True)
        self.conf.print_view()
        sys.exit(0)


    def check_enviroment(self):
        ## Create temp and build dirs
        if not os.path.exists(self.conf.TEMP):
            if self.V > 0:
                print "\t\t Created working dir: temp/"
            os.mkdir(self.conf.TEMP)

        if not os.path.exists(self.conf.BUILD):
            if self.V > 0:
                print "\t\t Created working dir: build/"
            os.mkdir(self.conf.BUILD)    
            
