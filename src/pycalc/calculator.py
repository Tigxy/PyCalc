import re
import math
import operator

constants = {
    "pi": math.pi,
    "e": math.e
}

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "//": operator.floordiv,
    "^": operator.pow
}

# sorted by descending precedence
operator_precedence = ["^", "*", "/", "//", "%", "+", "-"]

unary_functions = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "floor": math.floor,
    "ceil": math.ceil,
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": lambda x: math.log(x, math.e)
}

brackets = ["(", ")"]

int_pattern = r"[+-]?[0-9]+"
float_pattern = int_pattern + r"(\.[0-9]+){0,1}"
scientific_pattern = float_pattern + r"(e[+-]?[0-9]+){0,1}"

single_char_pattern = r"[\-+\/%^*()]"
split_pattern = rf"({scientific_pattern}|{single_char_pattern}|[a-z]+)"


class Node:
    def __init__(self, left=None, right=None, op=None, value=None, unary_fn=None):
        self.left = left
        self.right = right
        self.operator = op
        self.unary_fn = unary_fn
        self.value = value
        self.is_value_node = self.value is not None
        self.is_unary_op = self.unary_fn is not None

    def reduce(self):
        """ Calculates the value itself by reducing the operators and functions to actual values. """
        if self.is_value_node:
            return self.value
        if self.is_unary_op:
            return unary_functions[self.unary_fn](self.left.reduce())
        else:
            return operators[self.operator](self.left.reduce(), self.right.reduce())

    def __str__(self):
        if self.is_value_node:
            return str(self.value)
        elif self.is_unary_op:
            return f"{self.unary_fn}({self.left})"
        else:
            return f"{self.left} {self.operator} {self.right}"


def __split_formula(formula):
    """
    Splits a formula into its parts, e.g., separating values from operators
    :param formula: The formula to split up
    :return: The split up formula
    :raises: `ValueError`
    """

    formula = formula.strip().replace(" ", "")
    elements = re.findall(split_pattern, formula)
    elements = [el[0] for el in elements]

    # ensure that no term was left out, although this costs some resources,
    # for simple usage this should be neglectable
    if "".join(elements) != formula:
        raise ValueError("Unsupported terms / characters have been used. Please check your formula.")

    return elements


def __is_op(term):
    return term in operators.keys()


def __is_neg(term):
    return term == "-"


def __is_const(term):
    return term in constants.keys()


def __is_unary_fn(term):
    return term in unary_functions.keys()


def __is_numeric(term):
    return re.match(f"^{scientific_pattern}$", term) is not None


def __parse_brackets(formula):
    is_open = False
    count_open = 0
    idx_open = -1

    # builds a subtree for each pair of brackets
    terms = []
    for i, term in enumerate(formula):
        if term == "(":
            if not is_open:
                is_open = True
                idx_open = i
            count_open += 1

        elif term == ")":
            if count_open == 1:
                terms.append(__build_tree(formula[idx_open + 1:i]))  # after building tree, brackets will be ignored
                is_open = False
            count_open -= 1

        elif is_open:
            # we don't parse the subformula directly, but recursively
            pass

        else:
            if len(terms) > 0 and __is_op(terms[-1]) and __is_op(term):
                # Not pretty, but we need to handle double operator for floor division
                if terms[-1] == "/" and term == "/":
                    terms[-1] = "//"
                    continue

                raise ValueError("Subsequent operators are not allowed. A value is required inbetween.")
            terms.append(Node(value=float(term)) if __is_numeric(term) else term)

    if count_open != 0:
        raise ValueError("Missing opening or closing bracket.")

    return terms


def __parse_constants(formula):
    return [Node(value=constants[term]) if __is_const(term) else term for term in formula]


def __parse_unary_fn(formula):
    unary_terms = []
    # set the parameters of the unary functions from back to front
    for term in formula[::-1]:
        if __is_unary_fn(term):
            # wrap the succeeding term with the current function
            unary_terms[-1] = Node(left=unary_terms[-1], unary_fn=term)
        else:
            unary_terms.append(term)

    # revert order again
    return unary_terms[::-1]


def __parse_operators(formula):
    # applies order of precedence for operators
    for op in operator_precedence:
        op_indices = [i for i, term in enumerate(formula) if term == op]
        for i in op_indices[::-1]:
            # replace operation by processed operation node
            formula[i] = Node(left=formula[i - 1], right=formula[i + 1], op=formula[i])
            del formula[i + 1], formula[i - 1]
    return formula


def __add_all(formula):
    while len(formula) > 1:
        formula[0] = Node(left=formula[0], right=formula[1], op="+")
        del formula[1]
    return formula[0]


def __build_tree(formula):
    """
    For solving a formula, we first need to build up a tree to determine which
    terms and operations may be executed at which point in time. Otherwise, by
    evaluating the formula from left to right, the order of precedence for
    operations may be lost.

    :param formula: The formula to evaluate, already preprocessed by __split_formula().
    :return: A node representing the entire formula, where each child node (and their child nodes)
             have to be evaluated before the node itself may be evaluated to maintain the
             order of precedence.
    :raises: `ValueError`
    """

    if len(formula) == 0:
        raise ValueError("Please specify your formula.")

    if __is_op(formula[0]) or __is_op(formula[-1]):
        raise ValueError("(Sub)formula must not start or end with an operator.")

    if __is_unary_fn(formula[-1]):
        raise ValueError("Each unary function requires a parameter.")

    # Numeric values may be immediately returned
    if len(formula) == 1 and __is_numeric(formula[0]):
        return Node(value=float(formula[0]))

    formula = __parse_brackets(formula)
    formula = __parse_constants(formula)
    formula = __parse_unary_fn(formula)
    formula = __parse_operators(formula)

    # ensure that all terms have been parsed
    failed_parsings = [term for term in formula if not isinstance(term, Node)]
    if len(failed_parsings) > 0:
        raise ValueError("Encountered unexpected term(s) in formula:", ", ".join(failed_parsings))

    # since positive or negative signs preceding numeric values have already been accounted for,
    # we may end up with more than 1 term. In that case, we can simply add up these terms.
    # E.g.: "2 - 1" leads to [Node(2), Node(-1)], which can be simplified to its sum. [Node(2) + Node(-1)]
    return __add_all(formula)


def solve(formula: str):
    return __build_tree(__split_formula(formula)).reduce()
