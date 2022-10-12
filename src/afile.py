#! /usr/bin/env python3

import os.path
from dataclasses import dataclass, field


@dataclass()
class AFile:
    path: str
    rel_path: str
    size: int
    creation_date: float
    modification_date: float
    hidden: bool
    file_type: str = field(init=False)
    name: str = field(init=False)
    parent_name: str = field(init=False)
    md5: str = field(init=False)

    def __post_init__(self):
        self.name = os.path.split(self.path)[1]
        self.file_type = os.path.splitext(self.name)[1]
        self.parent_name = os.path.split(os.path.split(self.path)[0])[1]
        self.md5 = ""
