import os
from os.path import basename,dirname,join
from pathlib import PureWindowsPath

def create_target_path_from_root(target,root=PureWindowsPath(os.getcwd()).drive+"\\"):
    
    dir_seq=[]
    folder=target
    while folder!=root:
        bname=basename(folder)
        dir_seq.append(bname)
        folder=dirname(folder)
    mktarget=root
    for folder in reversed(dir_seq):
        mktarget=join(mktarget,folder)
        if not os.path.exists(mktarget):
            print(mktarget)
            os.mkdir(mktarget)

def main():
    cwd=os.getcwd()
    folder_seq=['folderA','folderB']

    root=cwd
    mktarget=join(cwd,*folder_seq)
    create_target_path_from_root(target=mktarget,root=root)

if __name__ == '__main__':
    main()