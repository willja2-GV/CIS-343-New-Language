import unittest
import io
from unittest.mock import patch
from tempython import Tempython, main
from scanner import scanner
from tokenType import TokenType

class TestTypes(unittest.TestCase):
    
    def testindividualtokentype(self):
        test_tokens = '(){},.-+;*'
        tokens = scanner(test_tokens).scanTokens()
        expected_output = [TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN, TokenType.LEFT_BRACE, TokenType.RIGHT_BRACE, 
        TokenType.COMMA, TokenType.DOT, TokenType.MINUS, TokenType.PLUS, TokenType.SEMICOLON, TokenType.STAR, TokenType.EOF]
        actual_output = []
        for token in tokens:
            actual_output.append(token.type)
        self.assertEqual(actual_output, expected_output)

    def testgroupedtokentype(self):
        test_tokens = '! != = == < <= > >= /'
        tokens = scanner(test_tokens).scanTokens()
        expected_output = [TokenType.BANG, TokenType.BANG_EQUAL, TokenType.EQUAL, TokenType.EQUAL_EQUAL, TokenType.LESS,
        TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.SLASH, TokenType.EOF]
        actual_output = []
        for token in tokens:
            actual_output.append(token.type)
        self.assertEqual(actual_output, expected_output)

    def testgliteraltype(self):
        test_tokens = 'a b ab ands and class else false for fun if nil or print return super this true var while "and" 1 12 12.0'
        tokens = scanner(test_tokens).scanTokens()
        expected_output = [TokenType.IDENTIFIER, TokenType.IDENTIFIER, TokenType.IDENTIFIER, TokenType.IDENTIFIER, 
        TokenType.AND, TokenType.CLASS, TokenType.ELSE, TokenType.FALSE, TokenType.FOR, TokenType.FUN, TokenType.IF,
        TokenType.NIL, TokenType.OR, TokenType.PRINT, TokenType.RETURN, TokenType.SUPER, TokenType.THIS, TokenType.TRUE,
        TokenType.VAR, TokenType.WHILE, TokenType.STRING, TokenType.NUMBER, TokenType.NUMBER, TokenType.NUMBER, TokenType.EOF]
        actual_output = []
        for token in tokens:
            actual_output.append(token.type)
        self.assertEqual(actual_output, expected_output)

class TestRuleViolations(unittest.TestCase):

    @patch("sys.stdout", new_callable=io.StringIO)
    def teststringerror(self, mock_stdout):
        test_tokens = 'a"'
        scanner(test_tokens).scanTokens()
        self.assertEqual(
            mock_stdout.getvalue(),
            "[line 1] Error: Unterminated string.\n")

    @patch("sys.stdout", new_callable=io.StringIO)
    def testcharactererror(self, mock_stdout):
        test_tokens = '@'
        scanner(test_tokens).scanTokens()
        self.assertEqual(
            mock_stdout.getvalue(),
            "[line 1] Error: Unexpected character.\n")
        
    @patch("sys.stdout", new_callable=io.StringIO)
    def testerrorcheckingline(self, mock_stdout):
        test_tokens = '\n @'
        scanner(test_tokens).scanTokens()
        self.assertEqual(
            mock_stdout.getvalue(),
            "[line 2] Error: Unexpected character.\n")

class TestModes(unittest.TestCase):

    def testinteractive(self):
        t = Tempython()
        with patch("builtins.input", side_effect=['1 a', KeyboardInterrupt]), patch("builtins.print") as mock_print:
            t.run_prompt()
        output_lines = []
        for call in mock_print.call_args_list:
            first_argument = call.args[0]
            output_lines.append(str(first_argument))
        output = "\n".join(output_lines)
        expected = """TokenType.NUMBER 1 1.0
TokenType.IDENTIFIER a None
TokenType.EOF  None"""
        self.assertEqual(output, expected)
       
    def testinteractivexit(self):
        t = Tempython()
        with patch("builtins.input", side_effect=KeyboardInterrupt), patch.object(t, "run") as mock_run:
            t.run_prompt()
        mock_run.assert_not_called()
                    
    def testsource(self):
        t = Tempython()
        with patch("builtins.print") as mock_print:
            t.run_file(path='src/scanner.tempython')
        output_lines = []
        for call in mock_print.call_args_list:
            first_argument = call.args[0]
            output_lines.append(str(first_argument))
        output = "\n".join(output_lines)

        expected = """TokenType.VAR var None
TokenType.IDENTIFIER greeting None
TokenType.EQUAL = None
TokenType.STRING "hello" hello
TokenType.SEMICOLON ; None
TokenType.PRINT print None
TokenType.IDENTIFIER greeting None
TokenType.SEMICOLON ; None
TokenType.NUMBER 123 123.0
TokenType.PLUS + None
TokenType.NUMBER 45.67 45.67
TokenType.BANG_EQUAL != None
TokenType.NUMBER 0 0.0
TokenType.SEMICOLON ; None
TokenType.EOF  None"""
        self.assertEqual(output, expected)

    def testerrorcontinuation(self):
        t = Tempython()
        with patch("builtins.input", side_effect=['@','b',KeyboardInterrupt]), patch.object(t, "run") as mock_run:
            t.run_prompt()
        mock_run.assert_any_call('b')

if __name__ == "__main__":
    unittest.main()