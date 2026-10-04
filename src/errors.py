import sys

#framework for handling error.
class error_handling:
    error_present = False
    @staticmethod
    def error(line, message):
        error_handling.report(line, "", message)

    @staticmethod
    def report(line, where, message): 
        print(f"[line {line}] Error{where}: {message}")
        error_handling.error_present = True