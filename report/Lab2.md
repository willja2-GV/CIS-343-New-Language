Expression grammar: The expression grammar is represented in as
    expression     → literal
                    | unary
                    | binary
                    | grouping 
    literal         → NUMBER | STRING | "true" | "false" | "nil" 
    grouping        → "(" expression ")" 
    unary           → ( "-" | "!" ) expression 
    binary          → expression operator expression 
    operator        → "==" | "!=" | "<" | "<=" | ">" | ">="
                    | "+"  | "-"  | "*" | "/" 

Design choices: This section of project sticks to lox very closely. In the backend, naming schemes were changed for convenience.

Dependency/setup instructions for tests: The Lab2.txt file contains the test cases. Each test case should be copied to 
    ast_print.py to replace the default test at the bottom of that file. ast_print.py should be run. The output will be printed to the terminal.

Test cases: 
    The following test case confirms that every class of expression can be printed. The expected output and actual output is
    (* (- 1) (group 2)) which matches the intention.
        Expression = Expression = expression.binary(
        expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.literal(1)),
        Token(TokenType.STAR, "*", None, 1), expression.grouping(expression.literal(2)))
        print(AstPrinter().print(Expression))

    The following test cases confirms that every literal type, operator, and unary can be printed. The expected and actual output
    which matches the intention is below each test.
        Expression = expression.binary(expression.literal(1), Token(TokenType.EQUAL_EQUAL, "==", None, 1), expression.literal(2))
            (== 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.BANG_EQUAL, "!=", None, 1), expression.literal(2))
            (!= 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.GREATER, "<", None, 1), expression.literal(2))
            (< 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.GREATER_EQUAL, "<=", None, 1), expression.literal(2))
            (<= 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.LESS, ">", None, 1), expression.literal(2))
            (> 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.LESS_EQUAL, ">=", None, 1), expression.literal(2))
            (>= 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.PLUS, "+", None, 1), expression.literal(2))
            (+ 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.MINUS, "-", None, 1), expression.literal(2))
            (- 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.STAR, "*", None, 1), expression.literal(2))
            (* 1 2)
        Expression = expression.binary(expression.literal(1), Token(TokenType.SLASH, "/", None, 1), expression.literal(2))
            (/ 1 2)
        Expression = expression.binary(expression.literal("1"), Token(TokenType.SLASH, "/", None, 1), expression.literal("2"))
            (/ 1 2)
        Expression = expression.binary(expression.literal("a"), Token(TokenType.SLASH, "/", None, 1), expression.literal("b"))
            (/ a b)
        Expression = expression.binary(expression.literal("a"), Token(TokenType.SLASH, "/", None, 1), expression.literal(""))
            (/ a )
        Expression = expression.binary(expression.literal("true"), Token(TokenType.SLASH, "/", None, 1), expression.literal("false"))
            (/ true false)
        Expression = expression.binary(expression.literal("true"), Token(TokenType.SLASH, "/", None, 1), expression.literal("nil"))
            (/ true nil)
        Expression = expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.literal(1))
            (- 1)
        Expression = expression.unary(Token(TokenType.BANG, "!", None, 1), expression.literal(1))
            (! 1)``

    The following test cases confirms that every type of nested call can be printed. The expected and actual output
    which matches the intention is below each test.
        Expression = expression.binary(expression.binary(expression.literal(1), Token(TokenType.STAR, "*", None, 1), expression.literal(1)), Token(TokenType.STAR, "*", None, 1), expression.literal(1))
            (* (* 1 1) 1)
        Expression = expression.binary(expression.grouping(expression.literal(1)), Token(TokenType.STAR, "*", None, 1), expression.literal(1))
            (* (group 1) 1)
        Expression = expression.binary(expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.literal(1)), Token(TokenType.STAR, "*", None, 1), expression.literal(1))
            (* (- 1) 1)
        Expression = expression.grouping((expression.binary(expression.literal(1), Token(TokenType.STAR, "*", None, 1), expression.literal(1))))
            (group (* 1 1))
        Expression = expression.grouping(expression.grouping(expression.literal(1)))
            (group (group 1))
        Expression = expression.grouping((expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.literal(1))))
            (group (- 1))
        Expression = expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.binary(expression.literal(1), Token(TokenType.STAR, "*", None, 1), expression.literal(1)))
            (- (* 1 1))
        Expression = expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.grouping(expression.literal(1)))
            (- (group 1))
        Expression = expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.unary(Token(TokenType.MINUS, "-", None, 1), expression.literal(1)))
            (- (- 1))


Limitations/failing tests: All tests are working as intended. There may be limitations in that not all possible combinations of
    literals, operators, unaries, and groupings were tested.