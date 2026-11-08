import sys
from tokenType import TokenType
from tempython_token import Token

#framework for handling error.
class error_handling:
    error_present = False
    hadRuntimeError = False
    @staticmethod
    def error(line, message):
        error_handling.report(line, "", message)

    @staticmethod
    def report(line, where, message): 
        print(f"[line {line}] Error{where}: {message}")
        error_handling.error_present = True

    @staticmethod
    def errors(token, message):
        if token.type == TokenType.EOF:
            error_handling.report(token.line, " at end", message)
        else:
            error_handling.report(token.line, f" at '{token.lexeme}'", message)

    @staticmethod
    def runtimeError(error):
        print(error.getMessage() + "\n[line " + error.token.line + "]")
        error_handling.hadRuntimeError = True