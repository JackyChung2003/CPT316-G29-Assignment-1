from typing import List, Union
from lexical_temp import Token, TokenType, LexicalAnalyzer

# Assuming Token and TokenType are already defined, as in your lexical analysis


class SyntaxError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    # Utility functions for parser
    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1

    def expect(self, type_: TokenType, value=None):
        token = self.current_token()
        if token and token.type == type_ and (value is None or token.value == value):
            self.advance()
            return token
        expected_value = value if value else type_.value
        raise SyntaxError(f"Expected {expected_value}, but got {token}")

    # Parse a complete PoliteLang program (sequence of statements)
    # Using grammar rules: <STATEMENT_LIST> ::= <STATEMENT> <STATEMENT_LIST> | ε
    def parse_program(self):
        statements = []
        while self.position < len(self.tokens):
            statements.append(self.parse_statement())
        return statements

    # Parse a single statement
    # Using grammar rules: <STATEMENT> ::= <STATEMENT> ::= pls <IDENTIFIER> = <EXPRESSION> thanks~
    #                                   | show(<EXPRESSION>) thanks~
    #                                   | whisper(<EXPRESSION>) thanks~
    #                                   | shout(<EXPRESSION>) thanks~
    #                                   | Check (<EXPRESSION>) { <STATEMENT_LIST> } [otherwise { <STATEMENT_LIST> }]
    #                                   | During (<EXPRESSION>) { <STATEMENT_LIST> }
    #                                   | Given <IDENTIFIER> in <EXPRESSION> { <STATEMENT_LIST> }
    def parse_statement(self):
        token = self.current_token()

        if token.type == TokenType.KEYWORD:
            if token.value == "pls":
                return self.parse_assignment()
            elif token.value == "show":
                return self.parse_print("show")
            elif token.value == "whisper":
                return self.parse_print("whisper")
            elif token.value == "shout":
                return self.parse_print("shout")
            elif token.value == "Check":
                return self.parse_if()
            elif token.value == "During":
                return self.parse_while()
            elif token.value == "Given":
                return self.parse_for()

        raise SyntaxError(f"Unexpected statement: {token}")

    # Parse an assignment statement
    # Using grammar rules: <ASSIGNMENT> ::= pls <IDENTIFIER> = <EXPRESSION> thanks~
    def parse_assignment(self):
        self.expect(TokenType.KEYWORD, "pls")
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.OPERATOR, "=")
        expression = self.parse_expression()
        self.expect(TokenType.END_STATEMENT, "thanks~")
        return f"Assignment({identifier.value} = {expression})"

    # Parse a print statement (show, whisper, or shout)
    # Using grammar rules: <PRINT> ::= show(<EXPRESSION>) thanks~
    #                               | whisper(<EXPRESSION>) thanks~
    #                               | shout(<EXPRESSION>) thanks~
    def parse_print(self, print_type):
        self.expect(TokenType.KEYWORD, print_type)
        self.expect(TokenType.SEPARATOR, "(")
        expression = self.parse_expression()
        self.expect(TokenType.SEPARATOR, ")")
        self.expect(TokenType.END_STATEMENT, "thanks~")
        return f"{print_type.capitalize()}({expression})"

    # Parse an if-else statement
    # Using grammar rules: <IF> ::= Check (<CONDITION>) { <STATEMENT_LIST> } [otherwise { <STATEMENT_LIST> }]
    def parse_if(self):
        self.expect(TokenType.KEYWORD, "Check")
        self.expect(TokenType.SEPARATOR, "(")
        condition = self.parse_expression()
        self.expect(TokenType.SEPARATOR, ")")
        self.expect(TokenType.SEPARATOR, "{")
        if_body = self.parse_program_block()
        self.expect(TokenType.SEPARATOR, "}")

        else_body = None
        if self.current_token() and self.current_token().value == "otherwise":
            self.advance()  # Consume "otherwise"
            self.expect(TokenType.SEPARATOR, "{")
            else_body = self.parse_program_block()
            self.expect(TokenType.SEPARATOR, "}")

        return f"If({condition}) Then {if_body} Else {else_body}"

    # Parse a while loop
    # Using grammar rules: <WHILE> ::= During (<CONDITION>) { <STATEMENT_LIST> }
    def parse_while(self):
        self.expect(TokenType.KEYWORD, "During")
        self.expect(TokenType.SEPARATOR, "(")
        condition = self.parse_expression()
        self.expect(TokenType.SEPARATOR, ")")
        self.expect(TokenType.SEPARATOR, "{")
        body = self.parse_program_block()
        self.expect(TokenType.SEPARATOR, "}")
        return f"While({condition}) Do {body}"

    # Parse a for loop
    # Using grammar rules: <FOR> ::= Given <IDENTIFIER> in <EXPRESSION> { <STATEMENT_LIST> }
    def parse_for(self):
        self.expect(TokenType.KEYWORD, "Given")
        identifier = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.KEYWORD, "in")
        expression = self.parse_expression()
        self.expect(TokenType.SEPARATOR, "{")
        body = self.parse_program_block()
        self.expect(TokenType.SEPARATOR, "}")
        return f"ForEach({identifier.value} in {expression}) Do {body}"

    # Parse a block of statements
    # Using grammar rules: <STATEMENT_LIST> ::= <STATEMENT> <STATEMENT_LIST> | ε
    def parse_program_block(self):
        statements = []
        while self.current_token() and self.current_token().type != TokenType.SEPARATOR:
            statements.append(self.parse_statement())
        return statements

    # Parse an expression
    # Using grammar rules: <EXPRESSION> ::= <PRIMARY> <OPERATOR> <PRIMARY> | <PRIMARY>
    # e.g., 5 + 3, x * y, "Hello" + "World" for <PRIMARY> <OPERATOR> <PRIMARY>
    # e.g., 5, x, "Hello" for <PRIMARY>
    def parse_expression(self):
        left = self.parse_primary()  # Parse the left side of the expression

        # Parse any operators following the left side
        while self.current_token() and self.current_token().type == TokenType.OPERATOR:
            operator = self.current_token()
            self.advance()  # Move past the operator
            right = self.parse_primary()  # Parse the right side of the expression
            left = (
                f"({left} {operator.value} {right})"  # Combine into a binary expression
            )

        return left

    # Parse primary elements (literals, identifiers, and grouped expressions)
    # Using grammar rules: <PRIMARY> ::= <IDENTIFIER> | <LITERAL> | (<EXPRESSION>)
    def parse_primary(self):
        token = self.current_token()

        if token.type == TokenType.LITERAL:
            self.advance()
            return f"Literal({token.value})"
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return f"Identifier({token.value})"
        elif token.type == TokenType.SEPARATOR and token.value == "(":
            self.advance()  # Skip the opening parenthesis
            expr = self.parse_expression()  # Parse the inner expression
            self.expect(TokenType.SEPARATOR, ")")  # Expect a closing parenthesis
            return f"({expr})"  # Return the grouped expression
        else:
            raise SyntaxError(f"Expected expression, but got {token}")


# Example usage
if __name__ == "__main__":
    # Assuming `tokens` is the output from LexicalAnalyzer
    source_code = """
    pls score = 10 thanks~
    show("Hello from PoliteLang!") thanks~
    Check (score >= 5) {
        shout("High score!") thanks~
    } otherwise {
        whisper("Keep trying...") thanks~
    }
    """
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()

    # Display tokens (optional, for debugging purposes)
    print("Tokens generated by the lexical analyzer:")
    for token in tokens:
        print(token)
    print("\n--- Syntax Analysis ---\n")

    parser = Parser(tokens)

    try:
        ast = parser.parse_program()
        for statement in ast:
            print(statement)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
