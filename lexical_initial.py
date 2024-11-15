import re
from enum import Enum
from typing import List

# Enum class to define different types of tokens
class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER_LITERAL = "INTEGER_LITERAL"
    FLOAT_LITERAL = "FLOAT_LITERAL"
    OPERATOR = "OPERATOR"       # Include arithmetic & relational
    ASSIGNMENT = "ASSIGNMENT"
    SEPARATOR = "SEPARATOR"     #{}, [], (), ;, :, ","
    PUNCTUATION = "PUNCTUATION" # \", \', !
    UNKNOWN = "UNKNOWN"         # @, $, ~, `
    ILLEGAL_IDENTIFIER = "ILLEGAL_IDENTIFIER"

# Class to represent a token with type and value
class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Type: {self.type.value}, Value: {self.value}"
    
# Class that implement lexical analyzer
class LexicalAnalyzer:
    def __init__(self, source: str):
        self.input = source
        self.position = 0
        self.keyword = {"int", "float", "bool", "print", "if", "else", "return", "while"}

    # Function to check if character is alphabetic
    def is_alpha(self, char: str) -> bool:
        return char.isalpha()
    
    # Function to check if character is digit
    def is_digit(self, char:str) -> bool:
        return char.isdigit()
    
    # Function to check if character is alphanumeric
    def is_alphanumeric(self, char: str) -> bool:
        return char.isalnum()

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
                while self.position < len(self.input) and self.input[self.position].isalnum():
                    self.position += 1
                word = self.input[start:self.position]

                if word in self.keyword:
                    tokens.append(Token(TokenType.KEYWORD, word))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word))

            # Identify integers or floats
            elif current_char.isdigit():
                start = self.position
                has_decimal = False
                while self.position < len(self.input) and (self.input[self.position].isdigit() or self.input[self.position] == '.'):
                    if self.input[self.position] == '.':
                        if has_decimal:
                            break
                        has_decimal = True
                    self.position += 1
                number = self.input[start:self.position]

                # If the number is followed by an alphabetic character, it is an illegal identifier
                if self.position < len(self.input) and self.input[self.position].isalpha():
                    illegal_identifier = number
                    while self.position < len(self.input) and self.input[self.position].isalnum():
                        illegal_identifier += self.input[self.position]
                        self.position += 1

                    tokens.append(Token(TokenType.ILLEGAL_IDENTIFIER, illegal_identifier))
                    print(f"Error: Illegal identifier '{illegal_identifier}' - identifiers cannot start with a digit.")
                    
                else:
                    # Otherwise, it's a valid integer or float literal
                    if '.' in number:
                        tokens.append(Token(TokenType.FLOAT_LITERAL, number))
                    else:
                        tokens.append(Token(TokenType.INTEGER_LITERAL, number))

            # Identify operators
            elif current_char in "+=*/<>":
                tokens.append(Token(TokenType.OPERATOR, current_char))
                self.position += 1

            # Identify separator
            elif current_char in "();{}":
                tokens.append(Token(TokenType.SEPARATOR, current_char))
                self.position += 1

            # Identify punctuation
            elif current_char in "!\"\'":
                tokens.append(Token(TokenType.PUNCTUATION, current_char))
                self.position += 1

            #Handle unknown character
            else:
                tokens.append(Token(TokenType.UNKNOWN, current_char))
                self.position += 1

        return tokens

# Function print all tokens
def print_tokens(tokens: List[Token]):
    for token in tokens:
        print(token)

# Rule 1: Check for matching {}, [], ()
def check_matching_bracket(code):
    bracket_pairs = {'(':')', '{':'}', '[':']'}
    stack = []

    for char in code:
        if char in bracket_pairs:   #Append open braces here
            stack.append(char)
        elif char in bracket_pairs.values():
            # if stack empty || Pop element not same as input
            if not stack or bracket_pairs[stack.pop()] != char:   
                print("Rule Violation #1: Code is missing a bracket, parenthesis or curly braces")
                return False

    #If stack has element, means code is imbalanced as there is odd bracket without its matching pair
    if stack:   
        print("Rule Violation #1: Code is missing a bracket, parenthesis or curly braces")
        return False

    return True

#Rule 2: Missing semicolon before closing bracket
def check_semicolon(code):
    for i in range(1, len(code)):
        if code[i] == '}':
            if code[i-1] != ';':
                print("Rule Violation 2: Missing semicolon before closing curly braces")
                return False
    return True


# Main code
if __name__ == "__main__":
    
    while True:
        source_code = "{ int 12variable <= 3.14; #1boiboiboi int x = 5 print(x + \"is a variable\");}"
        print("\nSource code:", source_code)

        if check_matching_bracket(source_code) and check_semicolon(source_code):
            try:
                # Create a LexicalAnalyzer object
                lexer = LexicalAnalyzer(source_code)

                # Tokenize the source code
                tokens = lexer.tokenize()

                # Print the original source code
                print("\nTokens generated by Lexical Analyzer:")
                print_tokens(tokens)
                print("\n")
                break #Print token list once
    
            except Exception as e:
                print("")

        break   # Print error message once     
