/**
 * \mainpage Docs Index
 * 
 * The projects below are automatically updated daily. See here for more info
 * 
 * \page about About the Documentation Project
 * 
 * \section intro Introduction
 * The "tool" of this project is doxygen, a c++ tool to parse source code and then output
 * into various formats. The one we are interested in is html.
 * 
 * Indeed this test you are looking at was created by some documentation nutter 
 * in south wales (original not new), and the code style of doxy
 * 
 * Doxygen is a very clever application, your can throw anything at it and it can
 * make sense of something and create some docmentation out of nothing..
 * 
 * And that is cool. what makes it cooler is if it was:
 * - I dont have to compile and upload and be responsible for docs.
 * - I can see all some changes in the manual as its done automatically.
 * - My curiosiry of what does this function in flightgear, 
 *   leads me into simgear then to source of osg, plib, ie interconnected manuals.
 * 
 * Solution:
 *  - We Dont rely on anyone elses docs, we instead create out won reliable one were in control of.
 *  - We need to be in control of the documentation process to represent the "head" as in concert with devs.
 * 
 * 
 * To do this 
 * - We attain the source code, and output in a way we like it
 * 
 * Doxygen works by:
 *  - Creating a Config file
 *  - Then changing a few settings
 *  - Then run the Document Generation
 *    \code 
 *     doxygen ./docx/doxy.conf
 *    \endcode
 * 
 * \section problems Problems
 * 
 * The problem is that noone really focused on documentation. Its a pain.
 * But its also a valuable tool is we can all reely upon.
 * 
 * One of the frustrating things with documentation, its that a lot of the stuff is missing.
 * For example a small project can miss completely the other major library..
 * 
 * \section current Current Scenario
 * 
 * - this project
 * 
 * - requirements
 *  python-yaml
 * python-git
 * doxygen 1.8+
 * 
 * 
 * 
 * \page general How it works.
 * 
 * It was decided to use python for scripting as this has more libs
 * to use, such as pyGit, yaml, urllib etc
 * 
 * The process is to:
 *  - Create the temp/ directory for project
 *  - Create the build/ directory ie the www_root/
 *  - Checkout a repository (tried git externals with difficulties)
 * 
 * 
 * \section config Configuration
 * 
 * The configuration is within the yaml
 * 
 */