import sys
import pytest
from .parser import Parser, Argument


# Test separate_arguments method of Parser class
def test_separate_arguments():
    sys.argv = ['python', '--name=Anthony', '--age=16', '--verbose', '--list',
                'Paul', 'Célia', 'Mathieu', '--logging', '-l', 'this', 'for', 'while']

    p = Parser(sys.argv)

    assert p.separate_args() == ['--name=Anthony', '--age=16', '--verbose', '--list', ['Paul', 'Célia', 'Mathieu'], '--logging', '-l', ['this', 'for', 'while']]    


# Test the parse_values method of the Parser class
def test_parse_values():
    sys.argv = ['python', '--name=Anthony', '--age=16', '--verbose',
                '--list', 'Paul', 'Célia', 'Mathieu', '--logging', '-l', 'this', 'for', 'while']
    p = Parser(sys.argv)

    assert p.args == {'name': 'Anthony', 'age': '16', 'verbose': True, 'list': ['Paul', 'Célia', 'Mathieu'], 'logging': True, 'l': ['this', 'for', 'while']}

    sys.argv.extend(['--test1', '--test2', '-z','16'])

    p = Parser(sys.argv)

    assert p.args == {'name': 'Anthony', 'age': '16', 'verbose': True, 'list': ['Paul', 'Célia', 'Mathieu'], 'logging': True, 'l': ['this', 'for', 'while'],'test1':True, 'test2':True, 'z':'16'}


# Test the Argument class
def test_argument():
    assert Argument("-v").is_key()
    assert Argument("--help").is_key()
    assert Argument("-a=16").is_kwarg()
    assert Argument([1,2,3]).is_value()
