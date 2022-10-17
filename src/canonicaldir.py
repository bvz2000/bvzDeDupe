#! /usr/bin/env python3

from scandir import ScanDir


class CanonicalDir(ScanDir):
    """
    A class to scan and store the attributes of every file in a single directory.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 scan_dir):
        """
        :param scan_dir: The directory to scan.
        """
        super().__init__(scan_dir=scan_dir)

        self.by_size = dict()
        self.by_name = dict()
        self.by_parent = dict()
        self.by_type = dict()
        self.by_rel_path = dict()
        self.by_ctime = dict()
        self.by_mtime = dict()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _append_to_dict(by_dict,
                        key,
                        file_path):
        """
        Appends the file_path to the given dictionary.

        :param by_dict:
        :param file_path:
        :return:
        """

        try:
            by_dict[key].add(file_path)
        except KeyError:
            by_dict[key] = {file_path}

    # ------------------------------------------------------------------------------------------------------------------
    def _append_to_scan(self,
                        file_path,
                        metadata):
        """
        Appends a new file to the scan dictionaries.

        :param file_path: The path to the file to add
        :param metadata: The metadata for this file.

        :return: Nothing.
        """

        self._append_to_dict(by_dict=self.by_size,
                             key=metadata["size"],
                             file_path=file_path)

        self._append_to_dict(by_dict=self.by_name,
                             key=metadata["name"],
                             file_path=file_path)

        self._append_to_dict(by_dict=self.by_type,
                             key=metadata["file_type"],
                             file_path=file_path)

        self._append_to_dict(by_dict=self.by_parent,
                             key=metadata["parent"],
                             file_path=file_path)

        self._append_to_dict(by_dict=self.by_rel_path,
                             key=metadata["rel_path"],
                             file_path=file_path)

        self._append_to_dict(by_dict=self.by_ctime,
                             key=metadata["ctime"],
                             file_path=file_path)

        self._append_to_dict(by_dict=self.by_mtime,
                             key=metadata["mtime"],
                             file_path=file_path)
