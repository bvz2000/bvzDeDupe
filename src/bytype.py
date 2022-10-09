#! /usr/bin/env python3

from afile import AFile


class ByType(object):
    """
    A class to store afile objects with a specific type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 ftype=None):
        """
        :param ftype: The type shared by all the files stored in this instance. If None, the type will be set to ""
               and will have to be set directly later. Defaults to None.
        """

        assert ftype is None or type(ftype) is str

        if ftype is None:
            self.ftype = ""
        else:
            self.ftype = ftype

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
