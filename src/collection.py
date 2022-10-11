#! /usr/bin/env python3

from dataclasses import dataclass, field

from byattribute import ByAttribute


@dataclass()
class Collection(object):
    items: dict = field(init=False)

    def __post_init__(self):
        self.items = dict()

    def store_index(self,
                    key,
                    index):
        """
        Adds an item to the dictionary.

        :param key: The key for the item to be added (something like size, name, parent_name, or type).
        :param index: The index of the AFile object in the master afile_objs list.

        :return: Nothing.
        """

        try:
            self.items[key].indices.append(index)
        except KeyError:
            by_attribute_obj = ByAttribute(key)
            by_attribute_obj.indices.append(index)
            self.items[key] = by_attribute_obj

