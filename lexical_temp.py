import re
from enum import Enum
from typing import List


# Enum class to define different types of tokens
class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    OPERATOR = "OPERATOR"  # Include arithmetic & relational operators like +, -, *, /
    ASSIGNMENT = "ASSIGNMENT"  # Specifically for =
    SEPARATOR = "SEPARATOR"  # Symbols like {}, (), ;
    PUNCTUATION = "PUNCTUATION"  # Symbols like ", ', !
    UNKNOWN = "UNKNOWN"  # Unknown characters
    ILLEGAL_IDENTIFIER = "ILLEGAL_IDENTIFIER"


# Class to represent a token with type and value
class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Type: {self.type.value}, Value: {self.value}"


# Class that implements the lexical analyzer
class LexicalAnalyzer:
    def __init__(self, source: str):
        self.input = source
        self.position = 0
        self.keywords = {
            "int",
            "float",
            "bool",
            "print",
            "if",
            "else",
            "return",
            "while",
        }

    # Helper function to check if character is alphabetic
    def is_alpha(self, char: str) -> bool:
        return char.isalpha()

    # Helper function to check if character is a digit
    def is_digit(self, char: str) -> bool:
        return char.isdigit()

    # Function to tokenize the input string
    def tokenize(self) -> List[Token]:
        tokens = []

        while self.position < len(self.input):
            current_char = self.input[self.position]

            # Skip whitespace
            if current_char.isspace():
                self.position += 1
                continue

            # Identify keywords or identifiers
            if current_char.isalpha():
                start = self.position
                while (
                    self.position < len(self.input)
                    and self.input[self.position].isalnum()
                ):
                    self.position += 1
                word = self.input[start : self.position]
                if word in self.keywords:
                    tokens.append(Token(TokenType.KEYWORD, word))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word))

            # Identify integers or floats
            elif current_char.isdigit():
                start = self.position
                has_decimal = False
                while self.position < len(self.input) and (
                    self.input[self.position].isdigit()
                    or self.input[self.position] == "."
                ):
                    if self.input[self.position] == ".":
                        if has_decimal:
                            break
                        has_decimal = True
                    self.position += 1
                number = self.input[start : self.position]
                if (
                    self.position < len(self.input)
                    and self.input[self.position].isalpha()
                ):
                    illegal_identifier = number
                    while (
                        self.position < len(self.input)
                        and self.input[self.position].isalnum()
                    ):
                        illegal_identifier += self.input[self.position]
                        self.position += 1
                    tokens.append(
                        Token(TokenType.ILLEGAL_IDENTIFIER, illegal_identifier)
                    )
                    print(
                        f"Error: Illegal identifier '{illegal_identifier}' - identifiers cannot start with a digit."
                    )
                else:
                    if "." in number:
                        tokens.append(Token(TokenType.FLOAT_LITERAL, number))
                    else:
                        tokens.append(Token(TokenType.INTEGER_LITERAL, number))

            # Identify assignment operator
            elif current_char == "=":
                tokens.append(Token(TokenType.ASSIGNMENT, current_char))
                self.position += 1

            # Identify other operators
            elif current_char in "+-*/<>":
                tokens.append(Token(TokenType.OPERATOR, current_char))
                self.position += 1

            # Identify separators
            elif current_char in "();{}":
                tokens.append(Token(TokenType.SEPARATOR, current_char))
                self.position += 1

            # Identify punctuation
            elif current_char in "!\"'":
                tokens.append(Token(TokenType.PUNCTUATION, current_char))
                self.position += 1

            # Handle unknown characters
            else:
                tokens.append(Token(TokenType.UNKNOWN, current_char))
                self.position += 1

        return tokens


# Example usage
if __name__ == "__main__":
    source_code = "int x = 5; if (x > 0) { print(x); }"
    lexer = LexicalAnalyzer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
