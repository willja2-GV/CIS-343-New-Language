from tokenType import TokenType
from errors import error_handling
from syntax import expression as expr
from syntax import binary, literal, unary, grouping

expr.binary = binary
expr.unary = unary
expr.literal = literal
expr.grouping = grouping

class Parser():
    class ParseError(RuntimeError):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.equality()

    def equality(self):
        expression = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = expr.binary(expression, operator, right)
        return expression

    def comparison(self):
        expression = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expression = expr.binary(expression, operator, right)
        return expression

    def term(self):
        expression = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expression = expr.binary(expression, operator, right)
        return expression

    def factor(self):
        expression = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expression = expr.binary(expression, operator, right)
        return expression

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return expr.unary(operator, right)
        return self.primary()

    def primary(self):
        if (self.match(TokenType.FALSE)):
            return expr.literal(False)
        if (self.match(TokenType.TRUE)):
            return expr.literal(True)
        if (self.match(TokenType.NIL)): 
            return expr.literal(None)
        if (self.match(TokenType.NUMBER, TokenType.STRING)):
            return expr.literal(self.previous().literal);
        if (self.match(TokenType.LEFT_PAREN)):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return expr.grouping(expression)
        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types: TokenType):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, type):
        if self.isatend():
            return False
        return self.peek().type == type 

    def advance(self):
        if not self.isatend():
            self.current += 1
        return self.previous()

    def isatend(self): 
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        error_handling.errors(token, message)
        return Parser.ParseError()

    def synchronize(self):
        self.advance()
        while not self.isatend():
            if self.previous().type == TokenType.SEMICOLON:
                return
            match self.peek().type:
                        case 'CLASS':
                            pass
                        case 'FUN':
                            pass
                        case 'VAR':
                            pass
                        case 'FOR':
                            pass
                        case 'IF':
                            pass
                        case 'WHILE':
                            pass
                        case 'PRINT':
                            pass
                        case 'RETURN':
                            return
            self.advance()

    def parse(self):
        try:
            expression = self.expression()
            if not self.isatend():
                raise self.error(self.peek(), "Expected end of expression.")
            return expression
        except self.ParseError:
            return None