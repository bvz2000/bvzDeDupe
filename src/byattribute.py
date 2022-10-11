#! /usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass()
class ByAttribute(object):
    attr: Union[str, int]
    objs: list = field(init=False)

    def __post_init__(self):
        self.objs = list()
