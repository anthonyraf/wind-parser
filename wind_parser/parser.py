import sys
from typing import List, Any, Union

class Argument:
    def __init__(self, arg: Union[str, List[str]]):
        if not isinstance(arg, (str, list)):
            raise TypeError(f"Argument must be str or list not {type(arg).__name__}")
        self.arg = arg

    def is_key(self):
        """Check if the argument is a key"""
        if isinstance(self.arg,str):
            return self.arg.startswith('--') or self.arg.startswith('-')
        else:
            return False

    def is_kwarg(self):
        """Check if the argument is a key directly followed by a value after the '=' sign"""
        return isinstance(self.arg, str) and '=' in self.arg

    def is_value(self):
        """Check if the argument is a value"""
        return not self.is_key()
    
    def remove_prefix(self):
        """Delete the prefix of an argument"""
        if self.arg.startswith('--'):
            return self.arg[2:]
        elif self.arg.startswith('-'):
            return self.arg[1:]

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

    def __init__(self, args: List[str]=sys.argv):
        self._args = args[1:]
        self.args = {}

        if self._args and self._args[0][0] != '-':
            setattr(self,'subcommand', self._args[0])
            del self._args[0]

        if self._args:
            self.parse_values()
            # Transfrom the Parser instance into a dictionary
            super().__init__(self.args)
            # Set arguments as class attributes
            for arg in self.args:
                setattr(self, arg, self.args[arg])

    # def separate_args(self) -> List[List]:
    #     """Separate arguments by storing lists of values given to a key in lists
    #     ex: separate_args(['-l', 'a','b','c']) -> ['-l', ['a', 'b', 'c']]
    #     """
    #     result: List[Any] = []
    #     tmp: List[str] = []
    #     for arg in self._args:
    #         arg = arg.strip()
    #         if arg.startswith('--') or arg.startswith('-'):
    #             if tmp != []:
    #                 result.append(tmp)
    #                 tmp = []
    #             result.append(arg)
    #         else:
    #             tmp.append(arg)
    #     if tmp:
    #         result.append(tmp)

    #     return result
    
    def separate_args(self):
        result = []
        for arg in self._args:
            arg = arg.strip()
            if arg.startswith('-'): # or "--"
                if '=' in arg and ',' in arg:  # ex: --list=item1,item2,item3
                    _tmp = arg.split('=')
                    result.append(_tmp[0])
                    result.append(_tmp[1].split(','))
                else:
                    result.append(arg)
            elif ',' in arg:
                result.append(arg.split(','))
            else:
                result.append(arg)
        return result


    def parse_values(self):
        """Parses the argument list and transposes the values and keys into a dictionary"""
        args = self.separate_args()
        args = [Argument(arg) for arg in args] # Convert the list of arguments into a list of Argument objects

        key = None # Temporary key
        for arg in args:
            _arg = arg.remove_prefix() if arg.is_key() else arg.arg
            if arg.is_kwarg(): 
                key, value = _arg.split('=')
                self.args[key] = value
            elif arg.is_key():
                key = _arg
                self.args[key] = True
            elif key is not None:
                self.args[key] = _arg
                key = None
            else:
                self.args[_arg] = True
        
        for arg in self.args.copy():
            if isinstance(self.args[arg], list) and len(self.args[arg]) == 1:
                self.args[arg] = self.args[arg][0]

if __name__ == '__main__':
    sys.argv = ['python', '--name=Anthony', '--age=16', '--verbose',
                '--list', 'Paul', 'Célia', 'Mathieu', '--logging', '-l', 'this', 'for', 'while', '-i', '16']

    p = Parser(sys.argv)
    print(p)
