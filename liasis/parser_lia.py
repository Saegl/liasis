from lark import Lark, InlineTransformer
from . import ast_lia


grammar = """
?program: global_stmt*    -> program

?global_stmt: trait_def
    | struct_def
    | stmt

?trait_stmt: stmt
    | abs_func

?stmt: print
    | while_expr
    | func_def
    | conditional
    | cmp
    | assign
    | expr

print: "print" expr    -> print_

assign: NAME "=" expr    -> assign_var

struct_def: "struct" NAME "{" stmt* "}"    -> struct_def

trait_def: "trait" NAME "{" trait_stmt* "}"    -> trait_def

abs_func: "function" NAME argslist    -> abs_func

func_def: "function" NAME argslist "{" stmt* "}"    -> function_def

argslist: "(" [NAME ("," NAME)*] ")"    -> argslist

?cmp: expr cmp_op expr
!?cmp_op: "<"|"<="|"=="|"!="|">"|">="

conditional: "if" cmp "{" expr "}" "else" "{" expr "}"    -> conditional

while_expr: "while" cmp "{" stmt* "}"    -> while_expr

!?expr: product
    | expr "+" product    -> arith
    | expr "-" product    -> arith

!?product: atom
    | product "*" atom    -> arith
    | product "/" atom    -> arith

?atom: function_call
    | string
    | boolean
    | NUMBER    -> number
    | "-" atom    -> neg
    | NAME    -> var
    | "(" expr ")"

string: ESCAPED_STRING

!boolean: "true" | "false"    -> boolean

function_call: NAME exprlist    -> function_call

exprlist: "(" [expr ("," expr)*] ")"    -> exprlist

%import common.NUMBER
%import common.CNAME    -> NAME
%import common.WS
%import common.ESCAPED_STRING

%ignore WS
"""


class MakeAst(InlineTransformer):
    number = int

    def boolean(self, s):
        if s == 'true':
            return ast_lia.Boolean(True)
        elif s == 'false':
            return ast_lia.Boolean(False)
        else:
            raise TypeError("Unreachable")

    def string(self, s):
        return s[1:-1].replace('\\"', '"')

    def program(self, *list_):
        return list_

    def arith(self, lhs, op, rhs):
        return ast_lia.Arith(lhs, rhs, op)

    def assign_var(self, name, value):
        return ast_lia.VarAssign(name.value, value)

    def var(self, name):
        return ast_lia.GetVar(name.value)

    def trait_def(self, name, *body):
        return ast_lia.Trait(name, body)

    def abs_func(self, name, func_args):
        print(name)
        return ast_lia.AbsFunc(name.value, func_args)

    def function_def(self, name, func_args, *body):
        return ast_lia.FuncDef(name.value, func_args, body)

    def function_call(self, name, args):
        return ast_lia.FuncCall(name.value, args)

    def argslist(self, *args):
        return tuple(arg.value for arg in args)

    def exprlist(self, *args):
        return args

    def cmp(self, lhs, op, rhs):
        return ast_lia.Cmp(lhs, rhs, op.value)

    def conditional(self, if_, then, else_):
        return ast_lia.Conditional(if_, then, else_)

    def while_expr(self, cmp, *body):
        return ast_lia.While(cmp, body)

    def print_(self, s):
        return ast_lia.Print(s)


parser = Lark(grammar, start='program', parser='lalr', transformer=MakeAst())
parse = parser.parse


def test():
    tree = parser.parse('1 + 1')
    print(tree[0])


if __name__ == '__main__':
    test()
