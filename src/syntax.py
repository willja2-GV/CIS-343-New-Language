from abc import ABC

class expression(ABC):
    def accept(self, visitor):
        pass


class binary(expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class literal(expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
            return visitor.visitLiteralExpr(self)

class grouping(expression):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
            return visitor.visitGroupingExpr(self)

class unary(expression):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
            return visitor.visitUnaryExpr(self)
