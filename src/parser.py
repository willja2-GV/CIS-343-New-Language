from tokenType import TokenType
from errors import error_handling
from syntax import Expr as expr
from syntax import binary, literal, unary, grouping, variable
from syntax import Stmt
from syntax import expression, Print, Var, block
Stmt.block = block
Stmt.Print = Print
Stmt.expression = expression
Stmt.Var = Var
expr.binary = binary
expr.unary = unary
expr.literal = literal
expr.grouping = grouping
expr.variable = variable

class Parser():
    class ParseError(RuntimeError):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.vardeclaration()
            return self.statement()
        except self.ParseError:
            self.synchronize()
            return None

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
        if (self.match(TokenType.IDENTIFIER)):
            return expr.variable(self.previous())
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
                case TokenType.CLASS:
                    return
                case TokenType.FUN:
                    return
                case TokenType.VAR:
                    return
                case TokenType.FOR:
                    return
                case TokenType.IF:
                    return
                case TokenType.WHILE:
                    return
                case TokenType.PRINT:
                    return
                case TokenType.RETURN:
                    return
            self.advance()

    def parse(self):
        statement = []
        while not self.isatend():
            statement.append(self.declaration())
        return statement

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.LEFT_BRACE):
            return Stmt.block(self.block([]))
        return self.expressionStatement()

    def block(self, statements):
        while not self.check(TokenType.RIGHT_BRACE) and not self.isatend():
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Print(value)    

    def vardeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def expressionStatement(self):
        expressions = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.expression(expressions)

    def assignment(self):
        expression = self.equality()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expression, expr.variable):
                name = expr.variable.name
                return expr.assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expression