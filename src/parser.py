#! /usr/bin/env python3
"""
A module to manage command line parsing.
"""

from argparse import ArgumentParser

help_msg = f"""
A program to compare all of the files in a query directory to the files in a
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
"""


# ----------------------------------------------------------------------------------------------------------------------
def init_parser():
    """
    Creates and initializes the parser object.

    :return: An ArgumentParser object.
    """
    parser = ArgumentParser(description=help_msg)

    help_str = "The query directory."
    parser.add_argument('query directory',
                        metavar='query_dir',
                        type=str,
                        help=help_str)

    help_str = "The canonical directory."
    parser.add_argument('canonical directory',
                        metavar='canonical_dir',
                        type=str,
                        help=help_str)

    help_str = "The names of the files must match in order for the files to be considered duplicates."
    parser.add_argument("-n",
                        dest="match_on_name",
                        action="store_true",
                        help=help_str)

    help_str = "The names of the immediate parent directory of each file must match in order for the files to be " \
               "considered duplicates."
    parser.add_argument("-p",
                        dest="match_on_parent",
                        action="store_true",
                        help=help_str)

    help_str = "The file types (extensions) of the files must match in order for the files to be considered duplicates."
    parser.add_argument("-t",
                        dest="match_on_type",
                        action="store_true",
                        help=help_str)

    help_str = "The full relative paths of the files must match in order for the files to be considered duplicates."
    parser.add_argument("-r",
                        dest="match_on_relpath",
                        action="store_true",
                        help=help_str)

    help_str = "The creation date and time of the files must match in order for the files to be considered duplicates."
    parser.add_argument("-c",
                        dest="match_on_ctime",
                        action="store_true",
                        help=help_str)

    help_str = "The modification date and time of the files must match in order for the files to be considered "\
               "duplicates."
    parser.add_argument("-m",
                        dest="match_on_mtime",
                        action="store_true",
                        help=help_str)

    help_str = "Skip sub-directories of the scanned directories."
    parser.add_argument("--skip-subdir",
                        dest="skip_sub_dir",
                        action="store_true",
                        help=help_str)

    help_str = "Include hidden files in the comparison."
    parser.add_argument("--include-hidden",
                        dest="include_hidden",
                        action="store_true",
                        help=help_str)

    help_str = "Include zero length files in the comparison."
    parser.add_argument("--include-zero-length",
                        dest="include_zero_length",
                        action="store_true",
                        help=help_str)

    help_str = "Regular expression(s) to control directory names that are INCLUDED in the scan. Only those " \
               "directories that MATCH these regular expressions WILL be scanned. You may use this option more " \
               "once if you have multiple regular expressions you wish to include. Always enclose the regular " \
               "expression in quotes to avoid the shell interpreting the characters passed.\n\nExample:\n\n     " \
               "--idr \"geo.*\" --idr \"music.*\""
    parser.add_argument("--idr",
                        dest="incl_dir_regexes",
                        type=str,
                        action="append",
                        help=help_str)

    help_str = "Regular expression(s) to control directory names that are EXCLUDED from the scan. Any " \
               "directories that match these regular expressions WILL NOT be scanned. You may use this option more " \
               "once if you have multiple regular expressions you wish to include. Always enclose the regular " \
               "expression in quotes to avoid the shell interpreting the characters passed.\n\nExample:\n\n     " \
               "--edr \"temp.*\" --edr \"trash.*\""
    parser.add_argument("--edr",
                        dest="excl_dir_regexes",
                        type=str,
                        action="append",
                        help=help_str)

    help_str = "Regular expression(s) to control file names that are INCLUDED in the scan. Only those files that " \
               "MATCH these regular expressions WILL be included in the comparison. You may use this option more " \
               "once if you have multiple regular expressions you wish to include. Always enclose the regular " \
               "expression in quotes to avoid the shell interpreting the characters passed.\n\nExample:\n\n     " \
               "--ifr \"final_.*\" --ifr \"finished_.*\""
    parser.add_argument("--ifr",
                        dest="incl_file_regexes",
                        type=str,
                        action="append",
                        help=help_str)

    help_str = "Regular expression(s) to control file names that are EXCLUDED from the scan. Any files that " \
               "MATCH these regular expressions WILL NOT be included in the comparison. You may use this option more " \
               "once if you have multiple regular expressions you wish to include. Always enclose the regular " \
               "expression in quotes to avoid the shell interpreting the characters passed.\n\nExample:\n\n     " \
               "--efr \"delete_me_.*\" --efr \"old_.*\""
    parser.add_argument("--efr",
                        dest="excl_file_regexes",
                        type=str,
                        action="append",
                        help=help_str)

    return parser
