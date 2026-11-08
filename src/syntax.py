from abc import ABC

class Expr(ABC):
    def accept(self, visitor):
        pass

class Stmt(ABC):
    def accept(self, visitor):
        pass

class block(Stmt):
    def __init__(self, statements):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)
        
class expression(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)

class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)
    
class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVarStmt(self)

class assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value
         
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)

class binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class literal(Expr):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
            return visitor.visitLiteralExpr(self)

class grouping(Expr):
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
            return visitor.visitGroupingExpr(self)

class unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
            return visitor.visitUnaryExpr(self)
    
class variable(Expr):
    def __init__(self, name):
        self.name = name 

    def accept(self, visitor):
        return visitor.visitVariableExpr(self)