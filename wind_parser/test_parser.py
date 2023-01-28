import sys

import pytest

from .parser import Argument, Parser


# Test separate_arguments method of Parser class
def test_separate_arguments():
    sys.argv = [
        "python",
        "--name=Anthony",
        "--age=16",
        "--verbose",
        "--list=Paul,Célia,Mathieu",
        "--logging",
        "-l",
        "this,for,while",
    ]

    p = Parser(sys.argv)
    print(p.separate_args())

    assert p.separate_args() == [
        "--name=Anthony",
        "--age=16",
        "--verbose",
        "--list",
        ["Paul", "Célia", "Mathieu"],
        "--logging",
        "-l",
        ["this", "for", "while"],
    ]


# Test the parse_values method of the Parser class
def test_parse_values():
    sys.argv = [
        "python",
        "--name=Anthony",
        "--age=16",
        "--verbose",
        "--list",
        "Paul,Célia,Mathieu",
        "--logging",
        "-l",
        "this,for,while",
    ]
    p = Parser(sys.argv)

    assert p.args == {
        "name": "Anthony",
        "age": "16",
        "verbose": True,
        "list": ["Paul", "Célia", "Mathieu"],
        "logging": True,
        "l": ["this", "for", "while"],
    }

    sys.argv.extend(["--test1", "--test2", "-z", "16"])

    p = Parser(sys.argv)

    assert p.args == {
        "name": "Anthony",
        "age": "16",
        "verbose": True,
        "list": ["Paul", "Célia", "Mathieu"],
        "logging": True,
        "l": ["this", "for", "while"],
        "test1": True,
        "test2": True,
        "z": "16",
    }


def test_messy_list():
    sys.argv = ["python", "-l", ",item1,,item2,,,item3,"]
    p = Parser(sys.argv)
    assert p.args == {"l": ["item1", "item2", "item3"]}


# Test when there is no argument provided
def test_no_argument():
    sys.argv = ["python"]
    p = Parser(sys.argv)

    assert p.args == {}


def test_subcommand():
    sys.argv = ["python", "config"]
    p = Parser(sys.argv)

    assert p.subcommand == "config"
    assert "config" not in p.args

    with pytest.raises(KeyError):
        p["subcommand"]


# Test the Argument class
def test_argument():
    assert Argument("-v").is_key()
    assert Argument("--help").is_key()
    assert Argument("-a=16").is_kwarg()
    assert Argument([1, 2, 3]).is_value()
