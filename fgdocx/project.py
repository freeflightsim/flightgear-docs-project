## @package fgdocs


import os
import sys
import datetime

import json
import shutil

import helpers as h

## Builds a project
class ProjectBuilder:
    
    ## Initialze the project builder from configs
    # @param mainConf - a config.Config instance
    # @param projObj - a config.ProjectConfig instance
    # @param verbose - verbosity of output
    def __init__(self, mainConf, projname, verbose=1):
        
        ## Verbosity 0-4
        self.V = verbose
        
        ## Config object
        self.main_conf = mainConf
        self.projname = projname


        
        ## ProjectConfig  object
        self.conf = self.main_conf.get_project_config_object(self.projname)

    def wd(self):
	    return self.conf.work_dir

    ## Prepare the project, copying files, setting up doxy etc    
    def prepare(self):
        if self.V > 0:
            print "\n================================================================================="
            print "# Processing: %s" % self.conf.proj
            print "================================================================================="
                
        ##===========================================
        if self.V > 1:
            print "> Checking if temp/work_dir exists: %s" % self.conf.work_dir
        if not os.path.exists(self.conf.work_dir):
            if self.V > 1:
                print " > creating temp/work_dir path: %s" % self.conf.work_dir
            os.mkdir(self.conf.work_dir)
        else:
            if self.V > 1:
                print " > path Exists temp/work_dir path: %s" % self.conf.work_dir    
        
        ##===========================================
    
            
        # nuke and recreate build:
        if not self.conf.is_main:
            if self.V > 0:
                print "> checking build directory exits: %s" % self.conf.build_dir
            #if os.path.exists(self.conf.build_dir):
                #if self.V > 1:
                #	print "\t nuking build directory: %s" % self.conf.build_dir
                #shutil.rmtree(build_dir)
            #if self.V > 1:
            #	print "  > creating build directory: %s" % self.conf.build_dir
            
            #os.mkdir(build_dir)
        

            


            
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
        xover.append('TREEVIEW_WIDTH = 250')
        
        #xover.append('CLASS_DIAGRAMS = ')
        xover.append('HAVE_DOT = ')
        #xover.append('FILTER_SOURCE_FILES: YES')
        py_processor =  self.conf.ETC + "doxypy.py"
        #xover.append( 'FILTER_PATTERNS = "*.py=%s"' % py_processor )
        #xover.append('INPUT_FILTER: "%sdoxypy.py" ' % self.conf.ROOT)
        xover.append('WARN_LOGFILE = %s' % self.conf.build_dir + "warnings.txt")
        
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
        self.write_temp_doxy(dox_config_str)
        
    def get_build_cmd(self):
        print "\n> Compile: "
        os.chdir(self.conf.work_dir)
        if self.V > 0:
            print "  > curdir: %s" % os.path.abspath( os.curdir )
        
        dox_cmd =  "/usr/local/bin/doxygen ./%s " % self.conf.TEMP_DOXY
        if self.V > 0:
            print "  > command: %s" % dox_cmd
        return dox_cmd

    def post_build(self):
        
        if self.V > 0:
            print "> Copying extra files:"
        for f in ["logo-23.png", 'favicon.ico']: #, "dynsections.js"]:
            if self.V > 0:
                print ">   copied: %s" % f
            shutil.copyfile( self.conf.ETC + f , self.conf.build_dir + f )
        
        ## write info json
        self.write_info_file()
        
        print "< Done: %s" % self.conf.proj

            
                
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
            nav_str += '<li><a href="index.html">Index</a></li>\n'
        else:
            nav_str += '<li><a href="../">Index</a></li>\n'
        link_prefix = "" if self.conf.is_main else "../"
        for p in self.main_conf.get_projects_index():
            if not p.is_main:
                nav_str += '<li><a href="%s%s/">%s</a></li>\n' % (link_prefix, p.proj, p.abbrev)
    
        return nav_str
    
    def get_repo_link(self):
        s = ""
        if not self.conf.is_main:
            s += '<a target="_blank" class="projectrepos" href="%s">%s</a>\n' % (self.conf.project_page, self.conf.checkout)
        return s

    def get_branch(self):
        return "[%s]" % self.conf.branch
        if self.conf.is_main:
            s += '<a href="%s">%s</a>\n' % (self.conf.checkout, self.conf.checkout)
        return s
    
    ## Writes out the html header file
    def write_header_html(self):
        
        template_header = h.read_file( self.conf.ETC + "fg_docx_header.html" )
        template_header = template_header.replace("___NAV_ITEMS___", self.get_navigation() )
        template_header = template_header.replace("___REPO_LINK___", self.get_repo_link() )
        template_header = template_header.replace("___REPO_BRANCH___", self.get_branch() )
        h.write_file( self.conf.work_dir + "fg_docx_header.html", template_header)
    
    ## Return the contents of the doxy file  
    def get_doxy_file(self):
        if self.V > 0:
            print "> Checking doxy file"

        if self.conf.doxy_file:
            if self.V > 0:
                doxy_path = self.conf.ROOT + self.conf.doxy_file
                print "  > using %s project doxy file: %s" % (self.conf.proj, doxy_path )
            dox_contents = h.read_file(doxy_path)
            
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
        #print "CONTENTS", contents[:1000]
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

    def get_projects_dic(self):
        return self.main_conf.get_projects_dic()

    def get_projects_pages_cpp(self):
        projects = self.main_conf.get_projects_index()
        
        l = []
        for p in projects:
            l.append( " * \section project_%s %s" % (p.proj, p.title) )
            l.append( " * - Version: %s" % p.version)
            l.append( " * - repo: %s" % p.repo)
            l.append( " * - checkout: %s" % p.checkout)
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
        s += "\t<th>Path</th><th>Project</th><th>Version</th><th>Branch</th><th>Updated</th><th>Source</th>"
        s += "\n</tr>\n"
        for p in self.main_conf.get_projects_index(load_info=True):
            if p.is_main == False:
                s += '\n<tr>\n'
                s += '\t<td><a class="lnk" href="%s/" style="border-left: 10px solid %s;">' % (p.proj, p.color)
                s += '%s</a></td>' % (p.proj)
                s += '\t<td>%s<br><a target="_blank" class="lnkp" href="%s">' % (p.title, p.project_page)
                s += '%s</a></td>'  % p.project_page

                s += '\n<td>%s</td><td>%s</td><td>%s</td>' % (p.version, p.branch if p.branch else "-", p.date_updated)
                s += '<td>%s</td>' % (p.checkout)
                s += '</tr>\n'
        s += '\n<tr>\n'
        s += '\t<td><a class="lnk" target="_fgms" href="%s" style="border-left: 10px solid %s;">' % ("http://fgms.freeflightsim.org/", "#C974B4")
        s += '%s</a></td>' % ("fgms")
        s += '\t<td>%s<br><a target="_fgms" class="lnkp" href="%s">' % ("Multiplayer Server", "http://fgms.freeflightsim.org/")
        s += '%s</a></td>'  % "http://fgms.freeflightsim.org/"

        s += '\n<td>%s</td><td>%s</td><td>%s</td>' % ("-", "-", "-")
        s += '<td>%s</td>' % "-"
        s += '</tr>\n'
        s += "</table>"
        return s

