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
    parser.add_argument('query_dir',
                        metavar='query directory',
                        type=str,
                        help=help_str)

    help_str = "The canonical directory."
    parser.add_argument('canonical_dir',
                        metavar='canonical directory',
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

    help_str = "One or more config files that contain all of the compare parameters that you would otherwise " \
               "supply via the command line (things like which files to skip or regex's to use as filters). You " \
               "may use this option more than once if you have multiple config files you wish to use. If you do " \
               "supply more than one config file, the regex settings in the config files will be merged. The skip " \
               "parameters will be taken only from the first listed config file. If you also supply command line " \
               "parameters, then the command line regex patterns will be merged with those from the config file or "\
               "files. Any boolean settings (such as the which files to skip) will be taken from the command line " \
               "and will supercede any settings in the config file.     \n\nExample:\n\n     " \
               "-C /path/to/config/fileA.cfg -C /path/to/config/fileB.cfg"
    parser.add_argument("-C",
                        dest="config_paths",
                        type=str,
                        action="append",
                        help=help_str)

    help_str = "Saves the settings passed via the command line to the specified config file without actually " \
               "running the compare operation. If the config file already exists, you will be prompted as to whether " \
               "you wish to overwrite it. If you also included other config files via the -C option, the contents of " \
               "those config files (subject to the limitations described in the -C option) will be merged as part of " \
               "this saved config file, effectively merging the various configs into a single file."
    parser.add_argument("-w",
                        dest="config_path",
                        type=str,
                        action="store",
                        help=help_str)

    return parser
