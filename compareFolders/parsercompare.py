#! /usr/bin/env python3
"""
A module to manage command line parsing for the compareFolders command.
"""
from argparse import ArgumentParser
import os.path
import sys

import displaylib

help_msg = f"""
A program to compareFolders all of the files in a query directory to the files in a
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

class Parser(object):
    """
    A class to manage a single argparse object.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 commandline_args):
        """
        Creates and initializes the parser object.

        :param commandline_args: The arguments passed on the command line.

        :return: Nothing.
        """

        self.parser = ArgumentParser(description=help_msg)

        help_str = "The query directory."
        self.parser.add_argument('query_dir',
                                 metavar='query directory',
                                 type=str,
                                 help=help_str)

        help_str = "The canonical directory."
        self.parser.add_argument('canonical_dir',
                                 metavar='canonical directory',
                                 type=str,
                                 help=help_str)

        help_str = "If provided, the results of the comparison operation will be written to this log file on disk " \
                   "as a comma separated text file. If the file already exists, you will be prompted as to whether " \
                   "you wish to overwrite it."
        self.parser.add_argument("-o",
                                 dest="output_file",
                                 type=str,
                                 action="store",
                                 default=None,
                                 help=help_str)

        help_str = "The names of the files must match in order for the files to be considered duplicates. The use of "\
                   "this option automatically disables the -t (match on type) options since that would be a redundant "\
                   "check."
        self.parser.add_argument("-n",
                                 dest="match_on_name",
                                 action="store_true",
                                 help=help_str)

        help_str = "The names of the immediate parent directory of each file must match in order for the files to be " \
                   "considered duplicates."
        self.parser.add_argument("-p",
                                 dest="match_on_parent",
                                 action="store_true",
                                 help=help_str)

        help_str = "The file types (extensions) of the files must match in order for the files to be considered " \
                   "duplicates."
        self.parser.add_argument("-t",
                                 dest="match_on_type",
                                 action="store_true",
                                 help=help_str)

        help_str = "The full relative paths of the files must match in order for the files to be considered " \
                   "duplicates. The use of this option automatically disables the -p (match on parent) options since " \
                   "that would a redundant check."
        self.parser.add_argument("-r",
                                 dest="match_on_relpath",
                                 action="store_true",
                                 help=help_str)

        help_str = "The creation date and time of the files must match in order for the files to be considered " \
                   "duplicates."
        self.parser.add_argument("-c",
                                 dest="match_on_ctime",
                                 action="store_true",
                                 help=help_str)

        help_str = "The modification date and time of the files must match in order for the files to be considered "\
                   "duplicates."
        self.parser.add_argument("-m",
                                 dest="match_on_mtime",
                                 action="store_true",
                                 help=help_str)

        help_str = "Skip the checksum and only compareFolders on the name, file size, and any other (optional) metrics " \
                   "listed above. Note: using this option automatically also enables the -n (match on name)" \
                   "option."
        self.parser.add_argument("-S",
                                 dest="skip_checksum",
                                 action="store_true",
                                 help=help_str)

        help_str = "Skip sub-directories of the scanned directories."
        self.parser.add_argument("--skip-subdir",
                                 dest="skip_sub_dir",
                                 action="store_true",
                                 help=help_str)

        help_str = "Include hidden files in the comparison."
        self.parser.add_argument("--include-hidden",
                                 dest="include_hidden",
                                 action="store_true",
                                 help=help_str)

        help_str = "Include zero length files in the comparison."
        self.parser.add_argument("--include-zero-length",
                                 dest="include_zero_length",
                                 action="store_true",
                                 help=help_str)

        help_str = "Regular expression(s) to control directory names that are INCLUDED in the scan. Only those " \
                   "directories that MATCH these regular expressions WILL be scanned. You may use this option more " \
                   "once if you have multiple regular expressions you wish to include. Always enclose the regular " \
                   "expression in quotes to avoid the shell interpreting the characters passed.\n\nExample:\n\n     " \
                   "--idr \"geo.*\" --idr \"music.*\""
        self.parser.add_argument("--idr",
                                 dest="incl_dir_regexes",
                                 type=str,
                                 action="append",
                                 help=help_str)

        help_str = "Regular expression(s) to control directory names that are EXCLUDED from the scan. Any " \
                   "directories that match these regular expressions WILL NOT be scanned. You may use this option " \
                   "more once if you have multiple regular expressions you wish to include. Always enclose the " \
                   "regular expression in quotes to avoid the shell interpreting the characters passed." \
                   "\n\nExample:\n\n     --edr \"temp.*\" --edr \"trash.*\""
        self.parser.add_argument("--edr",
                                 dest="excl_dir_regexes",
                                 type=str,
                                 action="append",
                                 help=help_str)

        help_str = "Regular expression(s) to control file names that are INCLUDED in the scan. Only those files that " \
                   "MATCH these regular expressions WILL be included in the comparison. You may use this option more " \
                   "once if you have multiple regular expressions you wish to include. Always enclose the regular " \
                   "expression in quotes to avoid the shell interpreting the characters passed.\n\nExample:\n\n     " \
                   "--ifr \"final_.*\" --ifr \"finished_.*\""
        self.parser.add_argument("--ifr",
                                 dest="incl_file_regexes",
                                 type=str,
                                 action="append",
                                 help=help_str)

        help_str = "Regular expression(s) to control file names that are EXCLUDED from the scan. Any files that " \
                   "MATCH these regular expressions WILL NOT be included in the comparison. You may use this option " \
                   "more once if you have multiple regular expressions you wish to include. Always enclose the " \
                   "regular expression in quotes to avoid the shell interpreting the characters passed." \
                   "\n\nExample:\n\n     --efr \"delete_me_.*\" --efr \"old_.*\""
        self.parser.add_argument("--efr",
                                 dest="excl_file_regexes",
                                 type=str,
                                 action="append",
                                 help=help_str)

        help_str = "One or more config files that contain all of the compareFolders parameters that you would otherwise " \
                   "supply via the command line (things like which files to skip or regex's to use as filters). You " \
                   "may use this option more than once if you have multiple config files you wish to use. If you do " \
                   "supply more than one config file, the regex settings in the config files will be merged. The " \
                   "skip parameters will be taken only from the first listed config file. If you also supply command " \
                   "line parameters, then the command line regex patterns will be merged with those from the config "\
                   "file or files. Any boolean settings (such as the which files to skip) will be taken from the " \
                   "command line and will supersede any settings in the config file.     \n\nExample:\n\n     " \
                   "-C /path/to/config/fileA.cfg -C /path/to/config/fileB.cfg"
        self.parser.add_argument("-C",
                                 dest="config_paths",
                                 type=str,
                                 action="append",
                                 help=help_str)

        help_str = "Saves the settings passed via the command line to the specified config file without actually " \
                   "running the compareFolders operation. If the config file already exists, you will be prompted as to " \
                   "whether you wish to overwrite it. If you also included other config files via the -C option, the " \
                   "contents of those config files (subject to the limitations described in the -C option) will be " \
                   "merged as part of this saved config file, thereby merging the various configs into a single file."
        self.parser.add_argument("-w",
                                 dest="config_path",
                                 type=str,
                                 action="store",
                                 help=help_str)

        self.args = self.parser.parse_args(commandline_args)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self):
        """
        Validates that the command line arguments are valid. Raises an appropriate error if any of the checks fail
        validation.

        :return: Nothing.
        """

        if self.args.skip_checksum:
            self.args.match_on_name = True

        if self.args.match_on_relpath:
            self.args.match_on_parent = False

        if self.args.match_on_name:
            self.args.match_on_type = False

        if self.args.config_paths:
            for path in self.args.config_path:
                if not os.path.exists(path) or os.path.isdir(path):
                    raise FileNotFoundError(f"Config file does not exist or it is a directory: {path}")

        if self.args.config_path:
            config_path_parent = os.path.split(self.args.config_path)[0]

            if os.path.exists(self.args.config_path) and os.path.isdir(self.args.config_path):
                raise FileNotFoundError(f"Config file is not a file (it is a directory): {self.args.config_path}")

            if not os.path.exists(config_path_parent) or not os.path.isdir(config_path_parent):
                raise NotADirectoryError(f"Config file path does not contain a valid directory: {config_path_parent}")

            if os.path.exists(self.args.config_path) and not os.access(self.args.config_path, os.W_OK):
                raise PermissionError(f"You do not have permissions to write to the file: {self.args.config_path}.")

            if os.path.exists(self.args.config_path):
                raise FileExistsError(f"Config file already exists: {self.args.config_path} ")

        if self.args.output_file is not None:

            if os.path.exists(self.args.output_file):
                yes = "{{BRIGHT_YELLOW}}Y{{COLOR_NONE}}es"
                no = "{{BRIGHT_YELLOW}}N{{COLOR_NONE}}o"
                quitapp = "{{BRIGHT_YELLOW}}Q{{COLOR_NONE}}uit"
                prompt = f"\n\nOutput file ({self.args.output_file}) already exists. Overwrite? ({yes}/{no}/{quitapp} "
                prompt = displaylib.format_string(prompt)
                result = input(prompt)
                if result.lower() in {"quit", "q", "no", "n"}:
                    sys.exit(0)

            if not os.path.isdir(os.path.split(self.args.output_file)[0]):
                raise NotADirectoryError(f"{self.args.output_file} is not a valid path")
