# PoliteLang

PoliteLang is a friendly and expressive programming language that uses polite syntax and conversational keywords to make coding both fun and accessible. Below is a quick overview of its unique syntax, keywords, and language rules.

## Language Specification

### 1. Output Commands

- **`show`**: Prints text as-is.

  ```plaintext
  show("Hello from PoliteLang!");
  ```

  **Output: Hello from PoliteLang!**

- **`whisper`**: Prints text in lowercase.

  ```plaintext
  whisper("This is a quiet message.");
  ```

  **Output: this is a quiet message.**

- **`shout`**: Prints text in uppercase.

  ```plaintext
  shout("congratulations!");
  ```

  **Output: this is a quiet message.**

### 2. Assignments

- **`show`**: Prints text as-is.

  ```plaintext
  show("Hello from PoliteLang!");
  ```

  **Output: Hello from PoliteLang!**

### 2. Assignments

- Use **`pls`** to start an assignment and **`thanks~`** to end the line.

  ```plaintext
  pls score = 10 thanks~
  pls name = "Polite Programmer" thanks~
  ```

  These lines assign the value `10` to `score` and `"Polite Programmer"` to `name`.

### 3. Booleans

- **`yep`** and **`nah`** for `true` and `false`.

  ```plaintext
  pls isComplete = nah thanks;
  pls isWinner = yep thanks;
  ```

  **Effect**: These lines set `isComplete` to `false` (nah) and `isWinner` to `true` (yep).

### 4. Control Flow

- **`Check`**: For `if` statements, with **`otherwise`** as `else`.

  ```plaintext
  Check (score > 10) {
      shout("High score!");
  } otherwise {
      whisper("Keep trying...");
  }
  ```

- **`Given`**: For `for ` loops.

  ```plaintext
  Given (pls i = 0 thanks; i < 3; pls i = i + 1 thanks) {
    show("Loop iteration:", i);
  }
  ```

### 5. Comments

- Use **`:)`** for single-line comments.

  ```plaintext
  :) This is a friendly comment!
  ```
