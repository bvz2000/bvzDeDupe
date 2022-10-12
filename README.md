# bvzDeDupe
A script to help identify and de-duplicate files on disk.

Current usage (testing only):

dedupe {path to query directory} {path to canonical directory}

Currently, able to scan two directories and compare their contents. 

HAS A PRETTY MAJOR FLAW IN HOW IT DECIDES WHICH FILES TO COMPARE!!!!
DO NOT USE FOR REAL COMPARISON WORK!!!

(You may safely run this script since it only reads information, and never changes anything on disk, but do not rely on it's output for any real work yet.)