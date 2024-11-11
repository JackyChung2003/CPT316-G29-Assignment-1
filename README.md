# CPT316-G29-Assignment-1

Code Explanation (Jacky can see here)

1. Define enum type in our code.

        class TokenType(Enum):
           KEYWORD = "KEYWORD"
           IDENTIFIER = "IDENTIFIER"
           INTEGER_LITERAL = "INTEGER_LITERAL"
           FLOAT_LITERAL = "FLOAT_LITERAL"
           OPERATOR = "OPERATOR"       // Include arithmetic & relational
           ASSIGNMENT = "ASSIGNMENT"
           SEPARATOR = "SEPARATOR"     //{}, [], (), ;, :, ","
           PUNCTUATION = "PUNCTUATION" // \", \', !
           UNKNOWN = "UNKNOWN"         // @, $, ~, `
           ILLEGAL_IDENTIFIER = "ILLEGAL_IDENTIFIER"

2. Initialize token - enum type & actual value. Printed in final output
   
       class Token:
           def __init__(self, type: TokenType, value: str):
               self.type = type     // Store enum type
               self.value = value   // Store actual value
           def __str__(self):
               return f"Type: {self.type.value}, Value: {self.value}"  // Printed in the output  

4. Lexical analysis starts here! 

        Parts in this section:
        (a) Define rules to check if its an alphabet, integer or alphanumerical (Line 45 - 55)
        (b) Traverse through the input and separate character into individual tokens
        (c)  





        // Class that implement lexical analyzer
        class LexicalAnalyzer:
            def __init__(self, source: str):
                self.input = source   // Self.input is a string, it stores the users input here (source code)
                self.position = 0     // Functions like index/pointer. Data type is int
                                      // Keep track of analyzer current position when analyzing the input. 
                self.keyword = {"int", "float", "bool", "print", "if", "else", "return", "while"}
                              // Set that stores keywords.
                              // Later used to identify if input is a keyword

  // Function to check if character is alphabetic
    def is_alpha(self, char: str) -> bool:   // Returm True/False
        return char.isalpha()                // Python Library detects if its an alphabet
    
  // Function to check if character is digit
    def is_digit(self, char:str) -> bool:
        return char.isdigit()                // Python Library detects if its a number
    
  // Function to check if character is alphanumeric
    def is_alphanumeric(self, char: str) -> bool:
        return char.isalnum()                // Python Library detects if its an alpha + number

  // Function to tokenize the input string
    def tokenize(self) -> List[Token]:  // Tokenize Function is called in main function 
                                      // It returns a list of token in the array
        tokens = []                   // Initialize an empty list to store tokens

        while self.position < len(self.input):  // While current position < length (source code)
            current_char = self.input[self.position] // Current character = string[0]

            // Skip whitespace
            if current_char.isspace():
                self.position += 1    // Ignore whitespace, move to next character
                continue
            
            // Identify keywords or identifiers
            if current_char.isalpha():
                start = self.position  
                while self.position < len(self.input) and self.input[self.position].isalnum():
                    self.position += 1
                word = self.input[start:self.position]

                if word in self.keyword:
                    tokens.append(Token(TokenType.KEYWORD, word))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, word))
            
            // Identify integers or floats
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

                // If the number is followed by an alphabetic character, it is an illegal identifier
                if self.position < len(self.input) and self.input[self.position].isalpha():
                    illegal_identifier = number
                    while self.position < len(self.input) and self.input[self.position].isalnum():
                        illegal_identifier += self.input[self.position]
                        self.position += 1

                    tokens.append(Token(TokenType.ILLEGAL_IDENTIFIER, illegal_identifier))
                    print(f"Error: Illegal identifier '{illegal_identifier}' - identifiers cannot start with a digit.")
                    
                else:
                    // Otherwise, it's a valid integer or float literal
                    if '.' in number:
                        tokens.append(Token(TokenType.FLOAT_LITERAL, number))
                    else:
                        tokens.append(Token(TokenType.INTEGER_LITERAL, number))

