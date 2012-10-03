
import os
import sys
import datetime

import json
import shutil
import git
import pysvn

import helpers as h

###########################################################################
class Project:
    
    ## Initialse the project a config
    # @param confObject - a ProjectConfig instance
    def __init__(self, mainConf, projObj, verbose=1):
        
        ## Vervosity 0-4
        self.V = verbose
        
        ## ProjectConfig object
        self.main_conf = mainConf
        self.conf = projObj 
        
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
            if V > 0:
                print "\t checking build directory exits: %s" % self.conf.build_dir
            if os.path.exists(self.conf.build_dir):
                if V > 1:
                    print "\t nuking build directory: %s" % self.conf.build_dir
                #shutil.rmtree(build_dir)
            if V > 1:
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
 
            
            elif pvals['repo'] == "svn":
                
                if not os.path.exists(work_dir + "/.svn/"):
                    print "Checkout out svn"
                    svn = pysvn.Client()
                    print pvals
                    print svn.checkout( pvals['checkout'] , work_dir, recurse=True)
                else:
                    print "SVN update"
                    svn = pysvn.Client()
                    svn.update( work_dir, recurse=True )

            
        ## Copy file
        self.copy_files()
        
        #print nav_str
        #sys.exit(0)
        
        #### copy required file
        if self.V > 0:
            print "> Copying build files:"
        for f in ["fg_xstyle.css"]:
            if self.V > 0:
                print ">   copied: %s" % f
            shutil.copyfile( self.conf.ETC + f , self.conf.work_dir + f )
        

        
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
        xover.append('HTML_EXTRA_STYLESHEET = "fg_xstyle.css"')
        xover.append('TREEVIEW_WIDTH = 120')
        
        dox_override = "\n".join(xover)
        
        if self.V > 0:
            print "> Overides for fg-docs output"
            for oo in xover:
                print "  > " + oo
        
        ## make config string and write to file
        dox_config_str = dox_file_contents + dox_override
        #print dox_config_str
        self.write_temp_doxy(dox_config_str)
        
    def compile(self):
        print "\n> Compile: "
        os.chdir(self.conf.work_dir)
        if V > 0:
            print "  > curdir: %s" % os.path.abspath( os.curdir )
        
        dox_cmd =  "doxygen ./%s " % self.conf.temp_doxy_file 
        if V > 0:
            print "  > command: %s" % dox_cmd
        os.system( dox_cmd  )
        
        if V > 0:
            print "> Copying extra files:"
        for f in ["logo-23.png"]:
            if V > 0:
                print ">   copied: %s" % f
            shutil.copyfile( self.conf.ETC + f , self.conf.build_dir + f )
        
        ## write info json
        h.write_info_file(self.conf.proj, self.conf.version, pvals)
        
        print "< Done: %s" % proj

    ## Process this project is its git
    def git_process(self):
        print "  > Checking is git repos at: %s" % self.conf.work_dir + "/.git"       
        if not os.path.exists(self.conf.work_dir + "/.git/"):
            #os.chdir(TEMP)
            self.git_clone()
                    

    def git_clone(self):
      
        print "Cloning new Repo"
        shutil.rmtree( self.conf.work_dir )
        #print "work_dir=", work_dir
        #cmd = "git clone %s %s" % (pvals['git'], proj )
        #print "git clone= ", cmd
        #os.system(cmd)
        os.chdir( self.conf.TEMP )
        g = git.Git( self.conf.TEMP )
        g.clone(pvals['git'], proj)
            
          
    def git_update(self):
       
        
            
           
                
                
                branch = pvals['branch'] if "branch" in pvals else "master"
                print "\t\t\tCheckout branch: %s" % branch
                g = git.Git( TEMP + proj)
                print g.checkout(branch)
                print g.pull()
                
    ## Copies the files in \ref copy
    def copy_files(self):
        if self.conf.copy:
            print self.conf.copy 
            for f in self.conf.copy:
                source = self.conf.ROOT + f
                head, tail = os.path.split(source)
                print "  > cp " + self.conf.ROOT + f + " >> " +  self.conf.work_dir + tail
                shutil.copyfile( self.conf.ROOT + f, self.conf.work_dir + tail)
        
    #### Make the Top navigation
    def get_navigation(self):
        nav_str = ""
        if self.conf.is_main:
            nav_str += '<li><a href="index.html">Home</a></li>\n'
        else:
            nav_str += '<li><a href="../">Home</a></li>\n' 
        link_prefix = "" if self.is_main else "../"
        for c in self.conf:
            if c != "fg-docs":
                nav_str += '<li><a href="%s%s/">%s</a></li>\n' % (link_prefix, c, conf[c]['abbrev'])
        return nav_str
    
    def write_header_html(self):
        
        template_header = h.read_file( ETC + "fg_docx_header.html" )
        template_header = template_header.replace("___NAV_ITEMS___", self.get_navigation() )
        h.write_file( self.conf.work_dir + "fg_docx_header.html", template_header)
        
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
            version = h.read_file( self.conf.work_dir + self.conf.version_file )
        return version
    
    def write_temp_doxy(self, contents):
        
        if os.path.exists( self.conf.temp_doxy_path):
            os.remove(self.conf.temp_doxy_path)
        h.write_file( self.conf.temp_doxy_path, contents)
        if self.V > 0:
            print "> Wrote temp doy file: %s" % self.conf.temp_doxy_path
            
    ## Write out json encoded info file to \ref INFO_JSON_FILE
    #  @param proj the project dir
    #  @param version the version
    #  @param conf the yaml config file
    def write_info_file(self):
        dic = dict(color= self.conf.color,
                    version=self.get_version(),
                    title=self.conf.title,
                    project=self.conf.proj,
                    date_updated=datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y-%m-%d %H:%M:%S")
                )  
        h.write_file(self.conf.json_info_path, json.dumps(dic) )

    def get_projects_pages_cpp(self):
        projects = self.main_conf.get_projects_info()
        
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
    
    def get_projects_table_html(self):
        s = '<table id="projects_index">\n'
        s += "<tr>\n"
        s += "\t<th>Project</th><th>Zip</th><th>Version</th><th>Updated</th><th>More..</th>"
        s += "\n</tr>\n"
        for p in self.main_conf.get_projects_info():
            s += '\n<tr>\n\t<td><a class="lnk" href="%s/" style="border-left: 10px solid %s;">' % (p.proj, p.color)
            s += '%s</a></td>' % (p.title)
            s += '\n<td><a target="_blank" href="%s/%s.zip">%s.zip</a></td>' % (p.proj, p.proj, p.proj)
            s += '\n<td>%s</td><td>%s</td>' % (p.version, p.date_updated)
            s += '<td><a href="projects.html#%s">%s</a></td>' % (p.proj, p.proj)
            s += '</tr>\n'
        s += "</table>"
        return s

            