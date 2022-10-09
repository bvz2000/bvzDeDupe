#! /usr/bin/env python3

from afile import AFile


class BySize(object):
    """
    A class to store afile objects of a specific file size.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 size=None):
        """
        :param size: The size (in bytes) of all the files stored in this instance. If None, the size will be set to 0
               bytes and will have to be set directly later. Defaults to None.
        """

        assert size is None or type(size) is int

        if size is None:
            self.size = 0
        else:
            self.size = size

        self.afile_objs = list()

    # ------------------------------------------------------------------------------------------------------------------
    def add(self,
            afile_obj):
        """
        Adds an afile object to the set of objects.

        :param afile_obj: The afile object to add.

        :return: Nothing.
        """

        assert type(afile_obj) is AFile

        self.afile_objs.append(afile_obj)
