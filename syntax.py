from typing import List, Union
from lexical import Token, TokenType, LexicalAnalyzer
from PrettyPrint import PrettyPrintTree

# Assuming Token and TokenType are already defined, as in your lexical analysis


class SyntaxError(Exception):
    pass


# AST Node classes
class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    # def __repr__(self):
    #     return f"{self.type}({self.value}) -> {self.children}"

    # def __repr__(self, level=0):
    #     # This will return a string with indentation for hierarchical tree structure
    #     ret = "\t" * level + f"{self.type}({self.value if self.value else ''})\n"
    #     for child in self.children:
    #         ret += child.__repr__(level + 1)
    #     return ret

    def to_tree(self, level=0):
        # Create a hierarchical tree-like string representation
        ret = "\t" * level + f"{self.type}({self.value if self.value else ''})\n"
        for child in self.children:
            if isinstance(child, ASTNode):  # Ensure child is an ASTNode
                ret += child.to_tree(level + 1)
            elif isinstance(child, list):  # Handle lists of ASTNodes
                for sub_child in child:
                    ret += sub_child.to_tree(level + 1)
            else:
                raise TypeError("Invalid child type in ASTNode")
        return ret

    def __repr__(self):
        # Keep __repr__ simple for debugging purposes
        return f"{self.type}({self.value})"


class AssignmentNode(ASTNode):
    def __init__(self, identifier, expression):
        super().__init__("Assignment")
        self.add_child(ASTNode("Identifier", identifier))
        self.add_child(expression)


class PrintNode(ASTNode):
    def __init__(self, print_type, expression):
        super().__init__(f"{print_type.capitalize()}Print")
        self.add_child(expression)


class IfNode(ASTNode):
    def __init__(self, condition, if_body, else_body=None):
        super().__init__("If")
        self.add_child(condition)
        self.add_child(if_body)
        if else_body:
            self.add_child(else_body)


class WhileNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__("While")
        self.add_child(condition)
        self.add_child(body)


class ForNode(ASTNode):
    def __init__(self, identifier, expression, body):
        super().__init__("ForEach")
        self.add_child(ASTNode("Identifier", identifier))
        self.add_child(expression)
        self.add_child(body)


class BinaryOperationNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__("BinaryOperation", operator)
        self.add_child(left)
        self.add_child(right)


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0

    # def display_ast(self, ast):
    # print("Abstract Syntax Tree (AST):")
    # for statement in ast:
    # print(
    # statement.to_tree()
    # )  # Each statement is printed with tree-like structure from __repr__

    def display_ast(self, ast):
        print("Abstract Syntax Tree (AST):")
        for statement in ast:
            print(statement.to_tree())

    # def visualize_ast(self, ast_root):
    #     """
    #     Visualizes the AST using PrettyPrintTree.
    #     """
    #     # Create a PrettyPrintTree object
    #     pt = PrettyPrintTree(
    #         lambda node: node.children,  # Function to get child nodes
    #         lambda node: f"{node.type}\n{node.value if node.value else ''}",  # Function to get node label
    #     )
    #     pt(ast_root)  # Print the tree to the console

    def visualize_ast(self, ast_statements):
        # Create a dummy root node to hold the entire program
        program_root = ASTNode("Program")

        # Add each top-level statement as a child of the root
        for statement in ast_statements:
            program_root.add_child(statement)

        # Visualize using PrettyPrintTree
        pt = PrettyPrintTree(
            lambda node: node.children,  # Function to get child nodes
            lambda node: f"{node.type}\n{node.value if node.value else ''}",  # Function to get node label
        )
        pt(program_root)  # Print the full program tree

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
        # return f"Assignment({identifier.value} = {expression})"   # print the assignment statement for now
        return AssignmentNode(identifier, expression)

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
        # return f"{print_type.capitalize()}({expression})"  # Return the print statement for now
        return PrintNode(print_type, expression)

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

        # return f"If({condition}) Then {if_body} Else {else_body}"   # Return the if-else statement for now
        return IfNode(condition, if_body, else_body)

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
        # return f"While({condition}) Do {body}"      # Return the while loop statement for now
        return WhileNode(condition, body)

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
        # return f"ForEach({identifier.value} in {expression}) Do {body}" # Return the for loop statement for now
        return ForNode(identifier.value, expression, body)
        # return ForNode(identifier, expression, body)

    # Parse a block of statements
    # Using grammar rules: <STATEMENT_LIST> ::= <STATEMENT> <STATEMENT_LIST> | ε
    def parse_program_block(self):

        # statements = []
        # while self.current_token() and self.current_token().type != TokenType.SEPARATOR:
        #     statements.append(self.parse_statement())
        # return statements
        block_node = ASTNode("Block")  # Create a node for the block
        while self.current_token() and self.current_token().type != TokenType.SEPARATOR:
            block_node.add_child(self.parse_statement())
        return block_node

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
                # f"({left} {operator.value} {right})"  # Combine into a binary expression for now
                BinaryOperationNode(operator.value, left, right)
            )

        return left

    # Parse primary elements (literals, identifiers, and grouped expressions)
    # Using grammar rules: <PRIMARY> ::= <IDENTIFIER> | <LITERAL> | (<EXPRESSION>)
    def parse_primary(self):
        token = self.current_token()

        if token.type == TokenType.LITERAL:
            self.advance()
            # return f"Literal({token.value})"    # Return the literal value for now
            return ASTNode("Literal", token.value)
        elif token.type == TokenType.IDENTIFIER:
            self.advance()
            # return f"Identifier({token.value})"  # Return the identifier for now
            return ASTNode("Identifier", token.value)
        elif token.type == TokenType.SEPARATOR and token.value == "(":
            self.advance()  # Skip the opening parenthesis
            expr = self.parse_expression()  # Parse the inner expression
            self.expect(TokenType.SEPARATOR, ")")  # Expect a closing parenthesis
            # return f"({expr})"  # Return the grouped expression for now
            return expr
        else:
            raise SyntaxError(f"Expected expression, but got {token}")
