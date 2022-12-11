# bvzDeDupe
A script to help identify and de-duplicate files on disk.

Current usage (STILL IN ALPHA PHASE):

A program to compare all the files in a query directory to the files in a
canonical directory and list any which are duplicates. The query directory is
the directory where you may have a bunch of files that may or may not already
exist in another location (the canonical location where they are supposed to
reside). Using this program you can decide whether you need to copy the files
from the query directory to the canonical location, or whether these files
already exist in the canonical directory and may therefore be deleted from the
query directory. Note: This program DOES NOT actually touch any files on disk.
It merely reports on duplicates.

You may decide which characteristics are considered when deciding whether two
files are duplicates of each other or not.

The possible characteristics are listed below. If you do not indicate any
characteristics using the options provided, then the only thing that is considered
is whether the contents of the files are identical, regardless of the file name,
date, or location in the directory structure.

Usage: dedupe <query directory> <canonical directory> <-n -p -t -r -c -m -h>

-n    The names of the files must match in order for the files to be considered 
      duplicates.

-p    The names of the parent directories of the files must match in order for 
      the files to be considered duplicates.

-t    The file types (extensions) of the files must match in order for the files 
      to be considered duplicates.

-r    The relative paths of the files must match in order for the files to be 
      considered duplicates.

-c    The creation date and time of the files must match in order for the files 
      to be considered duplicates.

-m    The modification date and time of the files must match in order for the 
      files to be considered duplicates.

-h    Show this help string and exit.

Note: Each option must have its own hyphen (dash). For example, You may not do this: -nptrcm. 
      You must do this: -n -p -t -r -c -m.