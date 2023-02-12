#! /usr/bin/env python3
"""
A module to manage command line parsing for the deleteDuplicates command.
"""
from argparse import ArgumentParser
import os.path
import sys

import displaylib

help_msg = f"""
A program to delete files that were identified as duplicates by the compareFolders app. This app requires
that the compareFolders app be run first using the -o (output file) option. That output file which lists
the results of the comparison operation is used to determine which files to delete.

By default, the delete files operation runs a sanity check before deleting each file. This can be as simple as
comparing the file size to make sure the files are still likely to be identical before deleting the duplicate file
in the query directory. But it can also run a checksum to make sure that the two files are actually bit for bit
identical before deleting. This will, of course, add a fair bit of time to the delete operation. Additional checks,
like whether the names match, the parent directory matches, the relative path matches, etc. can also be applied as
part of this sanity check. But these can only be applied if they had been used in the original compareFolders
operation.

Additional options include simply renaming the files with the prefix: "compareFoldersPendingDelete_" instead of actually
deleting the files.
"""


class Parser(object):
    """
    A class to manage a single argparse object.
    """

    # ----------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 commandline_args):
        """
        Creates and initializes the parser object for the deleteFiles command.

        :param commandline_args: The arguments passed on the command line.

        :return: Nothing.
        """

        self.parser = ArgumentParser(description=help_msg)

        help_str = "The log file written out by the compareFolders command."
        self.parser.add_argument('log_file',
                                 metavar='log_file',
                                 type=str,
                                 help=help_str)

        help_str = "Perform a check to ensure that the MD5 checksum of each file matches before deleting or " \
                   "renaming. By default each file is checked using the same comparison operations performed by the " \
                   "original compareFolders session. Size is always compared. Name, Parent Directory Name, Relative " \
                   "Path, File Type, Creation Time, and Modification Time will also be compared if any of these were " \
                   "used in the original compareFolders session. But a checksum is NOT automatically run. Use this " \
                   "option to force the checksum. Note: this will slow down the delete or rename operation by a " \
                   "significant amount."
        self.parser.add_argument("-c",
                                 dest="checksum",
                                 action="store_true",
                                 help=help_str)

        help_str = "Rename files instead of deleting them. A prefix of \"compareFoldersPendingDelete_\" will be " \
                   "added to the beginning of each file that would otherwise be deleted."
        self.parser.add_argument("-r",
                                 dest="rename",
                                 action="store_true",
                                 help=help_str)

        help_str = "Trial run. This will print out any actions that would have been taken (deleting or renaming) " \
                   "instead of actually renaming or deleting any files. Use the -s option to force the trial to run " \
                   "without printing out any commands."
        self.parser.add_argument("-t",
                                 dest="trial",
                                 action="store_true",
                                 help=help_str)

        help_str = "Silent trial. This will prevent the trial run from displaying any information. The trial is " \
                   "still performed, but the outputs mimic that of a real run."
        self.parser.add_argument("-s",
                                 dest="silent_trial",
                                 action="store_true",
                                 help=help_str)

        self.args = self.parser.parse_args(commandline_args)

    # ------------------------------------------------------------------------------------------------------------------
    def validate(self):
        """
        Validates that the command line arguments are valid. Raises an appropriate error if any of the checks fail
        validation.

        :return: Nothing.
        """

        if not os.path.exists(self.args.log_file):
            raise FileNotFoundError(f"Log file does not exist: {self.args.log_file}")

        if os.path.isdir(self.args.log_file):
            raise FileNotFoundError(f"Log file path is actually a directory: {self.args.log_file}")

        if os.path.islink(self.args.log_file):
            raise FileNotFoundError(f"Log file path is actually a symlink: {self.args.log_file}")
