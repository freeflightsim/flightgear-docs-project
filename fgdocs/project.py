
import os
import sys
import shutil


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
        if 'copy' in pvals:
            print pvals['copy']
            for f in pvals['copy']:
                source = ROOT + f
                head, tail = os.path.split(source)
                print "  > cp " + ROOT + f + " >> " +  work_dir + tail
                shutil.copyfile( ROOT + f, work_dir + tail)
        
        
        #print nav_str
        #sys.exit(0)
        
        #### copy required file
        if V > 0:
            print "> Copying build files:"
        for f in ["fg_xstyle.css"]:
            if V > 0:
                print ">   copied: %s" % f
            shutil.copyfile( ETC + f , work_dir + f )
        
        #### Make the page template ###
        ## Create Navigation
        nav_str = ""
        if is_main:
            nav_str += '<li><a href="index.html">Home</a></li>\n'
        else:
            nav_str += '<li><a href="../">Home</a></li>\n' 
        link_prefix = "" if is_main else "../"
        for c in conf:
            if c != "fg-docs":
                nav_str += '<li><a href="%s%s/">%s</a></li>\n' % (link_prefix, c, conf[c]['abbrev'])
                
        template_header = read_file( ETC + "fg_docx_header.html" )
        template_header = template_header.replace("___NAV_ITEMS___", nav_str)
        write_file( work_dir + "fg_docx_header.html", template_header)
        
        ##############################################
        ## Create temp doxy string and write to file
        
        ## READ default
        if V > 0:
            print "> Checking doxy file"
        if 'doxy_file' in pvals and pvals['doxy_file']:
            if V > 0:
                print "  > using %s project doxy file: %s" % (proj, pvals['doxy_file'])
            dox_default = read_file(work_dir + pvals['doxy_file'])
            
        else:
            dox_default = read_file(ETC + DEFAULT_DOXY)
            if V > 0:
                print "  > using default fg-docs file: etc/%s"  % DEFAULT_DOXY
    
        ## Add the extra stuff doxy vars from config
        if V > 0:
            print "> Checking doxy vars from config.yaml"
        xover = []
        if 'doxy_args' in pvals: 
            for dox in pvals['doxy_args']:
                xover.append( "%s = %s" % (dox, pvals['doxy_args'][dox]) )
        else:
            if V > 0:
                print "  > No vars"
        
        ## MAIN project extras
        if is_main:
            write_file(work_dir + "projects_index.html", make_projects_table())
            write_file( work_dir + "project_pages.cpp",  make_projects_pages_cpp())
            
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

    def git_process(self):
             #rep = git.Repo(work_dir)
        if not os.path.exists(self.conf.work_dir + "/.git/"):
            #os.chdir(TEMP)
            print "Cloning new Repo"
            shutil.rmtree( self.conf.work_dir )
            #print "work_dir=", work_dir
            #cmd = "git clone %s %s" % (pvals['git'], proj )
            #print "git clone= ", cmd
            #os.system(cmd)
            os.chdir(TEMP)
            g = git.Git( TEMP )
            g.clone(pvals['git'], proj)
                    

    def git_clone(self):
      print "  > Checking is git repos at: %s" % work_dir + "/.git"
          
    def git_update(self):
       
        
            
           
                
                
                branch = pvals['branch'] if "branch" in pvals else "master"
                print "\t\t\tCheckout branch: %s" % branch
                g = git.Git( TEMP + proj)
                print g.checkout(branch)
                print g.pull()
                
    