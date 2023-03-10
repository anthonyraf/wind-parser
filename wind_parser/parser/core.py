import sys
from typing import Any, Dict, List, Union

from .parser import ArgParser


class Parser:

    def __init__(self, arguments: List[str]):
        self.__argparser = ArgParser()
        self.args = self.__argparser.parse(arguments)
