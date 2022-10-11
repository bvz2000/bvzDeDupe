#! /usr/bin/env python3

from dataclasses import dataclass, field

from byattribute import ByAttribute


@dataclass()
class Collection(object):
    items: dict = field(init=False)

    def __post_init__(self):
        self.items = dict()

    def add(self,
            key,
            item):
        """
        Adds an item to the dictionary.

        :param key: The key for the item to be added.
        :param item: The AFile object to add to this key.

        :return: Nothing.
        """

        try:
            self.items[key].append(item)
        except KeyError:
            by_attribute_obj = ByAttribute(key)
            by_attribute_obj.objs.append(item)
            self.items[key] = [by_attribute_obj]

