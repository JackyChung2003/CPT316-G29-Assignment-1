import re
from enum import Enum
from typing import List


# Simplified token types for PoliteLang
class TokenType(Enum):
    KEYWORD = "KEYWORD"  # For all language keywords (e.g., show, whisper, pls, thanks~)
    IDENTIFIER = "IDENTIFIER"  # For variable names
    LITERAL = "LITERAL"  # For literals (strings, integers, floats, booleans)
    OPERATOR = "OPERATOR"  # For arithmetic and relational operators
    SEPARATOR = "SEPARATOR"  # For delimiters like (), {}, etc.
    END_STATEMENT = "END_STATEMENT"  # For statement terminators (thanks~)
    COMMENT = "COMMENT"  # For comments (start with ":)")
    UNKNOWN = "UNKNOWN"  # For unrecognized characters
    ILLEGAL_IDENTIFIER = "ILLEGAL_IDENTIFIER"  # For invalid identifiers


# Token class to store type and value of each token
class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type  # The type of the token
        self.value = value  # The actual string value of the token

    def __str__(self):
        return f"Type: {self.type.value}, Value: {self.value}"


# LexicalAnalyzer for PoliteLang
class LexicalAnalyzer:
    def __init__(self, source: str):
        self.source = source  # Source code input as a string
        self.position = 0  # Position tracker for character analysis

        # Define sets of keywords, operators, and separators
        self.KEYWORDS = {
            "show",
            "whisper",
            "shout",
            "pls",
            "thanks~",
            "yep",
            "nah",
            "Check",
            "otherwise",
            "During",
            "Given",
        }
        self.OPERATORS = {"+", "-", "*", "/", "<", ">", ">=", "<=", "==", "!=", "="}
        self.SEPARATORS = {"(", ")", "{", "}", "[", "]", ":", ","}

    # Tokenize the input string and return a list of tokens
    def tokenize(self) -> List[Token]:
        tokens = []

        while self.position < len(self.source):
            current_char = self.source[self.position]

            # Skip whitespace
            if current_char.isspace():
                self.position += 1
                continue

            # Check for comments starting with :)
            elif self.source.startswith(":)", self.position):
                self.skip_comment()
                continue

            # Identify string literals enclosed in double quotes
            elif current_char == '"':
                string_literal = (
                    self.read_string()
                )  # Capture entire string between quotes
                tokens.append(Token(TokenType.LITERAL, string_literal))

            # Check for end of statement "thanks~"
            elif self.source.startswith("thanks~", self.position):
                tokens.append(Token(TokenType.END_STATEMENT, "thanks~"))
                self.position += len("thanks~")

            # Check for multi-character operators (e.g., >=, <=, ==, !=)
            elif any(
                self.source.startswith(op, self.position)
                for op in self.OPERATORS
                if len(op) > 1
            ):
                for op in sorted(
                    self.OPERATORS, key=lambda x: -len(x)
                ):  # Sort operators by length descending
                    if self.source.startswith(op, self.position):
                        tokens.append(Token(TokenType.OPERATOR, op))
                        self.position += len(op)
                        break

            # Check for single-character operators
            elif current_char in self.OPERATORS:
                tokens.append(Token(TokenType.OPERATOR, current_char))
                self.position += 1

            # Check for separators
            elif current_char in self.SEPARATORS:
                tokens.append(Token(TokenType.SEPARATOR, current_char))
                self.position += 1

            # Check for keywords or identifiers
            elif current_char.isalpha() or current_char == "_":
                identifier = self.read_identifier()
                if identifier in self.KEYWORDS:
                    tokens.append(Token(TokenType.KEYWORD, identifier))
                else:
                    tokens.append(self.validate_identifier(identifier))

            # Check for literals (numbers or strings)
            elif current_char.isdigit():
                number = self.read_number()
                if (
                    self.position < len(self.source)
                    and self.source[self.position].isalpha()
                ):
                    # Handle case like "1score" where a digit is followed by an alphabetic character
                    illegal_identifier = self.read_identifier()
                    print(
                        f"Error: Illegal identifier '{number + illegal_identifier}' - identifiers cannot start with a digit."
                    )
                    tokens.append(
                        Token(TokenType.ILLEGAL_IDENTIFIER, number + illegal_identifier)
                    )
                else:
                    tokens.append(Token(TokenType.LITERAL, number))

            # # Handle unknown characters
            # else:
            #     tokens.append(Token(TokenType.UNKNOWN, current_char))
            #     self.position += 1

            # Handle unknown characters
            else:
                print(
                    f"Error: Unrecognized symbol '{current_char}' at position {self.position}"
                )
                tokens.append(Token(TokenType.UNKNOWN, current_char))
                self.position += 1
        return tokens

    # Read an identifier (variable name) or keyword
    def read_identifier(self):
        start = self.position
        while self.position < len(self.source) and (
            self.source[self.position].isalnum() or self.source[self.position] == "_"
        ):
            self.position += 1
        return self.source[start : self.position]

    # Validate an identifier (checking if it starts with a digit)
    def validate_identifier(self, identifier: str) -> Token:
        if identifier[0].isdigit():
            print(
                f"Error: Illegal identifier '{identifier}' - identifiers cannot start with a digit."
            )
            return Token(TokenType.ILLEGAL_IDENTIFIER, identifier)
        return Token(TokenType.IDENTIFIER, identifier)

    # Read a number (integer or float)
    def read_number(self):
        start = self.position
        has_decimal = False
        while self.position < len(self.source) and (
            self.source[self.position].isdigit()
            or (self.source[self.position] == "." and not has_decimal)
        ):
            if self.source[self.position] == ".":
                has_decimal = True
            self.position += 1
        return self.source[start : self.position]

    # Read a string literal enclosed in double quotes
    def read_string(self):
        self.position += 1  # Skip the opening quote like ' or "
        start = self.position
        while self.position < len(self.source) and self.source[self.position] != '"':
            self.position += 1

        # Error handling for missing closing quote
        if self.position >= len(self.source) or self.source[self.position] != '"':
            print("Error: Unterminated string literal")  # Error message
            return self.source[start : self.position]  # Return partial string

        string_literal = self.source[start : self.position]
        self.position += 1  # Skip the closing quote
        return string_literal

    # Skip a comment line starting with :)
    def skip_comment(self):
        while self.position < len(self.source) and self.source[self.position] != "\n":
            self.position += 1
        self.position += 1  # Skip the newline character


# Example usage to test the lexical analyzer
if __name__ == "__main__":
    source_code = """
    :) This is a comment
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

    # Print each token generated by the lexical analyzer
    for token in tokens:
        print(token)
