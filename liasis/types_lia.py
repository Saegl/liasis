class Object:
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value


class Trait:
    def __init__(self, name: str, methods: list):
        self.name = name
        self.methods = methods


class Type:
    def call_method(self, name, args):
        pass

    def new(self):
        pass

    def repr(self):
        return "No repr"


class Bool(Type):
    def __init__(self, b: bool):
        self.b = b

    def repr(self):
        return "true" if self.b else "false"


class String(Type):
    def __init__(self, text: str):
        self.text = text

    def add(self, other):
        return String(self.text + other.text)

    def repr(self):
        return self.text


class Int(Type):
    def __init__(self, value: int):
        self.value = value

    def add(self, other):
        return Int(self.value + other.value)

    def sub(self, other):
        return Int(self.value - other.value)

    def mul(self, other):
        return Int(self.value * other.value)

    def div(self, other):
        return Int(self.value // other.value)

    def lt(self, other):
        return Bool(True) if self.value < other.value else Bool(False)

    def le(self, other):
        return Bool(True) if self.value <= other.value else Bool(False)

    def eq(self, other):
        return Bool(True) if self.value == other.value else Bool(False)

    def ne(self, other):
        return Bool(True) if self.value != other.value else Bool(False)

    def gt(self, other):
        return Bool(True) if self.value > other.value else Bool(False)

    def ge(self, other):
        return Bool(True) if self.value >= other.value else Bool(False)

    def repr(self):
        return self.to_string().text

    def to_string(self):
        return String(str(self.value))

    def call_method(self, name, args):
        pass


class Struct(Type):
    def __init__(self, name: str, fields: dict):
        self.name = name
        self.fields = fields
    
    def new(self) -> Object:
        return Object(self, 1)

    def call_method(self, method_name, args):
        pass
    
    def impl_trait(self, trait: Trait, methods: list):
        pass


if __name__ == '__main__':
    inttype = Struct("Add", {})
