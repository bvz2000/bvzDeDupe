#! /usr/bin/env python3

from dataclasses import dataclass, field


@dataclass()
class ByName(object):
    name: str
    afile_objs: list = field(init=False)
