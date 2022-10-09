#! /usr/bin/env python3

import os.path
import re

from afile import AFile
from bysize import BySize
from byname import ByName
from byparent import ByParent
from bytype import ByType


class Scan(object):
    """
    A class to scan a single directory.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 scan_dir):
        """
        :param scan_dir: The directory to scan.
        """

        assert type(scan_dir) is str

        self.scan_dir = scan_dir

        self.bysize = dict()
        self.byname = dict()
        self.byparent = dict()
        self.bytype = dict()
        self.error_files = set()
        self.count = 0
        self.checked_count = 0
        self.error_count = 0
        self.skipped_zero_len = 0
        self.skipped_hidden = 0
        self.skipped_exclude = 0
        self.skipped_include = 0

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def create_afile_obj(file_path,
                         file_size=None):
        """
        Given a file path, creates an AFile object.

        :param file_path: The path to the file on disk.
        :param file_size: The size of the file. If None, then the size will be extracted from disk. Used in case the
               size has already been determined and, as such, may be passed in instead of having to calculate it a
               second time. Defaults to None.

        :return: an AFile object
        """

        if file_size is None:
            file_size = os.path.getsize(file_path)

        file_creation_date = os.stat(file_path).st_ctime  # Not always the creation time, but as close as it gets.
        file_modification_date = os.stat(file_path).st_mtime

        afile_obj = AFile(path=file_path,
                          size=file_size,
                          creation_date=file_creation_date,
                          modification_date=file_modification_date,
                          hidden=os.path.split(file_path)[1][0] == ".")

        return afile_obj

    # ------------------------------------------------------------------------------------------------------------------
    def add_by_size(self,
                    afile_obj):
        """
        Adds the afile_obj to the bysize collection.

        :param afile_obj: The afile object to add based on its size.

        :return: Nothing.
        """

        try:
            self.bysize[afile_obj.size].afile_objs.append(afile_obj)
        except KeyError:
            bysize_obj = BySize(afile_obj.size)
            bysize_obj.afile_objs.append(afile_obj)
            self.bysize[afile_obj.size] = bysize_obj

    # ------------------------------------------------------------------------------------------------------------------
    def add_by_name(self,
                    afile_obj):
        """
        Adds the afile_obj to the byname collection.

        :param afile_obj: The afile object to add based on its name.

        :return: Nothing.
        """

        try:
            self.byname[afile_obj.name].afile_objs.append(afile_obj)
        except KeyError:
            byname_obj = ByName(afile_obj.name)
            byname_obj.afile_objs.append(afile_obj)
            self.byname[afile_obj.name] = byname_obj

    # ------------------------------------------------------------------------------------------------------------------
    def add_by_parent(self,
                      afile_obj):
        """
        Adds the afile_obj to the byparent collection.

        :param afile_obj: The afile object to add based on its parent name.

        :return: Nothing.
        """

        try:
            self.byparent[afile_obj.parent_name].afile_objs.append(afile_obj)
        except KeyError:
            byparent_obj = ByParent(afile_obj.parent_name)
            byparent_obj.afile_objs.append(afile_obj)
            self.byparent[afile_obj.parent_name] = byparent_obj

    # ------------------------------------------------------------------------------------------------------------------
    def add_by_type(self,
                    afile_obj):
        """
        Adds the afile_obj to the bytype collection.

        :param afile_obj: The afile object to add based on its type.

        :return: Nothing.
        """

        try:
            self.bytype[afile_obj.file_type].afile_objs.append(afile_obj)
        except KeyError:
            bytype_obj = ByType(afile_obj.file_type)
            bytype_obj.afile_objs.append(afile_obj)
            self.bytype[afile_obj.parent_name] = bytype_obj

    # ------------------------------------------------------------------------------------------------------------------
    def scan(self,
             skip_sub_dir=False,
             skip_hidden=False,
             skip_zero_len=True,
             incl_dir_regex=None,
             excl_dir_regex=None,
             incl_file_regex=None,
             excl_file_regex=None,
             report_frequency=1000):
        """
        Triggers a scan of the directory.

        :param skip_sub_dir: If True, then no subdirectories will be included (only the top-level directory will be
               scanned. Defaults to False.
        :param skip_hidden: If True, then hidden files will be ignored in the scan. Defaults to False.
        :param skip_zero_len: If True, then files of zero length will be skipped. Defaults to True.
        :param incl_dir_regex: A regular expression to filter matching directories. Only those that match this regex
               will be INCLUDED. If None, no filtering will be done. Defaults to None.
        :param excl_dir_regex: A regular expression to filter matching directories. Those that match this regex
               will be EXCLUDED. If None, no filtering will be done. Defaults to None.
        :param incl_file_regex: A regular expression to filter matching files. Only those that match this regex
               will be INCLUDED. If None, no filtering will be done. Defaults to None.
        :param excl_file_regex: A regular expression to filter matching files. Those that match this regex
               will be EXCLUDED. If None, no filtering will be done. Defaults to None.
        :param report_frequency: After this many files have been scanned, report back to the calling function via a
               yield statement (to keep allow the calling function to report on the progress or interrupt it in some
               way.)  Defaults to 1000 files.

        :return: Nothing.
        """

        if self.scan_dir is None:
            raise IOError("No directory has been set to scan.")

        if not os.path.exists(self.scan_dir):
            #raise IOError(f"The directory {self.scan_dir} does not exist")
            raise IOError("The directory does not exist")

        if not os.path.isdir(self.scan_dir):
            #raise IOError(f"The path {self.scan_dir} is not a directory")
            raise IOError(f"The path is not a directory")

        for root, sub_folders, files in os.walk(self.scan_dir):

            root_name = os.path.split(root)[1]

            for file_name in files:

                self.checked_count += 1

                if self.checked_count % report_frequency == 0:
                    yield self.checked_count

                if skip_hidden and file_name[0] == ".":
                    self.skipped_hidden += 1
                    continue

                if incl_dir_regex is not None:
                    if re.match(incl_dir_regex, root_name) is None:
                        self.skipped_include += 1
                        continue

                if excl_dir_regex is not None:
                    if re.match(excl_dir_regex, root_name) is not None:
                        self.skipped_exclude += 1
                        continue

                if incl_file_regex is not None:
                    if re.match(incl_file_regex, file_name) is None:
                        self.skipped_include += 1
                        continue

                if excl_file_regex is not None:
                    if re.match(excl_file_regex, file_name) is not None:
                        self.skipped_exclude += 1
                        continue

                file_path = os.path.join(root, file_name)
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

                self.count += 1

                afile_obj = self.create_afile_obj(file_path)
                self.add_by_size(afile_obj)
                self.add_by_name(afile_obj)
                self.add_by_parent(afile_obj)
                self.add_by_type(afile_obj)

                if skip_sub_dir:
                    sub_folders[:] = []
