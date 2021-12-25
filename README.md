# Python string calculator
## Quick overview:
An easily extendable python calculator that evaluates a formula given
as string. It supports a wide variety of commonly used operations:
- basic operators: `+`, `-`, `*`, `/`, `//`, `%`, `^` 
- constants: `e`, `pi`
- unary functions: `ceil`, `floor`, `ln` (base `e`), `log` (base `10`), `sqrt`
- trigonometric functions: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`

It maintains the [operator precedence](https://en.wikipedia.org/wiki/Order_of_operations), 
e.g., it will always multiply terms if possible before adding others. Integers, floats and values 
in scientific notation (e.g., `1e-3` for `0.001`) are all supported.

Moreover, more may be easily added by appending them on top of the [main file](src/pycalc/calculator.py)
in the respective sections.

## Installation
- Install it as usual with `pip`:  
`python -m pip install git+https://github.com/tigxy/pycalc.git`
- Or from source:
``

## Usage
- Either from the command line: `python -m pycalc "2+2"`
- Or inside your code
```py
from pycalc import solve
result = solve("2 + 2")
print(result) # 4.0
```

## Why?
Mostly a fun little side project as I have been wondering how to best 
parse and evaluate a mathematical formula. In case you have any real use-case, 
please let me know!

Feel free to create an issue or a PR in case you would like some additional
functionality.

## License
MIT License - see the [LICENSE](/LICENSE) file for more details.
