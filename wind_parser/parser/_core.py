"""
Ancient version of the parser (for development purposes)
"""


import re
import sys
from typing import Any, Dict, List, Union

from ._utils import *


class Argument(str):

    def __init__(self, arg):
        super().__init__()

    def is_list(self) -> bool:
        return "," in self

    def is_kwarg(self) -> bool:
        separator = "=" in self or " " in self
        return separator and not self.is_list()

    def is_flag(self) -> bool:
        return self.startswith("-") and not self.is_kwarg()

    def remove_prefix(self, enable: bool = False) -> str:
        """
        Remove the prefix of an argument (-- or -).

        Returns
        -------
        str : The argument without the prefix.
        """
        if not enable:
            return self.lstrip("-")
        return self

    def render_list(self, show_prefix: bool = False) -> Dict[str, List]:
        if "=" in self:
            _ = self.remove_prefix(show_prefix).split("=")
        else:
            _ = self.remove_prefix(show_prefix).split(" ")

        return {_[0]: remove_empty_strings(_[1].split(","))}

    def render_kwarg(self, show_prefix: bool = False) -> Dict[str, str]:
        if "=" in self:
            _ = self.remove_prefix(show_prefix).split("=")
        else:
            _ = self.remove_prefix(show_prefix).split(" ")

        return {_[0]: _[1]}

    def render_flag(self, show_prefix: bool = False) -> Dict[str, bool]:
        return {self.remove_prefix(show_prefix): True}


class Parser(dict):
    """
    A class that parses arguments from sys.argv and returns a
    dictionary of arguments with their values.

    Parameters
    ----------
    args : List[str], optional
        A list of arguments (from sys.argv by default)

    prefix : bool, optional
        If True, the prefix will be kept in the keys (by default False)

    Attributes
    ----------
    args : Dict[str, Union[str, List[str], bool]]
        A dictionary of arguments with their values

    """

    def __init__(self, args: List[str] = None, prefix=False):
        if args is None:
            args = sys.argv
        self.prefix = prefix  # If True, the prefix will be kept in the keys
        self._args = args[1:]
        self.args = {}

        if self._args and self._args[0][0] != "-":
            setattr(self, "subcommand", self._args[0])
            del self._args[0]
        else:
            setattr(self, "subcommand", None)

        if self._args:
            self.parse_values()
            # Transfrom the Parser instance into a dictionary
            super().__init__(self.args)
            # Set arguments as class attributes
            for arg in self.args:
                setattr(self, arg, self.args[arg])

    def split_args(self) -> List[str]:
        """
        Split arguments directly from sys.argv and return a list of key with its value(s) or just a key if it's a flag

        Returns
        -------
        List[str]
            A list of arguments with their values inside a string
            or just a key if it's a flag

        ex : ['--name=John', '--age 32', '-v', '--list=item1,item2,item3']
        """
        pattern = re.compile(
            r"(--\w+(?:=|\s+)[\w,]+|-\w+(?:=|\s+)[\w,]+|--\w+)")
        args = pattern.findall(" ".join(self._args))
        return args

    def parse_values(self):
        """Parses the argument list and transposes the values and keys into a dictionary"""
        args = self.split_args()
        args = [
            Argument(arg) for arg in args
        ]  # Convert the list of arguments into a list of Argument objects

        for arg in args:
            if arg.is_list():
                self.args = {**self.args, **arg.render_list(self.prefix)}
            elif arg.is_kwarg():
                self.args = {**self.args, **arg.render_kwarg(self.prefix)}
            elif arg.is_flag():
                self.args = {**self.args, **arg.render_flag(self.prefix)}
