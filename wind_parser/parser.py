import re
import sys
from typing import Any, Dict, List, Union

from .utils import *


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

    def remove_prefix(self) -> str:
        return self.lstrip("-")

    def render_list(self) -> Dict[str, List]:
        if "=" in self:
            _ = self.remove_prefix().split("=")
        else:
            _ = self.remove_prefix().split(" ")

        return {_[0]: remove_empty_strings(_[1].split(","))}

    def render_kwarg(self) -> Dict[str, str]:
        if "=" in self:
            _ = self.remove_prefix().split("=")
        else:
            _ = self.remove_prefix().split(" ")

        return {_[0]: _[1]}

    def render_flag(self) -> Dict[str, bool]:
        return {self.remove_prefix(): True}


class Parser(dict):
    """
    Parse arguments from script call

    Usage:
        import sys

        p = Parser(sys.argv)
        print(p)
        print(f"Your name is %s"%p.name)

        $ python main.py --name=John --age=32 --hobbies test test1

    Output :
        {'name':'John', 'age':'32', 'hobbies': ['test', 'test1']}
        Your name is John
    """

    def __init__(self, args: List[str] = None):
        if args is None:
            args = sys.argv
        self._args = args[1:]
        self.args = {}

        if self._args and self._args[0][0] != "-":
            setattr(self, "subcommand", self._args[0])
            del self._args[0]

        if self._args:
            self.parse_values()
            # Transfrom the Parser instance into a dictionary
            super().__init__(self.args)
            # Set arguments as class attributes
            for arg in self.args:
                setattr(self, arg, self.args[arg])

    def separate_args(self) -> List[str]:
        """
        Separate arguments directly from sys.argv and return a list of key with its value(s) or just a key if it's a flag

        Returns
        -------
        List[str]
            A list of arguments.
            ex : ['--name=John', '--age 32', '-v', '--list=item1,item2,item3']
        """
        pattern = re.compile(
            r"(--\w+(?:=|\s+)[\w,]+|-\w+(?:=|\s+)[\w,]+|--\w+)")
        args = pattern.findall(" ".join(self._args))
        return args

    def parse_values(self):
        """Parses the argument list and transposes the values and keys into a dictionary"""
        args = self.separate_args()
        args = [
            Argument(arg) for arg in args
        ]  # Convert the list of arguments into a list of Argument objects

        for arg in args:
            if arg.is_list():
                self.args = {**self.args, **arg.render_list()}
            elif arg.is_kwarg():
                self.args = {**self.args, **arg.render_kwarg()}
            elif arg.is_flag():
                self.args = {**self.args, **arg.render_flag()}


if __name__ == "__main__":
    p = Parser(sys.argv)
    print(p.age)
    # print(f"Your name is %s"%p.name)
