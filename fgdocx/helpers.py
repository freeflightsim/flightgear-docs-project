## @package fgdocs
# Helper functions


## Read a text file and return its contents
# @param path_to_file
# @retval str with file content
def read_file(path_to_file):
    fob = open( path_to_file, "r")
    file_content = fob.read()
    fob.close()
    return file_content

## Write text string to file path
# @param path_to_file
# @param contents string with contents to write
def write_file(path_to_file, contents):
    fob = open( path_to_file, "w")
    fob.write(contents)
    fob.close()
    return#

def xsplit(v, char):
    v = v.strip()
    parts = v.split(char)
    ret = []
    for p in parts:
        if p != "":
            ret.append(p)
    return ret