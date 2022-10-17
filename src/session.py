#! /usr/bin/env python3

from canonicaldir import CanonicalDir
from querydir import QueryDir

import comparefiles


class Session(object):
    """
    A class to manage a scan and compare session.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 query_dir,
                 canonical_dir,
                 report_frequency=1000):
        """
        Init.

        :param query_dir: The full query directory path.
        :param canonical_dir: The full canonical directory path.
        :param report_frequency: How many files to scan before reporting back to the calling function.
        """

        self.canonical_scan = None
        self.query_scan = None

        self.query_dir = query_dir
        self.canonical_dir = canonical_dir
        self.report_frequency = report_frequency

        self.actual_matches = dict()

        self.pre_computed_checksum_count = 0

    # ------------------------------------------------------------------------------------------------------------------
    def do_query_scan(self):
        """
        Execute the query scan.

        :return: Nothing.
        """

        self.query_scan = QueryDir(scan_dir=self.query_dir)
        for file_count in self.query_scan.scan(report_frequency=self.report_frequency):
            yield file_count

    # ------------------------------------------------------------------------------------------------------------------
    def do_canonical_scan(self):
        """
        Execute the canonical scan.

        :return: Nothing.
        """

        self.canonical_scan = CanonicalDir(scan_dir=self.canonical_dir)
        for file_count in self.canonical_scan.scan(report_frequency=self.report_frequency):
            yield file_count

    # ------------------------------------------------------------------------------------------------------------------
    def do_compare(self,
                   name=False,
                   file_type=False,
                   parent=False,
                   rel_path=False,
                   ctime=False,
                   mtime=False):
        """
        Compare query scan to canonical scan. Any attributes that are set to True will be used as part of the
        comparison. Size is always used as a comparison attribute.

        :param name: If True, then also compare on name. Defaults to False.
        :param file_type: If True, then also compare on the file type. Defaults to False.
        :param parent: If True, then also compare on the parent directory name. Defaults to False.
        :param rel_path: If True, then also compare on teh relative path. Defaults to False.
        :param ctime: If True, then also compare on the creation time. Defaults to False.
        :param mtime: If True, then also compare on the modification time. Defaults to False.

        :return: A dictionary of matching files where the key is the file in the query directory and the value is a list
                 of files in the canonical directory which match.
        """

        count = 0

        for file_path, metadata in self.query_scan.files.items():

            count += 1
            yield count

            if name:
                name = metadata["name"]
            else:
                name = None

            if file_type:
                file_type = metadata["file_type"]
            else:
                file_type = None

            if parent:
                parent = metadata["parent"]
            else:
                parent = None

            if rel_path:
                rel_path = metadata["rel_path"]
            else:
                rel_path = None

            if ctime:
                ctime = metadata["ctime"]
            else:
                ctime = None

            if mtime:
                mtime = metadata["mtime"]
            else:
                mtime = None

            possible_matches = self.canonical_scan.get_intersection(size=metadata["size"],
                                                                    name=name,
                                                                    file_type=file_type,
                                                                    parent=parent,
                                                                    rel_path=rel_path,
                                                                    ctime=ctime,
                                                                    mtime=mtime)

            if len(possible_matches) == 0:
                continue

            for possible_match in possible_matches:
                possible_match_checksum = self.canonical_scan.get_checksum(possible_match)
                if possible_match_checksum is not None:
                    self.pre_computed_checksum_count += 1
                checksum = comparefiles.compare(file_a_path=file_path,
                                                file_b_path=possible_match,
                                                file_b_checksum=possible_match_checksum,
                                                single_pass=True)
                if checksum:
                    self.canonical_scan.checksum[possible_match] = checksum
                    try:
                        self.actual_matches[file_path].append(possible_match)
                    except KeyError:
                        self.actual_matches[file_path] = [possible_match]
