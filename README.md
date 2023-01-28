# Wind Parser 
![Python versions badge](https://img.shields.io/pypi/pyversions/wind-parser) [![Python package](https://github.com/anthonyraf/wind-parser/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/anthonyraf/wind-parser/actions/workflows/python-package.yml) [![DeepSource](https://deepsource.io/gh/anthonyraf/wind-parser.svg/?label=active+issues&show_trend=true&token=_GxN7KijEstuTXJ7QC8Q0vGb)](https://deepsource.io/gh/anthonyraf/wind-parser/?ref=repository-badge)

*Python wind parser is a parser used to retrieve arguments for command line interfaces and turn them into python dictionary.*

- Wind parser has a very simple and easy use
- Wind parser supports keyword arguments, flags and keyword arguments that accept lists
> This parser was created for the [speed](https://github.com/anthonyraf/speed-cli) framework.
## Installation

Installation with **pip** : 

    $ pip install wind-parser
    
## Usage

After installing wind-parser you can just instantiate the Parser class with `sys.argv` as argument (`sys.argv` isn't required but it's better for the code clarity)

Here is an example of how the parser is used:
```python
# command.py

import sys
from wind_parser import Parser

parser = Parser(sys.argv) # This variable stores the arguments with their values in a python dictionary
 
if __name__ == '__main__':
    print(parser) # Print the dictionary
```
> **Note**
> : You can also use `p.args` for printing the dictionary


Then you can run in your terminal:
    
    $ python command.py --name=John --age=32 --hobbies Football,Basketball,Cinema --verbose
Output:

    {'name':'John', 'age':'32', 'hobbies': ['Football', 'Basketball', 'Cinema'],  'verbose':True}
To access the value of an argument, you can choose between:

- Use dictionary key access: 
```python
print(p['name'])
# or
print(p.args['name'])
```
- Use class attribute access:
```python
print(p.name)
```
> **Note**
> : With this method, you will not be able to retrieve arguments with a `-` in its name.

## Specifications
The different types of arguments supported:

- Keyword argument : `-a 1`, `--a=1`, `-a item1,item2,item3`
- Flag : `--verbose`, `-v`, `--help`


Here are the types of the different possible values depending on the type of argument:

| Arguments | Python type|
|-----------|-----|
|`--name=John` or `--age 16`| str |
|`--verbose` or `-v` | bool (always True) |
|`--files main.py,m.cfg,test.txt` | list[str]

