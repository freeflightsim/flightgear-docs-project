#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#

S = """AI_doc.html                                                                                                           
buildings.png                                                                                                         
FGShortRef.css                                                                                                        
FGShortRef.html                                                                                                       
FGShortRef.pdf                                                                                                        
FlightGear-FAQ.html                                                                                                   
fschool_0.0.3.pdf                                                                                                     
getstart-fr.pdf                                                                                                       
getstart.pdf                                                                                                          
img                                                                                                                   
index.html                                                                                                            
keyboard                                                                                                              
model-combined.eff                                                                                                    
model-howto.html                                                                                                      
README                                                                                                                
README.3DClouds                                                                                                       
README.airspeed-indicator                                                                                             
README.commands                                                                                                       
README.conditions
README.digitalfilters                                                                                                 
README.effects                                                                                                        
README.electrical                                                                                                     
README.fgjs
README.flightrecorder                                                                                                 
README.gui                                                                                                            
README.hud
README.introduction                                                                                                   
README.IO
README.Joystick
README.Joystick.html
README.JSBsim
README.jsclient
README.kln89.html                                                                                                     
README.layout
README.local_weather.html
README.logging
README.materials
README.mingw
README.minipanel
README.multiplayer
README.multiscreen
README.osgtext
README.properties
README.protocol
README.scenery
README.sound
README.submodels
README.tutorials
README.voice.html
README.wildfire
README.xmlhud
README.xmlpanel
README.xmlpanel.html
README.xmlparticles
README.xmlsound
README.xmlsyntax
README.yasim
README.YASim.rotor.ods
README.yasim.rotor.png
README.YASim.rotor.xls
Serial
"""

parts = S.split("\n")
print parts
	
for p in sorted(parts):
	p = p.strip()
	print ' * - <a href="Docs/%s">%s</a>' % (p, p)