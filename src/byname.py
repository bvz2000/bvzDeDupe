#! /usr/bin/env python3

from afile import AFile


class ByName(object):
    """
    A class to store afile objects with a specific name.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 name=None):
        """
        :param name: The name shared by all the files stored in this instance. If None, the name will be set to ""
               and will have to be set directly later. Defaults to None.
        """

        assert name is None or type(name) is str

        if name is None:
            self.name = ""
        else:
            self.name = name

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
