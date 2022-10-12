#! /usr/bin/env python3

import os.path
import re

from afile import AFile


class Scan(object):
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

        self.afile_objs = dict()

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
    @staticmethod
    def create_afile_obj(file_path,
                         rel_path,
                         file_size=None):
        """
        Given a file path, creates an AFile object.

        :param file_path: The path to the file on disk.
        :param rel_path: The relative path to the file (relative to the scan directory)
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
                          rel_path=rel_path,
                          size=file_size,
                          creation_date=file_creation_date,
                          modification_date=file_modification_date,
                          hidden=os.path.split(file_path)[1][0] == ".")

        return afile_obj

    # ------------------------------------------------------------------------------------------------------------------
    def scan(self,
             compare_on_name=False,
             compare_on_parent_name=False,
             compare_on_rel_path=False,
             compare_on_cdate=False,
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

        :param compare_on_name: If True, then the name of the files will have to match in order for two files to be
               considered identical.
        :param compare_on_parent_name: If True, then the name of the files' parent directory will have to match in order
               for two files to be considered identical.
        :param compare_on_rel_path: If True, then the full relative path of the files will have to match in order for
               two files to be considered identical.
        :param compare_on_cdate: If True, then the creation date of the files will have to match in order for two files
               to be considered identical.
        :param skip_sub_dir: If True, then no subdirectories will be included (only the top-level directory will be
               scanned). Defaults to False.
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
            raise IOError(f"The directory {self.scan_dir} does not exist")

        if not os.path.isdir(self.scan_dir):
            raise IOError(f"The path {self.scan_dir} is not a directory")

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

                rel_path = os.path.relpath(file_path, self.scan_dir)
                afile_obj = self.create_afile_obj(file_path, rel_path=rel_path)

                if compare_on_name:
                    name = afile_obj.name
                else:
                    name = None

                if compare_on_parent_name:
                    parent_name = afile_obj.parent_name
                else:
                    parent_name = None

                if compare_on_cdate:
                    cdate = afile_obj.creation_date
                else:
                    cdate = None

                # TODO: Here is the conundrum. If I include the relative path each time, then only files with the same
                #  relative path will match. But if I leave it out, then if more than one file has the same size, the
                #  very last one that is scanned will clobber the others in the dictionary. Even if I do include the
                #  relative path, if more than one file has the same size INSIDE of that path, then the same issue
                #  occurs. The only way I know to solve this is to have the top-level dictionary only key on size, and
                #  then have each item in that dictionary contain a dictionary keyed on all of the other categories. But
                #  then I wind up with the same convoluted code that I had before... sigh. Ideally I would have just the
                #  single dict with all of the key elements filled in (relative path, name, size, etc.) but when I
                #  compare keys I would be able to do it only on certain elements of this... which may actually be
                #  possible. I am just comparing entire keys, but what if I compared the key tuples element by element?
                #  .
                #  But in any event, the code below will fail to correctly identify duplicates because it only works on
                #  duplicates in the same relative path, and will potentially fail to match duplicates if more than one
                #  file in the relative path shares the same size. So it is BROKEN!!!!! and should NOT be trusted.
                key = (rel_path, afile_obj.size, name, parent_name, cdate)
                self.afile_objs[key] = afile_obj

                if skip_sub_dir:
                    sub_folders[:] = []

    # ------------------------------------------------------------------------------------------------------------------
    def keys(self):
        """
        Yields each key from the afile_objs dict as part of an iterator.

        :return: all the keys as a list.
        """

        for key in self.afile_objs.keys():
            yield key

        return list(self.afile_objs.keys())
