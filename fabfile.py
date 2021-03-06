## Visit api-docs.freeflightsim.org
# maintainer pete@freeflightsim.org
#
# Checkouts all the flightgear repos and uses doxygen to compile docs
# this is serielised to a build directory = static html = website
#
# Notes
# the only active changes are epected to be simgear + flightgear
# the whole build is done every two hours or so
import sys
import os
import yaml
import datetime
import glob

from fabric.api import env, local, run, cd, lcd, sudo, warn_only

from fgdocx.project import ProjectBuilder as _ProjectBuilder
from fgdocx.config import Config as _Config
import fgdocx.helpers as _h

env.hosts = [ 'api-docs.freeflightsim.org' ]
env.user = "fg"
env.password = "using ssh key"
env.use_ssh_config = True
env.shell = "/bin/sh -c"

REMOTE_PATH = "/home/fg/flightgear-docs-project"

conf = _Config(1)


def checkoutall():
	"""Checks out all repos"""
    # Need to read repos from projects_config.yaml
	with lcd(conf.TEMP):
		projs = conf.get_projects_dic()
		print projs.keys()
		del projs['fgdocx']
		del projs['plib']
		for pk in projs.keys():
			projObj = _ProjectBuilder(conf, pk)
			path = projObj.wd()
			cmd = "git clone %s" % projObj.conf.checkout
			print cmd
			if not os.path.exists(path):
				cmd = "git clone --depth 2 %s" % projObj.conf.checkout
				local(cmd)	 
		
		local("svn co https://svn.code.sf.net/p/plib/code/trunk plib")
        return    
        
        local("git clone https://github.com/openscenegraph/osg.git")
        local("git clone https://gitorious.org/fg/simgear.git")
        local("git clone https://gitorious.org/fg/flightgear.git")
        local("git clone https://gitorious.org/fg/terragear.git")
        
        
        
        
        
def openradar():
    """openradar build docs"""
    projObj = _ProjectBuilder(conf, "openradar")
    with lcd(projObj.wd()):
        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()  
        


def plib():
    """plib build docs"""
    projObj = _ProjectBuilder(conf, "plib")
    with lcd(projObj.wd()):
        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()

def osg():
    """OpenSceneGraph build docs"""
    projObj = _ProjectBuilder(conf, "osg")
    with lcd(projObj.wd()):
        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()

def sg():
    """simgear docs build"""
    projObj = _ProjectBuilder(conf, "simgear")
    with lcd(projObj.wd()):
        local("git pull")
        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()
        
def tg():
    """TerraGear docs build"""
    projObj = _ProjectBuilder(conf, "terragear")
    with lcd(projObj.wd()):
        local("git pull")
        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()

def fg():
    """flightgear docs build"""
    projObj = _ProjectBuilder(conf, "flightgear")
    with lcd(projObj.wd()):
        local("git pull")

        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()

def _get_nasal_files(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".nas"):
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

