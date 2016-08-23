import sys
import os
from os.path import join,relpath
from glob import glob

def main():
    argv=sys.argv
    argc=len(argv)

    print (argv)
    print (argc)

    if(argc not in {2,3}):
        print("usage: python %s (folder's relative path)\n"% argv[0])
        print("or\n")
        print("usage: python %s (folder's relative path) (extension))\n"% argv[0])
        quit()

    extension='.txt'
    if(argc==3):
        condi=argv[2]
    basedir=os.path.dirname(__file__)
    reldir=argv[1]
    search_dir=join(basedir,reldir)
    files=[relpath(x,search_dir) for x in glob(join(search_dir, '*'+extension))]
    print(files)
if __name__ == '__main__':
    main()
