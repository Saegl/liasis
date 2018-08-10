from collections import namedtuple

from . import types_lia as tt
from .parser_lia import ast_lia, parse


Function = namedtuple("Function", "args body")


class EngineError(Exception):
    pass


class VirtualMemory:
    def __init__(self):
        self.objs = []
        self.vars = {}

    def add_var(self, name, obj):
        self.objs.append(obj)
        self.vars[name] = len(self.objs)

    def get_var(self, name):
        return self.objs[self.vars[name]]


class VirtualLiasisMachine:
    def __init__(self):
        self.last_result = None
        self.vars = {}
        self.traits = {}
        self.structs = {}
        self.update_default_types()

    def update_default_types(self):
        self.traits['add'] = tt.Trait("Add", [])
        self.structs['int'] = tt.Struct("Int", {})

    def exe_tok(self, token, scope: dict):
        if isinstance(token, ast_lia.Arith):
            lhs = self.exe_tok(token.lhs, scope)
            rhs = self.exe_tok(token.rhs, scope)
            if token.op == "+":
                return lhs.add(rhs)
            elif token.op == "-":
                return lhs.sub(rhs)
            elif token.op == "*":
                return lhs.mul(rhs)
            elif token.op == "/":
                return lhs.div(rhs)
            else:
                raise EngineError("Unreachable")
        elif isinstance(token, ast_lia.Boolean):
            return tt.Bool(True) if token.b else tt.Bool(False)
        elif isinstance(token, ast_lia.Print):
            print(self.exe_tok(token.expr, scope).repr())
        elif isinstance(token, ast_lia.Conditional):
            if self.exe_tok(token.if_, scope).b:
                return self.exe_tok(token.then, scope)
            else:
                return self.exe_tok(token.else_, scope)
        elif isinstance(token, ast_lia.While):
            while self.exe_tok(token.cmp, scope).b:
                for tok in token.body:
                    self.exe_tok(tok, scope)
        elif isinstance(token, ast_lia.Cmp):
            lhs = self.exe_tok(token.lhs, scope)
            rhs = self.exe_tok(token.rhs, scope)
            if token.op == ">":
                return lhs.gt(rhs)
            elif token.op == "<":
                return lhs.lt(rhs)
            elif token.op == "==":
                return lhs.eq(rhs)
            elif token.op == "!=":
                return lhs.ne(rhs)
            elif token.op == ">=":
                return lhs.ge(rhs)
            elif token.op == "<=":
                return lhs.le(rhs)
            else:
                raise EngineError("Invalid op in comparison")
        elif isinstance(token, int):
            return tt.Int(token)
        elif isinstance(token, str):
            return tt.String(token)
        elif isinstance(token, ast_lia.GetVar):
            return scope[token.name]
        elif isinstance(token, ast_lia.VarAssign):
            self.vars[token.name] = self.exe_tok(token.value, scope)
        elif isinstance(token, ast_lia.FuncDef):
            self.vars[token.name] = Function(token.args, token.body)
        elif isinstance(token, ast_lia.FuncCall):
            func = self.vars[token.name]
            if isinstance(func, Function):
                arg_names = func.args
                arg_values = tuple(self.exe_tok(arg, scope) for arg in token.args)
                func_scope = dict(zip(arg_names, arg_values))

                resp = None
                for tok in func.body:
                    resp = self.exe_tok(tok, func_scope)
                return resp
            else:
                raise EngineError(f"{token.name} is not a function")
        elif isinstance(token, ast_lia.AbsFunc):
            pass
        elif isinstance(token, ast_lia.Trait):
            self.traits[token.name] = token.body
        else:
            raise EngineError(f"Invalid ast: {token}")

    def execute(self, s):
        for node in parse(s):
            self.last_result = self.exe_tok(node, self.vars)
