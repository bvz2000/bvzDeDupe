#! /usr/bin/env python3

import os.path
import re


class ScanDir(object):
    """
    A class to scan and store the attributes of every file in a single directory.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 scan_dir):
        """
        :param scan_dir: The directory to scan.
        """

        assert type(scan_dir) is str

        self.scan_dir = scan_dir

        self.error_files = set()

        self.initial_count = 0
        self.checked_count = 0
        self.skipped_links = 0
        self.error_count = 0
        self.skipped_zero_len = 0
        self.skipped_hidden = 0
        self.skipped_exclude = 0
        self.skipped_include = 0

    # ------------------------------------------------------------------------------------------------------------------
    def _get_metadata(self,
                      file_path):
        """
        Gets the metadata for the given file path.

        :param file_path: The path to the file to add

        :return: A dictionary of attributes.
        """

        attrs = dict()
        attrs["size"] = os.path.getsize(file_path)
        attrs["name"] = os.path.split(file_path)[1]
        attrs["file_type"] = os.path.splitext(attrs["name"])[1]
        attrs["parent"] = os.path.split(os.path.split(file_path)[0])[1]
        attrs["rel_path"] = os.path.relpath(file_path, self.scan_dir)
        attrs["ctime"] = os.stat(file_path).st_ctime  # Not always the creation time, but as close as it gets.
        attrs["mtime"] = os.stat(file_path).st_mtime

        return attrs

    # ------------------------------------------------------------------------------------------------------------------
    def _append_to_scan(self,
                        file_path,
                        metadata):
        """
        To be overridden in subclass

        :return: Nothing.
        """

        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def parameter_to_list(param_value):
        """
        Given a parameter (param_value) checks to see if it is a list or None. If so, the parameter is returned
        unchanged. If it is not a list and is not None, param_value is embedded in a list and that list is returned.

        :param param_value: The parameter value that is to be turned into a list if it is not already a list.

        :return: The param_value embedded in a list. If param_value is already a list or is None, returns param_value
                 unchanged.
        """

        if param_value is None:
            return None

        if type(param_value) is list:
            return param_value

        return [param_value]

    # ------------------------------------------------------------------------------------------------------------------
    def scan(self,
             skip_sub_dir=False,
             skip_hidden=False,
             skip_zero_len=True,
             incl_dir_regexes=None,
             excl_dir_regexes=None,
             incl_file_regexes=None,
             excl_file_regexes=None,
             report_frequency=1000):
        """
        Triggers a scan of the directory.

        :param skip_sub_dir: If True, then no subdirectories will be included (only the top-level directory will be
               scanned). Defaults to False.
        :param skip_hidden: If True, then hidden files will be ignored in the scan. Defaults to False.
        :param skip_zero_len: If True, then files of zero length will be skipped. Defaults to True.
        :param incl_dir_regexes: A regular expression (or list of regular expressions) to filter matching directories.
               Only those that match this regex will be INCLUDED. If None, no filtering will be done. Defaults to None.
        :param excl_dir_regexes: A regular expression (or list of regular expressions) to filter matching directories.
               Those that match this regex will be EXCLUDED. If None, no filtering will be done. Defaults to None.
        :param incl_file_regexes: A regular expression (or list of regular expressions) to filter matching files. Only
               those that match this regex will be INCLUDED. If None, no filtering will be done. Defaults to None.
        :param excl_file_regexes: A regular expression (or list of regular expressions) to filter matching files. Those
               that match this regex will be EXCLUDED. If None, no filtering will be done. Defaults to None.
        :param report_frequency: After this many files have been scanned, report back to the calling function via a
               yield statement (to keep allow the calling function to report on the progress or interrupt it in some
               way.)  Defaults to 1000 files.

        :return: Nothing.
        """

        if not self.scan_dir:
            raise IOError("No directory has been set to scan.")

        if not os.path.exists(self.scan_dir):
            raise IOError(f"The directory {self.scan_dir} does not exist")

        if not os.path.isdir(self.scan_dir):
            raise IOError(f"The path {self.scan_dir} is not a directory")

        incl_dir_regexes = self.parameter_to_list(incl_dir_regexes)
        excl_dir_regexes = self.parameter_to_list(excl_dir_regexes)
        incl_file_regexes = self.parameter_to_list(incl_file_regexes)
        excl_file_regexes = self.parameter_to_list(excl_file_regexes)

        for root, sub_folders, files in os.walk(self.scan_dir):

            root_name = os.path.split(root)[1]

            for file_name in files:

                self.checked_count += 1

                if self.checked_count % report_frequency == 0:
                    yield self.checked_count

                if skip_hidden and file_name[0] == ".":
                    self.skipped_hidden += 1
                    continue

                if incl_dir_regexes:
                    for incl_dir_regex in incl_dir_regexes:
                        if re.match(str(incl_dir_regex), root_name) is None:
                            self.skipped_include += 1
                            continue

                if excl_dir_regexes is not None:
                    for excl_dir_regex in excl_dir_regexes:
                        if re.match(str(excl_dir_regex), root_name) is not None:
                            self.skipped_exclude += 1
                            continue

                if incl_file_regexes is not None:
                    for incl_file_regex in incl_file_regexes:
                        if re.match(str(incl_file_regex), file_name) is None:
                            self.skipped_include += 1
                            continue

                if excl_file_regexes is not None:
                    for excl_file_regex in excl_file_regexes:
                        if re.match(str(excl_file_regex), file_name) is not None:
                            self.skipped_exclude += 1
                            continue

                file_path = os.path.join(root, file_name)

                if os.path.islink(file_path):
                    self.skipped_links += 1
                    continue

                try:
                    file_size = os.path.getsize(file_path)
                except FileNotFoundError:
                    self.error_files.add(file_path)
                    self.error_count += 1
                    continue

                if skip_zero_len:
                    if file_size == 0:
                        self.skipped_zero_len += 1
                        continue

                self.initial_count += 1

                file_metadata = self._get_metadata(file_path)

                self._append_to_scan(file_path=file_path,
                                     metadata=file_metadata)

                if skip_sub_dir:
                    sub_folders[:] = []
