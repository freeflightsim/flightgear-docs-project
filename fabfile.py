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


conf = _Config(1)


def checkoutall():
    with lcd(conf.TEMP):
        local("git clone http://git.code.sf.net/p/flightgear/fgdata")
        local("svn co https://svn.code.sf.net/p/plib/code/trunk plib")
        local("git clone https://github.com/openscenegraph/osg.git")
        local("git clone git://gitorious.org/fg/simgear.git")
        local("git clone git://gitorious.org/fg/flightgear.git")
        local("git clone git://gitorious.org/fg/terragear.git")
        


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

def fgdata():
    """flightgear docs build"""
    projObj = _ProjectBuilder(conf, "fgdata")
    with lcd(projObj.wd()):
        #local("git pull")
        temp_dir = projObj.wd() + "_examples"
        local("mkdir -p " + temp_dir)

        shaders = []
        verts = []
        frags = []
        shades_dir = projObj.wd() + "/Shaders"
        for f in os.listdir(shades_dir):
            print "f=", f
            parts = f.split(".")
            ext = parts[1]
            fp = parts[0]
            if ext in ["vert", "frag"] and shaders.count(fp) == 0:
                shaders.append(fp)
                shade_fn = shades_dir + f
                print shade_fn
                src = _h.read_file(shade_fn)
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
        return
        s = "<table>\n"
        s += "\t<tr><th>Frag</th><th>Vert</th></tr>\n"
        for sh in shaders:
            fr = ""
            if sh in frags:
                fr = sh + ".frag"
            vr = ""
            if sh in verts:
                vr = sh + ".vert" 
            s += "\t<tr><td>%s</td><td>%s</td></tr>\n" % (fr, vr)
        s += "</table>"
        #print s
        f = temp_dir + "/shaders.html"
        print f
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
    for d in ["simgear", "terragear", "flightgear", "fgdata"]:
        with lcd(conf.TEMP + d):
            local("git pull")

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
    site()
    sitemap()
