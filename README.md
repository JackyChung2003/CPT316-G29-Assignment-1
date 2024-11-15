# CPT316-G29-Assignment-1

##### Code Explanation

#### 1. The TokenType enum defines various types of tokens in PoliteLang.

    class TokenType(Enum):
        KEYWORD = "KEYWORD"
        IDENTIFIER = "IDENTIFIER"
        INTEGER_LITERAL = "INTEGER_LITERAL"
        FLOAT_LITERAL = "FLOAT_LITERAL"
        OPERATOR = "OPERATOR"
        ASSIGNMENT = "ASSIGNMENT"
        SEPARATOR = "SEPARATOR"
        PUNCTUATION = "PUNCTUATION"
        UNKNOWN = "UNKNOWN"
        ILLEGAL_IDENTIFIER = "ILLEGAL_IDENTIFIER"
        END_STATEMENT = "END_STATEMENT"

#### 2. Initialize variable to store enum type & actual value. Will be printed in final output

    class Token:
        def __init__(self, type: TokenType, value: str):
            self.type = type     # Store enum type
            self.value = value   # Store actual value
        def __str__(self):
            return f"Type: {self.type.value}, Value: {self.value}"  # Printed in the output

#### 3. Lexical analysis starts here.

    Parts in this section:
        (a) Define rules to check if character is an alphabet, integer or alphanumerical
        (b) Traverse through the input and separate character into individual tokens

##### Code Segment 1

##### - Initializing variable to store source code, current position and keyword

```plaintext
  // Class that implement lexical analyzer
  class LexicalAnalyzer:
      def __init__(self, source: str):
          self.input = source   # Self.input is a string, it stores the users input here (source code)
          self.position = 0     # Functions like index/pointer. Data type is int
                                # Keep track of analyzer current position when analyzing the input.
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
                        # Set that stores keywords.
                        # Later used to identify if input is a keyword
```

##### Code Segment 2

##### - Tokenization Process - The `tokenize` function traverses each character of `source`, categorizing and appending tokens to the `tokens` list.

```plaintext
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
```

#### 4. Violation Rules to detect potential errors in code

##### Rule 1: Violation Rule 1: Matching Brackets {}, [], ()

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

##### Rule 2: Missing semicolon before closing bracket

        def check_semicolon(code):
            for i in range(1, len(code)):
                if code[i] == '}':
                    if code[i-1] != ';':
                        print("Rule Violation 2: Missing semicolon before closing curly braces")
                        return False
            return True

### 5. Main Code

        if __name__ == "__main__":

            while True:
                source_code = "{ int 12variable <= 3.14; #1boiboiboi int x = 5 print(x + \"is a         variable\");}"
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

### 6. Language Specification

#### Syntax and Grammar Rules:

        (i) Keywords: Defined any reserved words in MiniLang, cannot be used as identifiers
                Example: int, float, if, else, while, print, etc.
        (ii) Identifiers: In MiniLang, identifiers can start with alphabets and could include letters and numbers after that
                Example: Variable1, Boiboiboi123
        (iii) Literals: Specifiy the kinds of constant values allowed, such as integers and floats
                Example: 12, 3.142
        (iv) Operators: List of operators MiniLang supports
                Example: +, -, *, / (Arithmetic operators)
                Example: <=, >=, ==, != (Relational operators)
        (v) Separators and Punctuations: Symbols to organize the code.
                Example: {}, [], (), ; (Separators)
                Example: \", \', :, (Punctuations)

#### Semantics:

        (i) Meaning of statemens: Explain what each language construct is supposed to do
                Example1: int x = 5;
                Explanation: declare variable x as an integer and assign it to value 5
                Example2: if(x < 10) {print(x);}
                Explanation: if x is less than 10 is true, print value of x

        (ii) Variable Declaration and Assignment: Define the behavior of declaring and assigning variable
                Example: How does MiniLang hangle data types, can you assigned a float value to int variable

        (iii) Function or statement: Describe any build-in functions, like print.
                Print function output a variable or literal to the console
                Example: print(x); display the value of x
