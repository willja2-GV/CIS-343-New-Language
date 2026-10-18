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

Design choices: This section of project sticks to lox very closely. I am unsure if my implementation of dealing with 
    trailing semi-colon tokens by raising an EOF error is in line with lox. In the backend, naming schemes were changed for
    convenience. No departures were made from the lab 2 grammar rules.

Dependency/setup instructions for tests: The Lab3.txt file contains the test cases. tempython.py should be run. Each test case
    should be copied to the tempython.py terminal one at a time. The output will be printed to the terminal after hitting enter. The example.py has the test for the source input test. This should be run by typing py src/tempython.py example.py into the terminal.

Test cases: 

    The following test case confirms that every expression form can be printed. The expected output and actual output is
    below which matches the intention.
        "1" + 1 - 2 + (1 * 2)!= -5 + !5
            (!= (+ (- (+ 1 1.0) 2.0) (group (* 1.0 2.0))) (- 5.0) (! 5.0))

    The following test case confirms that every literal type and operator can be printed. The expected and actual output which matches the intention is below test.
        "1" == 2 + true - false < nil > 1.0 <= 1.11 >= 21.1 != 1 * 3 / 4
            (!= (== 1 (>= (<= (> (< (- (+ 2.0 True) False) nil) 1.0) 1.11) 21.1)) (/ (* 1.0 3.0) 4.0))

    The following test case confirms that every requested error can be identified. The expected and actual output which matches the intention is below each test. After any of these another one can be tested to ensure interactive mode did not end.
        Unmatched parantheses
        (1 + 2
            [line 1] Error at end: Expect ')' after expression.
        1 + 2)
            [line 1] Error at ')': Expected end of expression.
        Unterminated strings    
        "1
            [line 1] Error: Unterminated string.
            [line 1] Error at end: Expect expression.
        1"
            [line 1] Error: Unterminated string.
        Missing operand
        1 +
            [line 1] Error at end: Expect expression.
        Unexpected character
        1 + ^
            [line 1] Error: Unexpected character.
            [line 1] Error at end: Expect expression.
        Trailing character
        1 + 2 4
            [line 1] Error at '4': Expected end of expression.

    The following test confirms that a source file can be used to print an ast. The expected and actual output match the test below.
        py src/tempython.py example.py 
            (!= (- 123.0 23.0) 1.0)

Diagrammed syntax tree: The expression 1 + -2 gives the syntax tree seen below. The output is (+ 1.0 (- 2.0)).
                        expression
                            ↓
                          binary
                            ↓
              expression operator expression
                  ↓         ↓         ↓
               literal      +       unary
                  ↓                 ↓   ↓
                number              - expression  
                  ↓                     ↓  
                  1                  literal
                                        ↓
                                      number
                                        ↓
                                        2
    The ast the programs is in prefix first notation and is parenthesize. This gives the binary-unary expression operator first, first literal second, and unary third. The syntax tree above uses an infix order with 1 + -2. They both follow the same expression grammar as described in lox.   

Limitations/failing tests: All tests are working as intended. There may be limitations in that not all possible combinations of
    literals, operators, unaries, and groupings were tested. There were limitations in that only one test was run using a source file, assuming behavoir is consistent with running from interactive mode.