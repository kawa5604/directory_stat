#!/usr/bin/env python3

'''
Give information about a Linux directory.

It should take one or zero arguments of a directory (if none then use current directory).
It should then output the following in a formatted report:

Size of directory
Read/write/execute permissions and who has them
Number of sub directories total
Number of symbolic/hard links total
Number of files by each file type
Up to 5 largest files
Up to 5 largest directories
'''

# Number of symbolic/hard links total
import sys
import os


def arg_check(arguments):
    # Checking command line arguments
    # --> true if no arguments provided, so check the current directory
    # --> false if more than one arguments were provided
    if len(arguments) == 1:
        return os.getcwd()
    if len(arguments) == 2:
        if os.path.isdir(arguments[1]):
            return arguments[1]
        else:
            print("Argument provided was not a directory")
            sys.exit(2)

    if len(arguments) > 2:
        print("Wrong number of arguments provided.")
        print("Arguments provided: ", str(arguments))
        sys.exit(2)

def dir_size(dirToCheck):
    # Size of a directory
    info = os.stat(dirToCheck)
    # dirinfo = "The directory " + dirToCheck + " size: " + str(info.st_size) + "B"
    return info.st_size

def permissions(dirToCheck):
    # Read/write/execute permissions and who has them
    read = False
    write = False
    # execute = False --> doesnt work with dirs
    if os.access(dirToCheck,os.R_OK):
        # Read access
        read = True
    if os.access(dirToCheck, os.W_OK):
        write = True
    return read, write

def sub_dirs(dirToCheck):
    # Number of sub directories total
    # Number of sub directories total
    # --> list of files in the new directory
    subDirList = []
    subFileList = []
    subLinkList = []
    fileCount = 0
    dirCount = 0
    linkcount = 0

    for items in os.listdir(dirToCheck):
        # This will check for dirs
        if os.path.isdir(items):
            subDirList.append(items)
            dirCount = dirCount + 1
        # This will check for files
        if os.path.isfile(items):
            subFileList.append(items)
            fileCount = fileCount + 1
        # This will check for links
        if os.path.islink(dirToCheck):
            subLinkList.append(items)
            linkcount = linkcount + 1


    if not subDirList:
        subDirList.append("No subDirs")
    if not subFileList:
        subFileList.append("No files")
    return dirCount, subDirList, fileCount, subFileList, linkcount, subLinkList

def top_5(dirToCheck):
    # Up to 5 largest files
    # Up to 5 largest directories
    fileCommand = "du -a " + str(dirToCheck) + " |sort -n -r |head -n 5"
    print("Top 5 largest files & dirs within {}\n".format(dirToCheck))
    os.system(fileCommand)

'''
#pointless
def links(dirToCheck):
    path = str(dirToCheck)
    #os.system("find "+ path +" -maxdepth 1 -type l -ls")
    os.system("find . -maxdepth 1 -type l -print | cut -c3- | grep -v \"\#\"")
    import sys;
    print '\n'.join([os.path.join(sys.argv[1],i) for i in os.listdir(sys.argv[1]) if os.path.islink(os.path.join(sys.argv[1],i))])" / path / to / dir
'''
def main():
    dirToCheck = arg_check(sys.argv)
    print("\n")
    print("Path: {}".format(dirToCheck))
    size = dir_size(dirToCheck)
    print("Dir size: {}Bytes\n".format(size))
    read, write = permissions(dirToCheck)
    print("Directory Permissions: \nRead: {}, Write: {}\n".format(read, write))
    dirCount, dirList, fileCount, fileList, linkCount, subLinkList = sub_dirs(dirToCheck)
    print("{} SubDirectories: \n{}\n".format(dirCount, dirList))
    print("{} Files: \n{}\n".format(fileCount, fileList))
    print("{} Links: \n{}\n".format(linkCount, subLinkList))

    #links(dirToCheck)
    top_5(dirToCheck)
    print("\n\n")
if __name__ == "__main__":
    main()
