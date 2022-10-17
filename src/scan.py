#! /usr/bin/env python3

import sqlite3
from scan_dir import ScanDir


class Scan(object):
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

    # ------------------------------------------------------------------------------------------------------------------
    def do_query_scan(self):
        """
        Execute the query scan.

        :return: Nothing.
        """

        self.query_scan = ScanDir(scan_dir=self.query_dir)
        for file_count in self.query_scan.scan(report_frequency=self.report_frequency):
            yield file_count

    # ------------------------------------------------------------------------------------------------------------------
    def do_canonical_scan(self):
        """
        Execute the canonical scan.

        :return: Nothing.
        """

        self.canonical_scan = ScanDir(scan_dir=self.canonical_dir)
        for file_count in self.canonical_scan.scan(report_frequency=self.report_frequency):
            yield file_count
