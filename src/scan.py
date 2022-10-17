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
                 canonical_dir):
        """
        Init.

        :param query_dir: The full query directory path.
        :param canonical_dir: The full canonical directory path.
        """

        self.query_dir = query_dir
        self.canonical_dir = canonical_dir

        self.connection, self.cursor = self._connect()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _connect():
        """
        Creates a new sqlite3 database in memory.

        :return: A sqlite3 connection object.
        """

        connection = sqlite3.connect("file::memory:")
        cursor = connection.cursor()
        return connection, cursor

    # ------------------------------------------------------------------------------------------------------------------
    def do_scan(self):
        """
        Execute the scan.

        :return: Nothing.
        """

        query_scan = ScanDir(scan_dir=self.query_dir,
                             connection=self.connection,
                             cursor=self.cursor)
        query_scan.scan()

        canonical_scan = ScanDir(scan_dir=self.canonical_dir,
                                 connection=self.connection,
                                 cursor=self.cursor)
        canonical_scan.scan()