from pprint import PrettyPrinter
from typing import Any, Dict, List, Union

import ply.lex as lex
import ply.yacc as yacc

from ._utils import remove_empty_strings

pprint = PrettyPrinter(indent=4, sort_dicts=False).pprint


class Lexer:
    tokens = ("KEY", "VALUE", "EQ")

    t_KEY = r"(?:--|-)[a-z-A-Z-0-9]+"
    t_VALUE = r"(?<=(?:=|\s))[(?:\s*)\w,]+"
    t_EQ = r"="
    t_ignore = " \t"

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


class ArgParser(object):
    tokens = Lexer.tokens
    args = {}

    def __init__(self):
        self.lexer = Lexer().lexer
        self.parser = yacc.yacc(module=self, debug=False, write_tables=False)

    def p_options(self, p):
        """
        options : option options
                | option
        """

        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[2]

    def p_option(self, p):
        """
        option : KEY VALUE
               | KEY EQ VALUE
               | KEY
        """

        if len(p) == 2:
            p[0] = (p[1], True)
            return

        if isinstance(p[2], str) and "," in p[2]:
            p[2] = remove_empty_strings(p[2].split(","))
            p[2] = list(map(lambda s: s.strip(), p[2]))

        if len(p) == 3:
            p[0] = (p[1], p[2])

        else:
            p[0] = (p[1], p[3])

    def p_error(self, p):
        print("Syntax error at '%s'" % p.value)

    def parse(self, *args, **kwargs) -> dict[str, Any]:
        """
        Bind the parse method from the yacc parser to the Parser class
        """
        result: list[tuple] = self.parser.parse(lexer=self.lexer,
                                                *args,
                                                **kwargs)

        for key, value in result:
            ArgParser.args[key] = value

        return ArgParser.args


if __name__ == "__main__":
    data = "--list=item1,item2,item3 -a -b -c --list2=item1,item2,item3 -l i1,i2,i3 --flag -f --single Anthony -s 16 --composed-name=Anthony --a-b-c"
    parser = ArgParser()

    result = parser.parse(data)
    pprint(result)