def fgdata():
    """flightgear docs build"""
    projObj = _ProjectBuilder(conf, "fgdata")
    with lcd(projObj.wd()):
        #local("git pull")
        temp_dir = projObj.wd() + "_examples"
        local("mkdir -p " + temp_dir)

        xshaders_dir = projObj.wd() + "Shaders_"
        local("mkdir -p " + xshaders_dir)

        xnasal_dir = projObj.wd() + "Nasal_"
        local("mkdir -p " + xnasal_dir)
        
        nasal_dir = projObj.wd() + "Nasal"
        len_root = len(nasal_dir)
        
        files = _get_nasal_files(nasal_dir)
        #print files
        for f in files:
            print "---------"
            #print f
            
            nas_path = f[len_root:]
            #print nas_path
            target_dir = projObj.wd() + "Nasal_"  + os.path.dirname(nas_path)
            #print target_dir
            file_n = os.path.basename(f)
            print file_n
            
            bits = os.path.dirname(nas_path)
            bitp = _h.xsplit(bits, "/")
            print "bits=", bits, bitp
            ns =  "Nasal"
            if len(bitp) > 0:
                 ns = ns + "::" + "::".join(bitp)
            print ns
            classn = "_".join(bitp)
            classd = ".".join(bitp)
            #classn += file_n[:-4]
            defg = "\defgroup %s %s" % ( classn, classd )
            print defg
            local("mkdir -p " + target_dir)
            src = _h.read_file( f )
            
            src_n = "/**\n"
            src_n += "  * @namespace %s\n" % ns
            src_n += "  * @file %s \n" % file_n
            #src_n += "  * @{\n"
            #src_n += "  * @class %s\n" % classn
            src_n += "  */\n"
            src_n += src
            #src_n += "/** @}*/\n"
            #print src_n
            _h.write_file(target_dir + "/" + file_n, src_n)
        #return   
        shaders = []
        verts = []
        frags = []
        shades_dir = projObj.wd() + "/Shaders"
        for f in os.listdir(shades_dir):
            print "f=", f
            parts = f.split(".")
            ext = parts[1]
            fp = parts[0]
            if ext in ["vert", "frag"]:
                shade_fn = shades_dir + "/" + f
                print shade_fn
                src = _h.read_file(shade_fn)
                #print src[0:20]
                
                xparts = fp.split("-")
                #xuparts = [ xp.upper() for xp in xparts]
                ns = "::".join(xparts)
                src_n = "/**\n"
                src_n += "  * @namespace Shaders::%s\n" % ns
                src_n += "  */\n"
                src_n += src
                #print src_n
                _h.write_file(xshaders_dir + "/" + f, src_n)
                if shaders.count(fp) == 0:
                    shaders.append(fp)
                
            if ext == "frag":
                frags.append(fp)
            if ext == "vert":
                verts.append(fp)
        shaders = sorted(shaders)
        verts = sorted(verts)
        frags = sorted(frags)
        #print "shaders=", shaders
        #print ""
        #print "verts=", verts
        #print ""
        #print "frags=", frags
        #return
        s = "/*!\n"
        s += "\page shaders Shaders List\n\nList of shader files included\n\n"
        s += "<table>\n"
        s += "<tr><th>Frag</th><th>Vert</th></tr>\n"
        for sh in shaders:
            fr = ""
            if sh in frags:
                fr = sh + ".frag"
            vr = ""
            if sh in verts:
                vr = sh + ".vert" 
            s += "<tr><td>%s</td><td>%s</td></tr>\n" % (fr, vr)
        s += "</table>\n"
        s += "*/\n"
        #print s
        f = projObj.wd() + "shaders.dox"
        #print f
        _h.write_file(f, s)
        #return
        projObj.prepare()
        local("chmod +x ./glslfilter.py")
        local( projObj.get_build_cmd() )
        projObj.post_build()
        
def index():
    """Updates Main webpages ie fgdocx  build after others"""
    projObj = _ProjectBuilder(conf, "fgdocx")
    with lcd(projObj.wd()):
        projObj.prepare()
        local( projObj.get_build_cmd() )
        projObj.post_build()

def site():
    local("cp %s %s" % (conf.ETC + "robots.txt", conf.BUILD))
    local("cp %s %s" % (conf.ETC + "logo-23.png", conf.BUILD))
    local("cp %s %s" % (conf.ETC + "favicon.ico", conf.BUILD))

def sitemap():
    s = '<?xml version="1.0" encoding="utf-8"?>\n'
    s += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    s += "\t<url>\n"
    s += "\t\t<loc>http://api-docs.freeflightsim.org</loc>\n"
    s += "\t\t<changefreq>daily</changefreq>\n"
    s += "\t\t<priority>0.2</priority>\n"
    s += "\t</url>\n"
    for page in conf.get_projects_list():
        #print page
        s  += "\t<url>\n"
        s  += "\t\t<loc>http://api-docs.freeflightsim.org/%s/</loc>\n" % page['proj']
        s  += "\t\t<lastmod>%s</lastmod>\n" % datetime.datetime.strftime(datetime.datetime.utcnow(),"%Y-%m-%d %H:%M:%S")
        s  += "\t\t<changefreq>daily</changefreq>\n"
        s  += "\t\t<priority>0.3</priority>\n"
        s += "\t</url>\n"

    s += "</urlset>\n"
    #print s
    #print conf.BUILD + "sitemap.xml"
    _h.write_file(conf.BUILD + "sitemap.xml", s)

def pull():
    for d in ["fgms", "simgear", "terragear", "flightgear", "fgdata"]:
        with lcd(conf.TEMP + d):
            local("git pull")

def up_server():
	"""Psuh local stuff and update removte code"""
	local("git push origin master")
	with cd(REMOTE_PATH):
		run("git pull")
		
	

def update():
    pull()
    sg()
    #tg()
    fg()
    site()
    sitemap()
    index()

def all():
    """Build all"""
    plib()
    osg()
    sg()
    tg()
    fg()
    fgdata()
    site()
    sitemap()
    index()
    
def do_compile():
	"""Compiles fg"""
	for d in ["simgear", "flightgear"]:
		compile_dir = "%s%s_build" % (conf.TEMP, d)
		
		if not os.path.exists(compile_dir):
			with lcd(conf.TEMP):
				local("mkdir %s_build" % d)
			
		with lcd(compile_dir):
			cmake_config = "cmake ../%s" % (d)
			print compile_dir, cmake_config
			
			local( cmake_config )
			local( "make" )
			local( "sudo make install")
			
				
            
    
