Design choices: This section of project sticks to lox very closely. In the backend, naming schemes were changed for
    convenience. No departures were made from the previous grammar rules.

Dependency/setup instructions for tests: The Lab4.txt file contains the test cases. Each test case
    should be copied to the src/scanner.tempython file one at a time. This should be run by typing py src/tempython.py src/scanner.tempython into the terminal. The output will be printed to the terminal after running the file.

Test Cases:
    The following test case confirms that inputs with syntax errors will not give an evaluated output, will continue to indentify other syantax errors, and give the corresponding error message. The expected output and actual output is below which matches the intention.
        "one"
        true;
        print 2 +
            [line 2] Error at 'true': Expect ';' after expression.
            [line 3] Error at end: Expect expression.

    The following test case confirms that expression statements can be parsed, print statements can be executed for the basic data types, statements without a print will give no output, and expression statements can be evaluated and printed in the same line. The expected output and actual output is below which matches the intention.
        4 + 2;
        print "one";
        print true;
        print 1 + 2;
        print nil;
            one
            True
            3
            nil

Limitations/failing tests: All tests are working as intended. There may be limitations in that not all possible combinations
    were tested.