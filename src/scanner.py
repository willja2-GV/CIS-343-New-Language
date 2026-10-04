from tempython_token import Token
from tokenType import TokenType
from errors import error_handling

class scanner():
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = self.keywords()

    def scanTokens(self):
        while not self.isatEnd():
            self.start = self.current
            self.scanToken()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def isatEnd(self):
        return self.current >= len(self.source)

    def scanToken(self):
        character = self.advance()
        match character:
            case '(':
                self.addToken(TokenType.LEFT_PAREN)
            case ')':
                self.addToken(TokenType.RIGHT_PAREN)
            case '{':
                self.addToken(TokenType.LEFT_BRACE)
            case '}':
                self.addToken(TokenType.RIGHT_BRACE)
            case ',':
                self.addToken(TokenType.COMMA)
            case '.':
                self.addToken(TokenType.DOT)
            case '-':
                self.addToken(TokenType.MINUS)
            case '+':
                self.addToken(TokenType.PLUS)
            case ';':
                self.addToken(TokenType.SEMICOLON)
            case '*':
                self.addToken(TokenType.STAR)
            case '!':
                if self.match('='):
                    self.addToken(TokenType.BANG_EQUAL)
                else:
                    self.addToken(TokenType.BANG)
            case '=':
                if self.match('='):
                    self.addToken(TokenType.EQUAL_EQUAL)
                else:
                    self.addToken(TokenType.EQUAL)                
            case '<':
                if self.match('='):
                    self.addToken(TokenType.LESS_EQUAL)
                else:
                    self.addToken(TokenType.LESS)
            case '>':
                if self.match('='):
                    self.addToken(TokenType.GREATER_EQUAL)
                else:
                    self.addToken(TokenType.GREATER)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.isatEnd():
                        self.advance()
                else:
                    self.addToken(TokenType.SLASH)
            case ' ':
                pass
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.isDigit(character):
                    self.number()
                elif self.isAlpha(character):
                    self.identifier()
                else:
                    error_handling.error(self.line, "Unexpected character.")

    def advance(self):
        character = self.source[self.current]
        self.current += 1
        return character
    
    def addToken(self, TokenType, literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(TokenType, text, literal, self.line))

    def match(self, expected):
        if self.isatEnd():
            return False
        if (self.source[self.current] != expected):
            return False
        self.current += 1
        return True

    def peek(self):
        if self.isatEnd():
            return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.isatEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isatEnd():
            error_handling.error(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1: self.current - 1]
        self.addToken(TokenType.STRING, value)

    def isDigit(self, character):
        return character >= '0' and character <= '9'

    def number(self):
        while self.isDigit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.advance()
            while self.isDigit(self.peek()):
                self.advance()
        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        text = self.source[self.start:self.current];
        type = self.keywords.get(text, TokenType.IDENTIFIER);
        self.addToken(type)

    def isAlpha(self, character):
        return ((character >= 'a' and character <= 'z') or (character >= 'A' and character <= 'Z') or character == '_')

    def isAlphaNumeric(self, character):
        return (self.isAlpha(character) or self.isDigit(character))

    def keywords(self):
        return {"and": TokenType.AND, "class": TokenType.CLASS, "else": TokenType.ELSE, "false": TokenType.FALSE,
        "for": TokenType.FOR,"fun": TokenType.FUN, "if": TokenType.IF, "nil": TokenType.NIL, "or": TokenType.OR,
        "print": TokenType.PRINT, "return": TokenType.RETURN, "super": TokenType.SUPER, "this": TokenType.THIS,
        "true": TokenType.TRUE, "var": TokenType.VAR, "while": TokenType.WHILE}
        

