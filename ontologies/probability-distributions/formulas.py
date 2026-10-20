"""The formula syntax of the ontology's source, and an evaluator for it.

A formula is an arithmetic expression in Python's syntax over the coordinates of a chart: numbers, names, + - * / **,
unary minus, comparisons, `and`/`or`, and calls to the functions in FUNCTIONS. Nothing else parses, so a formula can be
read by any consumer and evaluated without running code from the source. The generator rejects a formula outside this
syntax, or one naming anything but the coordinates its place allows.

The evaluator serves the generator's checks and the tests. The ontology provides no routines for the distributions
themselves.
"""

from __future__ import annotations

import ast
import math

FUNCTIONS = {
    "sqrt": math.sqrt,
    "exp": math.exp,
    "log": math.log,
    "Phi": lambda x: 0.5 * math.erfc(-x / math.sqrt(2.0)),  # the standard normal CDF
    "phi": lambda x: math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi),  # the standard normal density
}
CONSTANTS = {"inf": math.inf, "pi": math.pi}
TRANSCENDENTAL = {"sqrt", "exp", "log", "Phi", "phi"}

_BINARY = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a**b,
}
_COMPARE = {
    ast.Lt: lambda a, b: a < b,
    ast.LtE: lambda a, b: a <= b,
    ast.Gt: lambda a, b: a > b,
    ast.GtE: lambda a, b: a >= b,
    ast.Eq: lambda a, b: a == b,
}


class FormulaError(ValueError):
    pass


def parse(text: str) -> ast.Expression:
    """Parse a formula, refusing anything outside the syntax."""
    try:
        tree = ast.parse(str(text).strip(), mode="eval")
    except SyntaxError as e:
        raise FormulaError(f"not a formula: {text!r} ({e.msg})") from None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Expression, ast.Load, ast.UnaryOp, ast.USub, ast.UAdd, ast.BoolOp, ast.And, ast.Or)):
            continue
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY:
            continue
        if isinstance(node, ast.Compare) and all(type(op) in _COMPARE for op in node.ops):
            continue
        if type(node) in _BINARY or type(node) in _COMPARE:
            continue
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            continue
        if isinstance(node, ast.Name):
            continue
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in FUNCTIONS and not node.keywords:
                continue
            raise FormulaError(f"{text!r}: only {', '.join(sorted(FUNCTIONS))} may be called, with positional arguments")
        raise FormulaError(f"{text!r}: {type(node).__name__} is outside the formula syntax")
    return tree


def names(text: str) -> set[str]:
    """The free names of a formula: the names it uses as values, other than the constants."""
    tree = parse(text)
    called = {id(n.func) for n in ast.walk(tree) if isinstance(n, ast.Call)}
    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name) and id(n) not in called}
    return used - set(CONSTANTS)


def is_exact(text: str) -> bool:
    """True when the formula is rational in its names: no transcendental function and no fractional power."""
    tree = parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and node.func.id in TRANSCENDENTAL:
            return False
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            exponent = node.right
            if isinstance(exponent, ast.UnaryOp) and isinstance(exponent.operand, ast.Constant):
                exponent = exponent.operand
            if not (isinstance(exponent, ast.Constant) and float(exponent.value).is_integer()):
                return False
    return True


def evaluate(text: str, env: dict):
    """Evaluate a formula with the names in `env` (numbers, or numpy arrays where the operations allow)."""
    tree = parse(text)

    def ev(node):
        if isinstance(node, ast.Expression):
            return ev(node.body)
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            if node.id in env:
                return env[node.id]
            if node.id in CONSTANTS:
                return CONSTANTS[node.id]
            raise FormulaError(f"{text!r}: no value for {node.id!r}")
        if isinstance(node, ast.UnaryOp):
            v = ev(node.operand)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, ast.BinOp):
            return _BINARY[type(node.op)](ev(node.left), ev(node.right))
        if isinstance(node, ast.Compare):
            left = ev(node.left)
            for op, right_node in zip(node.ops, node.comparators):
                right = ev(right_node)
                if not _COMPARE[type(op)](left, right):
                    return False
                left = right
            return True
        if isinstance(node, ast.BoolOp):
            values = [ev(v) for v in node.values]
            return all(values) if isinstance(node.op, ast.And) else any(values)
        if isinstance(node, ast.Call):
            return FUNCTIONS[node.func.id](*[ev(a) for a in node.args])
        raise FormulaError(f"{text!r}: cannot evaluate {type(node).__name__}")

    return ev(tree)
