# AI Unit Test Generator (CLI)

A secure, deterministic command-line developer tool that automatically generates high-quality Python unit tests for legacy code and undocumented functions.

Unlike standard AI chatbots, this application enforces strict output constraints to behave like a native Unix tool. It accepts a Python file containing a single function and outputs **only** valid, executable `unittest` code—no markdown, no commentary, and no explanations.

## 🚀 Features

* **Strict Tooling Persona:** Bypasses conversational AI fluff. Outputs raw, executable code ready to be piped into other files or CI/CD workflows.
* **Prompt Injection Defense:** Uses Python's built-in `tokenize` module to physically strip all comments from the source code before it reaches the LLM, neutralizing malicious prompt injection attempts.
* **Pre-Flight Validation:** Leverages the Abstract Syntax Tree (`ast`) to validate the presence of actual executable `FunctionDef` nodes, rejecting malformed text or empty scripts instantly.
* **Deterministic Generation:** Configured with a generation temperature of `0` to ensure highly predictable and stable test coverage.

## 🛠️ Prerequisites

* Python 3.9+
* Google GenAI SDK (`google-genai`)
* A valid Google Gemini API Key

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/ai-unit-test-generator.git
cd ai-unit-test-generator

```


2. **Install the required dependencies:**
```bash
pip install google-genai

```


3. **Set up your API Key:**
Export your Gemini API key as an environment variable so the script can access it securely.
```bash
export GEMINI_API_KEY="your_api_key_here"

```



## 💻 Usage

Run the tool directly from your terminal, passing the path to the Python file you want to test.

```bash
python main.py path/to/your_function.py

```

### Example

**Input File (`math_ops.py`):**

```python
def add(a, b):
    # This comment will be stripped for security
    return a + b

```

**Terminal Command:**

```bash
python main.py math_ops.py

```

**Standard Output:**

```python
import unittest

def add(a, b):
    return a + b

class TestAddFunction(unittest.TestCase):
    def test_add_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)

    def test_add_mixed_numbers(self):
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()

```

## 🛡️ Security & Scope Enforcement

This tool is strictly scoped to generating tests for functions. It will return a standard error (`Error: This tool only generates unit tests for functions.`) if:

* The input file does not exist.
* The input file contains no valid Python functions.
* The code results in a `SyntaxError` during the AST parsing phase.
