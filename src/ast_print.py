from tokenType import TokenType
from tempython_token import Token
from syntax import Expr, binary, literal, unary, grouping


class AstPrinter():
    def print(self, expression):
        return expression.accept(self)


    def visitBinaryExpr(self, expression): 
        return self.parenthesize(expression.operator.lexeme, expression.left, expression.right)


    def visitGroupingExpr(self, expression): 
        return self.parenthesize("group", expression.expression)
 
    def visitLiteralExpr(self, expression):
        if expression.value is None:
            return "nil"
        return str(expression.value)
  
    def visitUnaryExpr(self, expression): 
        return self.parenthesize(expression.operator.lexeme, expression.right)

    def parenthesize(self, name, *expression):
        result = "(" + name
        for expr in expression:
            result += " "
            result += expr.accept(self)
        result += ")"
        return result

def main():
    Expr.binary = binary
    Expr.unary = unary
    Expr.literal = literal
    Expr.grouping = grouping

    Expression = Expr.unary(Token(TokenType.MINUS, "-", None, 1), Expr.unary(Token(TokenType.MINUS, "-", None, 1), Expr.literal(1)))

    print(AstPrinter().print(Expression))

if __name__ == "__main__":
    main()