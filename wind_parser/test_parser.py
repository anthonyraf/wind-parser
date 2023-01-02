import sys
import unittest
from .parser import Parser


class parserTestCase(unittest.TestCase):
    def test_separate_arguments(self):
        sys.argv = ['python', '--name=Anthony', '--age=16', '--verbose', '--list',
                    'Paul', 'Célia', 'Mathieu', '--logging', '-l', 'this', 'for', 'while']

        p = Parser(sys.argv)

        self.assertEqual(p.separate_args(),
                         ['--name=Anthony', '--age=16', '--verbose', '--list', ['Paul', 'Célia', 'Mathieu'], '--logging', '-l', ['this', 'for', 'while']])

    def test_parse_values(self):
        sys.argv = ['python', '--name=Anthony', '--age=16', '--verbose',
                    '--list', 'Paul', 'Célia', 'Mathieu', '--logging', '-l', 'this', 'for', 'while']
        p = Parser(sys.argv)

        self.assertEqual(p.args,
                         {'name': 'Anthony', 'age': '16', 'verbose': True, 'list': ['Paul', 'Célia', 'Mathieu'], 'logging': True, 'l': ['this', 'for', 'while']})

        sys.argv.extend(['--test1', '--test2', '-z','16'])

        p = Parser(sys.argv)

        self.assertEqual(p.args,
                         {'name': 'Anthony', 'age': '16', 'verbose': True, 'list': ['Paul', 'Célia', 'Mathieu'], 'logging': True, 'l': ['this', 'for', 'while'],'test1':True, 'test2':True, 'z':'16'})

if __name__ == '__main__':
    unittest.main()
