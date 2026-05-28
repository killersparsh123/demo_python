import ast
import operator as op
import math
import os
import readline

# safe map of operators
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

_ALLOWED_UNARYOPS = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}

# allowed functions and constants from math
_ALLOWED_FUNCS = {name: getattr(math, name) for name in (
    "sin", "cos", "tan", "asin", "acos", "atan", "sqrt",
    "log", "log10", "exp", "fabs", "floor", "ceil", "degrees", "radians"
)}
_ALLOWED_CONSTS = {"pi": math.pi, "e": math.e}

history = []
memory = 0.0

def eval_node(node):
    if isinstance(node, ast.Expression):
        return eval_node(node.body)
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if hasattr(ast, "Constant") and isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")
    if isinstance(node, ast.BinOp):
        left = eval_node(node.left)
        right = eval_node(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_BINOPS:
            return _ALLOWED_BINOPS[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = eval_node(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_UNARYOPS:
            return _ALLOWED_UNARYOPS[op_type](operand)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Unsupported function call")
        func_name = node.func.id
        if func_name not in _ALLOWED_FUNCS:
            raise ValueError(f"Function '{func_name}' not allowed")
        args = [eval_node(a) for a in node.args]
        return _ALLOWED_FUNCS[func_name](*args)
    if isinstance(node, ast.Name):
        if node.id == "mem":
            return memory
        if node.id in _ALLOWED_CONSTS:
            return _ALLOWED_CONSTS[node.id]
        raise ValueError(f"Unknown name: {node.id}")
    raise ValueError("Unsupported expression element")

def evaluate(expr):
    try:
        parsed = ast.parse(expr, mode="eval")
        return eval_node(parsed)
    except Exception as e:
        raise ValueError(str(e))

def print_help():
    print("Commands:")
    print("  help            show this help")
    print("  history         show calculation history")
    print("  clear           clear screen")
    print("  mem             show memory value")
    print("  mem+ <expr>     add expression result to memory")
    print("  mem- <expr>     subtract expression result from memory")
    print("  memr            recall memory (same as using 'mem' in expression)")
    print("  quit / exit     exit calculator")
    print("")
    print("You can type arithmetic expressions, use math functions like sin(), sqrt(),")
    print("and constants pi, e. Use 'mem' in expressions to refer to stored memory value.")

def repl():
    global memory
    print("CLI Calculator — type 'help' for commands, 'quit' to exit.")
    while True:
        try:
            s = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not s:
            continue
        if s.lower() in ("quit", "exit"):
            break
        if s.lower() == "help":
            print_help()
            continue
        if s.lower() == "history":
            if not history:
                print("(no history)")
            else:
                for i, (expr, res) in enumerate(history, 1):
                    print(f"{i}: {expr} = {res}")
            continue
        if s.lower() == "clear":
            os.system("clear")
            continue
        if s.lower() == "mem":
            print(f"memory = {memory}")
            continue
        if s.lower().startswith("mem+"):
            rest = s[4:].strip()
            if not rest:
                print("Usage: mem+ <expression>")
                continue
            try:
                val = evaluate(rest)
                memory += val
                print(f"memory = {memory}")
            except Exception as e:
                print("Error:", e)
            continue
        if s.lower().startswith("mem-"):
            rest = s[4:].strip()
            if not rest:
                print("Usage: mem- <expression>")
                continue
            try:
                val = evaluate(rest)
                memory -= val
                print(f"memory = {memory}")
            except Exception as e:
                print("Error:", e)
            continue
        if s.lower() == "memr":
            print(memory)
            continue

        # Evaluate general expression
        try:
            result = evaluate(s)
            history.append((s, result))
            print(result)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    repl()