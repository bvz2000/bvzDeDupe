#! /usr/bin/env python3

from dataclasses import dataclass, field


@dataclass()
class ByType(object):
    ftype: str
    afile_objs: list = field(init=False)
