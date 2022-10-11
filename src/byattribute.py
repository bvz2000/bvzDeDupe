#! /usr/bin/env python3
"""
A class to store every index of an AFile object that has the same attribute.

For example, stores the index of every file that has the same size. (or name, or parent, etc.)
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass()
class ByAttribute(object):
    attr: Union[str, int]
    indices: list = field(init=False)

    def __post_init__(self):
        self.indices = list()
