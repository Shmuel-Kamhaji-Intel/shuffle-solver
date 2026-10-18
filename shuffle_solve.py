import ast
import json
import math
import operator
import sys

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}
FUNCS = {"sin": math.sin, "cos": math.cos, "tan": math.tan, "log": math.log}
NAMES = {"e": math.e, "pi": math.pi}


def ev(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        return NAMES[node.id]
    if isinstance(node, ast.BinOp):
        return OPS[type(node.op)](ev(node.left), ev(node.right))
    if isinstance(node, ast.UnaryOp):
        return OPS[type(node.op)](ev(node.operand))
    if isinstance(node, ast.Call):
        return FUNCS[node.func.id](*[ev(a) for a in node.args])
    raise ValueError("unsupported expression")


tree = ast.parse(sys.argv[1].replace("^", "**"), mode="eval")
answer = format(ev(tree.body), ".12g")
print(json.dumps({"answer": answer, "reversed": answer[::-1]}))
