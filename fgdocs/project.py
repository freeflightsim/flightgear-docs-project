
import os
import sys
import shutil

import helpers as h

###########################################################################
class Project:
    
    ## Initialse the project a config
    # @param confObject - a ProjectConfig instance
    def __init__(self, confObj, verbose=1):
        
        ## Vervosity 0-4
        self.V = verbose
        
        ## ProjectConfig object
        self.conf = confObj 
        
    def build_project(self):
        if self.V > 0:
            print "---------------------------"
            print "# Processing: %s" % self.conf.proj
    
        #is_main = proj == "fg-docs"
        
        #work_dir = TEMP + proj + "/"
        
        #if is_main:
        #    build_dir = BUILD 
        #else:
        #    build_dir = BUILD + proj + "/"
            
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
        if not self.conf.is_main:
            
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
            #sys.exit(0)
            #print rep.is_dirty
            #print rep.git.status()
        else:
            pass
            ## ITS MAIN, so make up the site
            #if os.path.exists(work_dir + "docx/"):
            #    shutil.rmtree(work_dir + "docx/")
            #os.mkdir(work_dir + "docx/")
            
            #shutil.copytree( ROOT + "docx/"  , work_dir + "docx"  )
            #shutil.copyfile( ROOT + "py_update.py", work_dir + "py_update.py")
            
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
        doxy_str = self.get_doxy_file()
    
        ## Add the extra stuff doxy vars from config
        if self.V > 0:
            print "> Checking doxy vars from config.yaml"
        doxy_str += self.get_doxy_args()
        
        ## MAIN project extras
        if self.conf.is_main:
            h.write_file(self.conf.work_dir + "projects_index.html", self.get_projects_table())
            h.write_file( self.conf.work_dir + "project_pages.cpp",  self.get_projects_pages_cpp())
            
        ## Append and override the main settings from here
        xover.append('PROJECT_NAME="%s"' % proj)
        
        ## get version no from yaml, or source file
        version = "-na-"
        if 'version' in pvals:
            if 'number' in pvals['version']:
                version = pvals['version']['number']
                
            elif 'file' in pvals['version']:
                version = read_file( work_dir + pvals['version']['file'] ).strip()
        xover.append('PROJECT_NUMBER="%s"' % version)
        xover.append('PROJECT_BRIEF="%s"' % pvals['title'])
            
        xover.append('OUTPUT_DIRECTORY=' + build_dir )
        xover.append('HTML_OUTPUT=%s' %  "./")
        xover.append('GENERATE_TAGFILE=' + build_dir + proj + ".tag")
        xover.append('HTML_HEADER = fg_docx_header.html')
        xover.append('HTML_EXTRA_STYLESHEET = "fg_xstyle.css"')
        xover.append('TREEVIEW_WIDTH = 120')
        
        dox_override = "\n".join(xover)
        
        if V > 0:
            print "> Overides for fg-docs output"
            for oo in xover:
                print "  > " + oo
        
        ## make config string and write to file
        dox_config_str = dox_default + dox_override
        #print dox_config_str
        temp_doxy_file = "fg_temp_doxy.conf"
        temp_config_full_path = work_dir +  temp_doxy_file
        if os.path.exists( temp_config_full_path ):
            os.remove(temp_config_full_path)
        write_file( temp_config_full_path, dox_config_str)
        if V > 0:
            print "> Wrote temp doy file: %s" % temp_config_full_path
        
        print "\n> Compile: "
        os.chdir(work_dir)
        if V > 0:
            print "  > curdir: %s" % os.path.abspath( os.curdir )
        
        dox_cmd =  "doxygen ./%s " % temp_doxy_file 
        if V > 0:
            print "  > command: %s" % dox_cmd
        os.system( dox_cmd  )
        
        if V > 0:
            print "> Copying extra files:"
        for f in ["logo-23.png"]:
            if V > 0:
                print ">   copied: %s" % f
            shutil.copyfile( ETC + f , build_dir + f )
        
        ## write info json
        write_info_file(proj, version, pvals)
        
        print "< Done: %s" % proj

    ## Process this project is its git
    def git_process(self):
             
        if not os.path.exists(self.conf.work_dir + "/.git/"):
            #os.chdir(TEMP)
            print "Cloning new Repo"
            shutil.rmtree( self.conf.work_dir )
            #print "work_dir=", work_dir
            #cmd = "git clone %s %s" % (pvals['git'], proj )
            #print "git clone= ", cmd
            #os.system(cmd)
            os.chdir( self.conf.TEMP )
            g = git.Git( self.conf.TEMP )
            g.clone(pvals['git'], proj)
                    

    def git_clone(self):
      print "  > Checking is git repos at: %s" % work_dir + "/.git"
          
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
        link_prefix = "" if is_main else "../"
        for c in conf:
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
            return "\n"
        
        xover = []
        for dox in self.conf.doxy_args:
            xover.append(dox )
        return "\n".join(xover)

    def get_projects_table():
        s = '<table id="projects_index">\n'
        s += "<tr>\n"
        s += "\t<th>Project</th><th>Zip</th><th>Version</th><th>Updated</th><th>More..</th>"
        s += "\n</tr>\n"
        for p in self.get_projects_index():
            
            #pconf = conf[proj]
            #is_main = proj == "fg-docs"
            #js_filen =  BUILD + INFO_JSON_FILE if is_main else BUILD + proj + "/" + INFO_JSON_FILE
            #data = None
            #if os.path.exists(js_filen):
            #    json_str = read_file(js_filen)
            #    data = json.loads(json_str)
            #print data
            #if c != "fg-docs":
            #color = pconf['color'] if 'color' in pconf else "blue"
            #version = data['version'] if data else pconf['version']['number']
            #title = pconf['title']
            #repo = pconf['repo']
            #checkout = pconf['checkout']
            #v = conf[proj]
            s += '\n<tr>\n\t<td><a class="lnk" href="%s/" style="border-left: 10px solid %s;">' % (p.proj, p.color)
            s += '%s</a></td>' % (p.title)
            s += '\n<td><a target="_blank" href="%s/%s.zip">%s.zip</a></td>' % (p.proj, p.proj, p.proj)
            s += '\n<td>%s</td><td>%s</td>' % (p.version, p.date_updated)
            #s += '\n<td>%s</td><td>%s</td>\n</tr>\n' % (repo, checkout)
            #s += '\n<td>%s</td><td>%s</td>\n'  % (repo, checkout)
            s += '<td><a href="projects.html#%s">%s</a></td>' % (p.proj, p.proj)
            s += '</tr>\n'
        s += "</table>"
        return s