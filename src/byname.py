#! /usr/bin/env python3

from dataclasses import dataclass, field


@dataclass()
class ByName(object):
    name: str
    afile_objs: list = field(init=False)

    def __post_init__(self):
        self.afile_objs = list()