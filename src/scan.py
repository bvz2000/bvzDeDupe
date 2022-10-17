#! /usr/bin/env python3

from canonicaldir import CanonicalDir


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

        self.query_scan = CanonicalDir(scan_dir=self.query_dir)
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
    def do_compare(self):
        """
        Compare query scan to canonical scan.

        :return: Nothing.
        """

        pass


        # count = 0
        # old_percent = 0
        # matches = list()
        # unique = list()
        # for key in query_scan_obj.keys():
        #     if key in canonical_scan_obj.keys():
        #         old_percent = displaylib.display_progress(count=count,
        #                                                   total=num_possible_matches,
        #                                                   old_percent=old_percent)
        #         checksum = comparefiles.compare(query_scan_obj.afile_objs[key].path, canonical_scan_obj.afile_objs[key].path)
        #         if checksum:
        #             matches.append((key, checksum))
        #             canonical_scan_obj.afile_objs[key].md5 = checksum  # <- for the future when we store the checksum for multiple runs
        #         else:
        #             unique.append((key, checksum))
        #         count += 1
