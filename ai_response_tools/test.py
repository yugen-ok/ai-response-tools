
from .core import *


def test_and_demo():
    """
    Demonstrates and tests the functionality of `query_lbgpt` and `response_parsing`.

    This function:
    - Explains how to set up the environment for using `query_lbgpt`.
    - Demonstrates how to use `query_lbgpt` to query a language model.
    - Demonstrates and explains how `response_parsing` converts JSON output into Python objects.
    - Combines the two functions in a real-world use case, where a query returns JSON output, and it's parsed.
    - Validates success of each step with a success message.
    """

    print("### AI Response Tools: Demonstration and Testing ###\n")

    # Setup instructions for query_lbgpt
    print("To use `query_lbgpt`, you must define the following environment variables:\n")
    print("  - AZURE_OPENAI_API_KEY: Your Azure OpenAI API key (if using Azure).")
    print("  - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI API endpoint (if using Azure).")
    print("  - OPENAI_API_KEY: Your OpenAI API key (if using OpenAI directly).\n")

    print("Example code to set environment variables (Linux/Mac):\n")
    print('export AZURE_OPENAI_API_KEY="your_api_key"')
    print('export AZURE_OPENAI_ENDPOINT="your_api_endpoint"')
    print('export OPENAI_API_KEY="your_openai_api_key"\n')

    print("Ensure these variables are set before running the following examples.\n")

    # Step 1: Demonstrate query_lbgpt
    print("### Step 1: Demonstrating `query_lbgpt` ###\n")
    print("Code example:")
    print("""
response = query_lbgpt(
    system_prompt="Summarize the following text:",
    user_prompts=["This is a test input to the system."],
    model="gpt-3.5-turbo",
    use_azure=False,  # Set to True if using Azure
    cache=cache
)
print(response)
    """)

    try:
        responses = query_lbgpt(
            system_prompt="Summarize the following text:",
            user_prompts=["This is a test input to the system."],
            model="gpt-3.5-turbo",
            use_azure=False,  # Change to True if using Azure
            cache=cache
        )
        print(f"Response from query_lbgpt: {responses}\n")
        print("✅ `query_lbgpt` test passed.\n")
    except Exception as e:
        print(f"❌ `query_lbgpt` test failed: {e}\n")
        return

    # Step 2: Demonstrate response_parsing
    print("### Step 2: Demonstrating `response_parsing` ###\n")
    print("The `response_parsing` function is used to convert a JSON string or model response into structured Python objects.")
    print("This is useful when working with complex outputs from a language model.\n")
    print("Code example:")
    print("""
example_response = \"\"\"
{
    "name": "John Doe",
    "age": 30,
    "hobbies": ["reading", "swimming", "programming"]
}
\"\"\"
parsed_response = response_parsing(example_response)
print(parsed_response)
    """)

    example_response = """
    {
        "name": "John Doe",
        "age": 30,
        "hobbies": ["reading", "swimming", "programming"]
    }
    """
    try:
        parsed_response = response_parsing(example_response)
        print("Parsed Python object:")
        print(parsed_response)
        print("\n✅ `response_parsing` test passed.\n")
    except Exception as e:
        print(f"❌ `response_parsing` test failed: {e}\n")
        return

    # Step 3: Combine query_lbgpt and response_parsing
    print("### Step 3: Using `query_lbgpt` and `response_parsing` Together ###\n")
    print("Code example:")
    print("""
# Query the model for a JSON response
response = query_lbgpt(
    system_prompt="Describe the following people as JSON that have the fields name, date of birth, and gender:",
    user_prompts=["Albert Einstein", "Ada Lovelace"],
    model="gpt-3.5-turbo",
    use_azure=False,  # Set to True if using Azure
    cache=cache
)

# Parse the JSON response
parsed_response = response_parsing(response[0])
print(parsed_response)
    """)

    try:
        query_prompt = "Describe the following people as JSON that have the fields name, date of birth, and gender:"
        user_queries = ["Donald Trump", "Ada Lovelace"]
        responses = query_lbgpt(
            system_prompt=query_prompt,
            user_prompts=user_queries,
            model="gpt-3.5-turbo",
            use_azure=False,  # Change to True if using Azure
            cache=cache
        )
        print("Raw response from the model:")
        print(responses[0])

        parsed_response = response_parsing(responses[0])
        print("\nParsed JSON object:")
        print(parsed_response)
        print("\n✅ Combined usage test passed.\n")
    except Exception as e:
        print(f"❌ Combined usage test failed: {e}\n")
        return

    print("### All Tests Passed Successfully! ###")
