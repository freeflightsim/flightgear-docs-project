/**
 * @file DoxyMain-fgdocs.cpp
 * 
 * \mainpage Projects Index
 * 
 * The projects below are automatically updated daily. See \ref About 
 * 
 * \htmlinclude projects_index.html
 * 
 * 
 * \section Latest Latest Updates
 * - Switched on the graph creation with DOT
 * - TREE_VIE is dea
 * - SHOW_DIREECTORIES is head (need remove file from code)
 * 
 * 
 * 
 *****************************************************
 * \page About About the Docs Project
 * 
 * \section intro Introduction
 * The \a 'tool' of this project is \ref Doxygen, a c++ tool to parse source code and then output
 * into various formats; the one we are interested in is \b html.
 * 
 * \ref Doxygen is a very clever application, you can throw anything at it and it tries
 * to make sense of code, create some docmentation out of nothing sometimes.
 * 
 * @note The pages you are looking at now on this website, 
 * were generated from the \b fg-docs project (yes this project is self documenting, and also a doxygen project)
 * 
 * \section Goals Goals
 * - The objective is to autocreate the docs from source
 * - Make it a reliable endpoint for everyone to referance at
 * - Update the docs regularily aaautom magically 
 *   - Current using jenkins, currently thanks FGx project at http://jenkins.fgx.ch 
 * - Create a presentable and useful interface
 * - Make the documentation interlink, ie linking flightgear, simgear, osg together
 * 
 * \subsection basic_doxygen Basic Doxygen
 * To create documentatio/terragear/n for a project is a simple three step process
 * -# Create a doxygen config file for your project with the \b -g generate option
 *    \code
 *    cd my_project
 *    doxygen -g my_doxy.conf
 *    \endcode
 * -# Edit the config file to taste; important vars are:
 *    \code
 *    PROJECT_NAME = "My Project"
 *   
 *    # Adding two directories and a single file recursively
 *    INPUT = src/ foo/ main_docs_page.cpp
 *    RECURSIVE = YES
 * 
 *    # The output path and formats
 *    OUTPUT_DIRECTORY = build_docs/
 *    GENERATE_LATEX = NO
 *    GENERATE_MAN = NO
 *    GENERATE_HTML = YES
 *    \endcode
 * -# Then generate the docs
 *    \code
 *    doxygen ./my_doxy.conf
 *    \endcode
 *    Then open \b build_docs/html/index.html in your browser
 * 
 * \subsection advanced_doxygen Advanced Usage and Configration
 * For advanced usage, were using some key features such as:
 *  - \ref GENERATE_TAGFILE - When a project is documented, is creates an xml formatted tag file for the project
 *  - \ref TAGFILES - Integrate with other projects
 *  - Customation of the site with headers and footers
 * 
 * Each iteration of |ref Doxygen brings rich features and
 * - New Features - Latest version will have new features
 * - Depreceated Features - Stuff not used anymore
 * 
 * 
 * \section problems Problems
 * \ref Doxygen can be configured to 
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
 *****************************************************
 * \page Links Links
 * 
 * \section Doxygen
 *  (http://doxygen.org)
 *  Were using the altest compiled 1.8 series as this has better output
 * 
 * \subsection GENERATE_TAGFILE GENERATE_TAGFILE
 * This option creates an .xml file with the tags. This can be read by
 * other documentation projects. 
 * \code
 * # OSG config for creating a tag
 * GENERATE_TAGFILE = /build_dir/osg/osg.tag
 * \endcode
 * 
 * \subsection TAGFILES TAGFILES
 * This option links to other tag files in other project
 * \code
 * # Simgear config reads osg and plib tags
 * TAGFILES = /build_dir/osg/osg.tag /build_dir/plib/plib.tag
 * \endcode
 * 
 * 
 * *****************************************************************
 * \page crash_course Crash Course
 * A few things affect the output from source code. 
 * There is also the dilemaa os throwing stuff at doxygen and see wat coomes out
 * 
 * 
 ******************************************************************* 
 * \page doxy_default default-doxy.conf
 * - Below are the contents of the default-doxy.conf file
 *
 * \include  default-doxy.conf
 * 
 * 
 ******************************************************************* 
 * \page config_yaml Configuration with config.yaml
 * - The build configuration is contained within the file \b config.yaml. 
 * - The configuration is loaded by \ref Config and ProjectConfig
 * 
 * \section config_directives Config Directives
 * The format is explained with
 * the plib example. This is parsed from the yaml file to a python dictionary
 * \code
 plib:
    title: Portable Game Library
    runlevel: 10
    color: "#539053"
    version: 
        number: 1.8.5
    repo: svn
    checkout: https://plib.svn.sourceforge.net/svnroot/plib/trunk
    official: 1
    copy:
      - etc/DoxyMain-plib.cpp
    doxy_args:
       INPUT: DoxyMain-plib.cpp src/
       HTML_COLORSTYLE_HUE: 120
       HTML_COLORSTYLE_SAT: 80
       HTML_COLORSTYLE_GAMMA: 220
 * \endcode 
 * - \b plib - is the project key, and output directory. Must be unique.
 * 
 * \subsection title_config title:
 *  The title of the project, will appear in indexed as titles
 * \subsection color_config color: 
 *  This is the css color used on the index page. 
 *  @warning MUST be enclosed in double quotes <code>"#aabbcc"</code>
 * 
 * \subsection  runlevel_config  runlevel:  
 *  Some project need to be build before others, eg osg and plib before simgear. 
 *                 When buildall is run, the list is sorted by this order
 *                 - \b 0 - Runs first, no dependancies
 *                 - \b 100 - Reserved for \b fg-docs This project must be suild last
 * \subsection version_config Version Config:
 * The version requires either:
 *  - the \b number: eg <code>number: 1.8.5</code> 
 *  - or a \b file: eg <code>file: version.txt</code> in the project directory
 *  - If both are present, \b file: comes after \b number:
 *  - If neither is present <b>-na-</b> is presented
 *  @see ::Project.get_version()
 * 
 * \subsection repo_config repo: 
 *   The kind of repo: either \b git or \b svn
 * 
 * \subsection checkout_config checkout: 
 *  The url for checking out
 *
 * \subsection branch_config branch: 
 *  The git branch to checkout, defaults to \b master
 * 
 * \subsection official_config official: 
 *  TBA, the idea is to recognise upstream
 * 
 * \subsection copy_config copy: 
 * A list of file to copy from the ROOT to the project temp dir
 * - \b doxy_file: The doxy file to use, if there is one, otherwise omit
 * \subsection doxy_args_conf doxy_args: 
 * A list of doxygen config args. This is appended to the doxy source and overries settings.
 * 
 * \section tags_config Tags Config
 * The "tag" project are interlinked,
 * \code
 * tag: simgear plib osg
 * \endcode
 * 
 * \section current_config Current Config
 * \include config.yaml
 * 
 * 
 **************************************************************************** 
 * \page build_process The Build Process
 * 
 * 
 * \section build_steps How it works
 * - Checkout the project from https://git.gitorious.org/~ffs/flightgear-docs-project
 * - Run the script which completed the steps below
 *   \code
 *   fgdocs.py buildall
 *   \endcode
 *   -# Reads the \ref Projects config from \ref config_yaml
 *   -# Sorts the projects via \ref runlevel. \b fg-docs itself is 100 = last
 *   -# Runs build_project() for each project
 *    - Checks if its either a git or svn repos
 *      - Checks out the repo if is doesnt exist ie new
 *      - Updates the reps with <code>git pull,  svn up</code>
 *    - Copies across the required files to build
 *    - Create doxy file by either:
 *      - Read an existing doxy file if in the configuration and found
 *      - Or use the \ref doxy_default (eg no doxy file in project)
 * The process is to:
 *  - Create the temp/ directory for project
 *  - Create the build/ directory ie the www_root/
 *  - Checkout a repository (tried git externals with difficulties)
 * 
 * 
 * \section Requirements
 * @note It was decided to use python for scripting as this has more libs to automate the process. 
 * 
 * The following is required on the target machine
 * - \b git
 * - \b svn
 * - \b python
 *   - \b python-svn
 *   - \b python-git
 *   - \b python-yaml
 *   - \b python-simplejson
 * - \ref Doxygen - must be version 1.8+ (currently compiled on a dedicated)
 * 
 * 
 * 
 * \section config Configuration
 * 
 * The configuration is within the yaml
 * 
 */
