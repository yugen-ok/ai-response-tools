
# AI Response Tools

**AI Response Tools** is a Python package designed to simplify querying OpenAI and Azure OpenAI language models and parsing their responses into structured Python objects. It provides a streamlined interface for generating responses and validating their structure using JSON schemas.

---

## **Features**

1. **Query OpenAI/Azure Models**:
   - Easily send queries to language models using the `query_lbgpt` function.
   - Supports text and image inputs.
   - Built-in caching with `diskcache` for efficient repeated queries.

2. **Parse JSON Responses**:
   - Use `response_parsing` to convert JSON strings into Python objects.
   - Supports schema validation with `jsonschema` to ensure the structure of the parsed data.

3. **Demonstration and Testing**:
   - Includes a `test_and_demo` function to showcase functionality, provide usage examples, and test the package.

---

## **Installation**

### Prerequisites
- Python 3.8 or later
- API keys for OpenAI or Azure OpenAI

### Remote Installation

   ```
   pip install git+https://github.com/yugen-ok/ai-response-tools.git 
   ```

### Local Installation
1. Clone the repository or download the package.
2. Install the package using pip:
   ```bash
   pip install .
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **Environment Setup**

To use the package, ensure the following environment variables are set:
- **For Azure OpenAI**:
  ```bash
  export AZURE_OPENAI_API_KEY="your_azure_api_key"
  export AZURE_OPENAI_ENDPOINT="your_azure_api_endpoint"
  ```
- **For OpenAI**:
  ```bash
  export OPENAI_API_KEY="your_openai_api_key"
  ```

---

## **Usage**

### 1. **Query the Language Model**
Use `query_lbgpt` to send queries to a language model:
```python
from ai_response_tools import query_lbgpt

response = query_lbgpt(
    system_prompt="Summarize the following text:",
    user_prompts=["This is a test input to the system."],
    model="gpt-3.5-turbo",
    use_azure=False,  # Set to True for Azure
    cache=None  # Optional cache object
)
print(response)
```

### 2. **Parse JSON Responses**
Use `response_parsing` to convert a JSON response into a Python object:
```python
from ai_response_tools import response_parsing

example_response = """
{
    "name": "John Doe",
    "age": 30,
    "hobbies": ["reading", "swimming", "programming"]
}
"""
parsed = response_parsing(example_response)
print(parsed)
```

### 3. **Combine Querying and Parsing**
Query the model for a structured JSON response and parse it:
```python
from ai_response_tools import query_lbgpt, response_parsing

# Query the model
response = query_lbgpt(
    system_prompt="Generate a JSON object describing a person:",
    user_prompts=["Include their name, age, and hobbies."],
    model="gpt-3.5-turbo",
    use_azure=False
)

# Parse the JSON response
parsed_response = response_parsing(response[0])
print(parsed_response)
```

---

## **Demonstration and Testing**

The package includes a `test_and_demo` function to:
- Explain how to use the package.
- Provide example code and run tests for both `query_lbgpt` and `response_parsing`.
- Combine both functions in a real-world use case.

### Running the Demo
```python
from ai_response_tools import test_and_demo

test_and_demo()
```

### What It Does
1. **Demonstrates `query_lbgpt`**:
   - Sends a sample query to the language model.
   - Prints the response.
   - Validates the function with a success message.

2. **Demonstrates `response_parsing`**:
   - Parses a static JSON string.
   - Validates the parsed object.
   - Prints the result with a success message.

3. **Combines Both Functions**:
   - Queries the model to generate a JSON object describing a person.
   - Parses the response and validates its structure.
   - Prints the parsed object with a success message.

---

## **Dependencies**
- `openai`: For OpenAI API access.
- `diskcache`: For caching queries.
- `chompjs`: For parsing JavaScript objects in JSON strings.
- `jsonschema`: For validating JSON structures.
- `lbgpt`: A wrapper for interacting with OpenAI and Azure models.

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

## **Troubleshooting**

### Windows: Chompjs Installation Error

If you encounter this error when installing the package:

```
Building wheel for chompjs (setup.py) ... error
error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"
```

This occurs because `chompjs` requires C++ compilation. You have two options to resolve this:

#### Option 1: Install Visual C++ Build Tools (Recommended)
1. Download Microsoft Visual C++ Build Tools from [https://visualstudio.microsoft.com/visual-cpp-build-tools/](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Run the installer.
3. Select **Desktop development with C++**.
4. Complete the installation.
5. Retry installing `chompjs`:
   ```bash
   pip install chompjs
   ```

#### Option 2: Use Alternative Packages
If you prefer to avoid C++ compilation, you can use alternative JSON parsing packages like:
- `hjson`
- `demjson3`

**Note:** Using alternative packages will require code modifications.

---

## **License**
This project is licensed under the MIT License.

---

## **Contributing**
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m "Add new feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Submit a pull request.

---

## **Support**
If you encounter any issues or have questions, feel free to open an issue or contact the maintainer.