# CPT316-G29-Assignment-1

Code Explanation (Jacky can see here)

1. Define enum type in our code.

        class TokenType(Enum):
           KEYWORD = "KEYWORD"
           IDENTIFIER = "IDENTIFIER"
           INTEGER_LITERAL = "INTEGER_LITERAL"
           FLOAT_LITERAL = "FLOAT_LITERAL"
           OPERATOR = "OPERATOR"       # Include arithmetic & relational
           ASSIGNMENT = "ASSIGNMENT"
           SEPARATOR = "SEPARATOR"     # {}, [], (), ;, :, ","
           PUNCTUATION = "PUNCTUATION" # \", \', !
           UNKNOWN = "UNKNOWN"         # @, $, ~, `
           ILLEGAL_IDENTIFIER = "ILLEGAL_IDENTIFIER"
   

3. Initialize variable to store enum type & actual value. Will be printed in final output
   
       class Token:
           def __init__(self, type: TokenType, value: str):
               self.type = type     # Store enum type
               self.value = value   # Store actual value
           def __str__(self):
               return f"Type: {self.type.value}, Value: {self.value}"  # Printed in the output
    

4. Lexical analysis starts here.

        Parts in this section:
        (a) Define rules to check if character is an alphabet, integer or alphanumerical
        (b) Traverse through the input and separate character into individual tokens
        

   Code

        // Class that implement lexical analyzer
        class LexicalAnalyzer:
            def __init__(self, source: str):
                self.input = source   # Self.input is a string, it stores the users input here (source code)
                self.position = 0     # Functions like index/pointer. Data type is int
                                      # Keep track of analyzer current position when analyzing the input. 
                self.keyword = {"int", "float", "bool", "print", "if", "else", "return", "while"}
                              # Set that stores keywords.
                              # Later used to identify if input is a keyword

   Code (Part a) 

           # Python has a library which detect alphabets, numerics & alphanumeric
           # Function to check if character is alphabetic
            def is_alpha(self, char: str) -> bool:   
                return char.isalpha()                
    
          # Function to check if character is digit
            def is_digit(self, char:str) -> bool:
                return char.isdigit()                
    
          # Function to check if character is alphanumeric
            def is_alphanumeric(self, char: str) -> bool:
                return char.isalnum()                

   Code (Part b)

          # Function to tokenize the input string
            def tokenize(self) -> List[Token]:  # Tokenize Function is called in main function 
                                              # It returns a list of token in the array
                tokens = []                   # Initialize an empty list to store tokens

        while self.position < len(self.input):  # While current position < length (source code)
            current_char = self.input[self.position] # Current character = string[0]

           `# Skip whitespace
            if current_char.isspace():
                self.position += 1   
                continue
   
   Code (Part b) - Identifying Keyword, Identifier, Float_Literal, Integer_literal
   
            # Identify keywords or identifiers
            if current_char.isalpha():
                start = self.position

                # Ensure checking doesn't go out of bounds && check for alphanumeric
                while self.position < len(self.input) and self.input[self.position].isalnum():
                    self.position += 1        
                word = self.input[start:self.position] # Extracts the substring from start to the current self.position
                                                       # Contains all the consecutive alphanumeric characters found

                if word in self.keyword:
                    tokens.append(Token(TokenType.KEYWORD, word))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word))
            
            # Identify integers or floats
            elif current_char.isdigit(): 
                start = self.position
                has_decimal = False
           # Ensure checking doesn't go out of bounds && (if input is integer or floating)
                while self.position < len(self.input) and (self.input[self.position].isdigit() or self.input[self.position] == '.'): 
                   #If decimal is encounted, enter the if statement. (Has 2 cases)
                    if self.input[self.position] == '.': 
                        if has_decimal:    # Case 1 - True, if decimal has encountered in input string before, then break 
                            break
                        has_decimal = True # Case 2 - False, decimal has not been encountered in input string before. So set has_decimal to True
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

   Code (Part b) - identifying operators, separator, punctuation & unknown char

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
