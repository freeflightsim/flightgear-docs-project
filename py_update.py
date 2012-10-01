#!/usr/bin/env python

import os
import yaml
import git

ROOT = os.path.abspath( os.path.dirname(__file__) )

print "ROOT=%s" % ROOT

## Load Config
yaml_file = open("config.yaml")
conf = yaml.load( yaml_file.read() )
yaml_file.close()
print "Loaded config: %s" % " ".join( conf.keys() )


for proj, vals in conf:
	print proj, vals


