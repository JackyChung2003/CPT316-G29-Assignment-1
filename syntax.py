from enum import Enum
from typing import List
from lexical import TokenType, Token, LexicalAnalyzer


# AST Node Types
class ASTNodeType(Enum):
    ASSIGNMENT = "ASSIGNMENT"
    EXPRESSION = "EXPRESSION"
    CONDITIONAL = "CONDITIONAL"
    LOOP = "LOOP"
    PRINT = "PRINT"
    BINARY_OP = "BINARY_OP"
    LITERAL = "LITERAL"
    IDENTIFIER = "IDENTIFIER"


# AST Node Class
class ASTNode:
    def __init__(self, type_: ASTNodeType, value=None):
        self.type = type_
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"{self.type}({self.value}) -> {self.children}"


# Exception for Syntax Errors
class SyntaxError(Exception):
    pass


# Parser Class
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    def current_token(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def advance(self):
        self.position += 1

    def expect(self, type_: TokenType, value=None):
        token = self.current_token()
        if token and token.type == type_ and (value is None or token.value == value):
            self.advance()
            return token
        raise SyntaxError(f"Expected {type_} with value {value}, but got {token}")

    # Parse an assignment statement
    def parse_assignment(self):
        node = ASTNode(ASTNodeType.ASSIGNMENT)
        identifier = self.expect(TokenType.IDENTIFIER)
        node.add_child(ASTNode(ASTNodeType.IDENTIFIER, identifier.value))
        self.expect(TokenType.ASSIGNMENT, "=")
        node.add_child(self.parse_expression())
        self.expect(TokenType.SEPARATOR, ";")
        return node

    # Parse expressions (handles basic arithmetic)
    def parse_expression(self):
        left = self.parse_term()
        while self.current_token() and self.current_token().type == TokenType.OPERATOR:
            operator = self.current_token()
            self.advance()
            right = self.parse_term()
            op_node = ASTNode(ASTNodeType.BINARY_OP, operator.value)
            op_node.add_child(left)
            op_node.add_child(right)
            left = op_node
        return left

    def parse_term(self):
        token = self.current_token()
        if (
            token.type == TokenType.INTEGER_LITERAL
            or token.type == TokenType.FLOAT_LITERAL
        ):
            self.advance()
            return ASTNode(ASTNodeType.LITERAL, token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            return ASTNode(ASTNodeType.IDENTIFIER, token.value)
        elif token.type == TokenType.SEPARATOR and token.value == "(":
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.SEPARATOR, ")")
            return expr
        raise SyntaxError(f"Unexpected token {token}")

    # Parse an if-else conditional statement
    def parse_conditional(self):
        node = ASTNode(ASTNodeType.CONDITIONAL)
        self.expect(TokenType.KEYWORD, "if")
        self.expect(TokenType.SEPARATOR, "(")
        node.add_child(self.parse_expression())
        self.expect(TokenType.SEPARATOR, ")")
        self.expect(TokenType.SEPARATOR, "{")
        node.add_child(self.parse_statement())
        self.expect(TokenType.SEPARATOR, "}")
        if (
            self.current_token()
            and self.current_token().type == TokenType.KEYWORD
            and self.current_token().value == "else"
        ):
            self.advance()
            self.expect(TokenType.SEPARATOR, "{")
            node.add_child(self.parse_statement())
            self.expect(TokenType.SEPARATOR, "}")
        return node

    # Parse a while loop statement
    def parse_while(self):
        node = ASTNode(ASTNodeType.LOOP)
        self.expect(TokenType.KEYWORD, "while")
        self.expect(TokenType.SEPARATOR, "(")
        node.add_child(self.parse_expression())
        self.expect(TokenType.SEPARATOR, ")")
        self.expect(TokenType.SEPARATOR, "{")
        node.add_child(self.parse_statement())
        self.expect(TokenType.SEPARATOR, "}")
        return node

    # Parse a print statement
    def parse_print(self):
        node = ASTNode(ASTNodeType.PRINT)
        self.expect(TokenType.KEYWORD, "print")
        self.expect(TokenType.SEPARATOR, "(")
        node.add_child(self.parse_expression())
        self.expect(TokenType.SEPARATOR, ")")
        self.expect(TokenType.SEPARATOR, ";")
        return node

    # Function to parse a declaration with type (like 'int x = 5;')
    def parse_declaration(self):
        type_token = self.expect(TokenType.KEYWORD)
        if type_token.value not in {"int", "float"}:
            raise SyntaxError(f"Unexpected type {type_token.value}")

        identifier = self.expect(TokenType.IDENTIFIER)
        node = ASTNode(ASTNodeType.ASSIGNMENT, f"{type_token.value} {identifier.value}")
        self.expect(TokenType.ASSIGNMENT, "=")
        node.add_child(self.parse_expression())
        self.expect(TokenType.SEPARATOR, ";")
        return node

    # Parse a statement
    def parse_statement(self):
        token = self.current_token()
        if token.type == TokenType.KEYWORD and token.value in {"int", "float"}:
            return self.parse_declaration()
        elif token.type == TokenType.IDENTIFIER:
            return self.parse_assignment()
        elif token.type == TokenType.KEYWORD and token.value == "if":
            return self.parse_conditional()
        elif token.type == TokenType.KEYWORD and token.value == "while":
            return self.parse_while()
        elif token.type == TokenType.KEYWORD and token.value == "print":
            return self.parse_print()
        raise SyntaxError(f"Unexpected statement {token}")

    # Main parse function
    def parse(self):
        statements = []
        while self.current_token() is not None:
            statements.append(self.parse_statement())
        return statements


# Example usage
if __name__ == "__main__":
    source_code = "int x = 5; if (x > 0) { print(x); }"
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)

    try:
        ast = parser.parse()
        print("Abstract Syntax Tree (AST):")
        for statement in ast:
            print(statement)
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
