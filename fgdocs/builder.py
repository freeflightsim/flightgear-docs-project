
import sys

from config import Config

class DocsBuilder:
    
    COMMANDS = ['build', 'buildall', 'view', 'clean', 'nuke']
    
    def __init__(self, parser, opts, args):
        
        ## Verbose
        self.V = opts.v
        
        ## Check there is a command
        if len(args) == 0:
            parser.error("Need to supply a command ")
            sys.exit(0)
  
        ## check commands exist
        if not args[0] in self.COMMANDS:
            parser.error("Command '%s' not recognised" % args[0] )
            sys.exit(0)
        self.command = args[0]
        
        """
        if self.V > 2:
            print "========================================================="
            print "options=", opts, opts.v
            print "args=", args
        
        """
        
        self.conf = Config()
                
        if len(args) == 0:
            parser.error("Need to supply a command")
            #parser.print_help()
            sys.exit(0)
        
        ## The command executed is the first var
        command = args[0]
        if V > 1:
            print "#> command=", command
        
