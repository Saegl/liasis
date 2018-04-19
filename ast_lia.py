class AstToken:
    def __repr__(self):
        return self.__class__.__name__


class Boolean(AstToken):
    __slots__ = ("b",)

    def __init__(self, b: bool):
        self.b = b

    def __bool__(self):
        return self.b


class Struct(AstToken):
    __slots__ = ('name', 'fields')

    def __init__(self, name, fields):
        self.name = name
        self.fields = fields


class Trait(AstToken):
    __slots__ = ('name', 'body')

    def __init__(self, name: str, body):
        self.name = name
        self.body = body


class FuncCall(AstToken):
    __slots__ = ('name', 'args')

    def __init__(self, name: str, args: list):
        self.name: str = name
        self.args = args


class FuncDef(AstToken):
    __slots__ = ('name', 'args', 'body')

    def __init__(self, name: str, args: tuple, body: tuple):
        self.name = name
        self.args = args
        self.body = body


class AbsFunc(AstToken):
    __slots__ = ('name', 'args')

    def __init__(self, name: str, args: tuple):
        self.name = name
        self.args = args

    def valid(self, func) -> bool:
        pass


class Arith(AstToken):
    """Arithmetic operations"""
    __slots__ = ("lhs", "rhs", "op")

    def __init__(self, lhs, rhs, op: str):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op


class VarAssign(AstToken):
    __slots__ = ("name", "value")

    def __init__(self, name: str, value):
        self.name = name
        self.value = value


class GetVar(AstToken):
    __slots__ = ("name", )

    def __init__(self, name: str):
        self.name = name


class Cmp(AstToken):
    """Comparison
    lt <
    le <=
    eq ==
    ne !=
    gt >
    ge >=
    """
    __slots__ = ("lhs", "rhs", "op")

    def __init__(self, lhs, rhs, op: str):
        self.lhs = lhs
        self.rhs = rhs
        self.op = op


class Conditional(AstToken):
    __slots__ = ("if_", "then", "else_")

    def __init__(self, if_, then, else_):
        self.if_ = if_
        self.then = then
        self.else_ = else_


class While(AstToken):
    __slots__ = ("cmp", "body")

    def __init__(self, cmp, body: tuple):
        self.cmp = cmp
        self.body = body


class Print(AstToken):
    __slots__ = ("expr",)

    def __init__(self, expr):
        self.expr = expr
