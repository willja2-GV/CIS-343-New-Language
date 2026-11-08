from tokenType import TokenType
from runtimeError import RuntimeError
from errors import error_handling
from environment import Environment

class Interpreter():
    def __init__(self, visitor):
        self.visitor = visitor
        self.environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError:
            error_handling.error(RuntimeError)

    def visitLiteralExpr(self, experssion):
        return experssion.value

    def visitGroupingExpr(self, expression):
        return self.evaluate(expression.expression)

    def evaluate(self, expression):
        return expression.accept(self)

    def execute(self, Stmt):
        Stmt.accept(self)

    def executeBlock(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visitBlockStmt(self, Stmt):
        self.executeBlock(Stmt.statements, Environment(self.environment))
        return None

    def visitExpressionStmt(self, Stmt):
        self.evaluate(Stmt.expression)
        return None

    def visitPrintStmt(self, Stmt):
        value = self.evaluate(Stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, Stmt):
        value = None
        if Stmt.initializer is not None:
            value = self.evaluate(Stmt.initializer)
        self.environment.define(Stmt.name.lexeme, value)
        return None

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitUnaryExpr(self, expression):
        right = self.evaluate(expression.right)
        if expression.operator.type == TokenType.BANG:
            return not self.isTruthy(right)
        if expression.operator.type == TokenType.MINUS:
            self.checkNumberOperand(expression.operator, right)
            return -float(right)
        return None

    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    def checkNumberOperand(self, operator, operand):
        if isinstance(operand, float):
            return True
        raise RuntimeError(operator, "Operand must be a number.")

    def checkNumberOperands(self, operator, left, right):
        if isinstance(left, (float, bool)) and isinstance(right, (float, bool)):
            return True
        raise RuntimeError(operator, "Operands must be numbers.")

    def isTruthy(self, object):
        if object is None:
            return False
        if isinstance(object, bool):
            return bool(object)
        return True

    def isEqual(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b

    def stringify(self, object):
        if object is None:
            return "nil"
        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[0:-2]
            return text
        return str(object)

    def convertValue(self, value):
        if isinstance(value, bool):
            return float(value)
        return value

    def visitBinaryExpr(self, expression):
        left =  self.evaluate(expression.left)
        right =  self.evaluate(expression.right)
        if expression.operator.type == TokenType.GREATER:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) > self.convertValue(right)
        if expression.operator.type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) >= self.convertValue(right)
        if expression.operator.type == TokenType.LESS:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) < self.convertValue(right)
        if expression.operator.type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) <= self.convertValue(right)
        if expression.operator.type == TokenType.MINUS:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) - self.convertValue(right)
        if expression.operator.type == TokenType.PLUS:
            if (isinstance(left, (float, bool)) and isinstance(right, (float, bool))):
                return self.convertValue(left) + self.convertValue(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeError(expression.operator, "Operands must be two numbers or two strings.")
        if expression.operator.type == TokenType.SLASH:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) / self.convertValue(right)
        if expression.operator.type == TokenType.STAR:
            self.checkNumberOperands(expression.operator, left, right)
            return self.convertValue(left) * self.convertValue(right)
        if expression.operator.type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        if expression.operator.type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)
        return None