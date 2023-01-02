import sys
from typing import Dict, List, Union

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

    def __init__(self, args=sys.argv) -> Dict[str, Union[str, List]]:
        self._args = args[1:]
        self.args = {}

        if self._args:
            self.parse_values()
            # Transfrom the Parser class into a dictionary
            super().__init__(self.args)
            # Set arguments as class attributes
            for arg in self.args:
                setattr(self, arg, self.args[arg])

    def separate_args(self) -> List[List]:
        """Separate arguments by storing lists of values given to a key in lists
        ex: separate_args(['-l', 'a','b','c']) -> ['-l', ['a', 'b', 'c']]  
        """
        result = []
        tmp = []
        for arg in self._args:
            arg = arg.strip()
            if arg.startswith('--') or arg.startswith('-'):
                if tmp != []:
                    result.append(tmp)
                    tmp = []
                result.append(arg)
            else:
                tmp.append(arg)
        if tmp:
            result.append(tmp)

        return result

    def parse_values(self) -> None:
        """Parses the argument list and transposes the values and keys into a dictionary"""
        args = self.separate_args()

        for i in range(len(args)):
            if '=' in args[i] and isinstance(args[i], str):
                _ = args[i].split('=')
                self.args[_[0][2:] if _[0].startswith(
                    '--') else _[0][1:]] = _[1]

            elif i < len(args)-1:
                if isinstance(args[i], str):
                    if args[i].startswith('--') or args[i].startswith('-'):
                        if isinstance(args[i+1], list):
                            self.args[args[i][2:] if args[i].startswith(
                                '--') else args[i][1:]] = args[i+1]
                        else:
                            self.args[args[i][2:] if args[i].startswith(
                                '--') else args[i][1:]] = True

        if isinstance(args[-1], str) and (args[-1].startswith('--') or args[-1].startswith('-')):
            self.args[args[-1][2:]
                      if args[-1].startswith('--') else args[-1][1:]] = True

        for arg in self.args.copy():
            if isinstance(self.args[arg], list) and len(self.args[arg]) == 1:
                self.args[arg] = self.args[arg][0]


if __name__ == '__main__':
    sys.argv = ['python', ' --name=Anthony', '--age=16', '--verbose',
                '--list', 'Paul', 'Célia', 'Mathieu', '--logging', '-l', 'this', 'for', 'while', '-i', '16']

    p = Parser(sys.argv)
    print(p.args)
    print(p)
