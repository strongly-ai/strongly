# strongly

## Description

strongly is a powerful and user-friendly Python client for interacting with the Strongly.AI's API. This package simplifies the process of authentication, session management, and making API calls, allowing you to focus on utilizing the data and functionality provided by our service.


## Key Features

- **Automatic Authentication**: Handles API key authentication and session token management behind the scenes.
- **Session Persistence**: Maintains and renews sessions automatically, reducing unnecessary authentication calls.
- **Environment-based Configuration**: Easily configure API host and key using environment variables.
- **Intuitive Interface**: Provides a clean, Pythonic interface for all API endpoints.
- **Error Handling**: Custom exceptions for clearer error management.
- **Flexible**: Supports all API methods with a consistent interface.


## Use Cases

- Retrieve data from Strongly.AI with minimal setup.
- Integrate Strongly.AI functionality into your Python applications, scripts, or data pipelines.
- Automate tasks and workflows that interact with Strongly.AI.
- Build custom tools and dashboards on top of Strongly.AI data.

Whether you're a data scientist, software developer, or automation engineer, strongly provides a seamless way to leverage the power of Strongly.AI in your Python projects.


## Install instructions

To use this package, users need to:

Install strongly and its dependencies:

```bash
pip install strongly
```

Create a .env file in their project directory with their API host and key:

```text
API_HOST=https://your-api-host.com
API_KEY=their-api-key-here
```

API Keys are created in the Strongly.AI application.


## Usage

The following API logic applies to V1 of the RestAPI.

### Fetching Models

To fetch models available to account from the Strongly API:

```python
from strongly import APIClient

client = APIClient()

try:
    models_data = client.get_models()
    print("Models:", models_data['models'])
    print("User ID:", models_data['userId'])
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Fetching Applied Filters

To fetch the applied filters from the Strongly API:

```python
from strongly import APIClient

client = APIClient()

try:
    filters_data = client.get_applied_filters()
    print("Applied Filters:", filters_data['filters'])
    print("User ID:", filters_data['userId'])
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Filtering Text

To filter text using applicable filters:

```python
from strongly import APIClient

client = APIClient()

try:
    text_to_filter = "This is a confidential message containing a sensitive email: info@strongly.ai."
    result = client.filter_text(text_to_filter)

    print("Filtered Text:", result['filteredText'])
    print("Filter Counts:", result['filterCounts'])
    print("Hash Map:", result['hashMap'])
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Submitting a Prompt to Selected LLM

To submit a prompt to the selected large language model:

```python
from strongly import APIClient

client = APIClient()

try:
    session = {
        'sessionId': 'your-session-id',
        'sessionName': 'Your Session Name'
    }
    message = "What is the capital of France?"
    model = "gpt-3.5-turbo"

    result = client.submit_prompt(session, message, model)

    # The structure of the result may vary depending on the API response
    print("LLM Response:", result)

except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Checking Token Usage

To check the token usage for the current user:

```python
from strongly import APIClient

client = APIClient()

try:
    token_usage = client.check_token_usage()
    print("Token Usage Information:")
    print(f"Is Over Limit: {token_usage['isOverLimit']}")
    print(f"Is Restricted: {token_usage['isRestricted']}")
    print(f"User Token Usage: {token_usage['userTokenUsage']}")
    print(f"Plan Token Limit: {token_usage['planTokenLimit']}")
    print(f"Company Tokens Available: {token_usage['companyTokensAvailable']}")
    print(f"Purchased Tokens: {token_usage['purchasedTokens']}")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Creating a New Chat Session

To create a new chat session using the Strongly API:

```python
from strongly import APIClient

client = APIClient()

try:
    session_data = client.create_session("My New Chat Session")
    print("Session created successfully!")
    print("Session ID:", session_data['sessionId'])
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Deleting An Existing Session

To delete an existing session using the Strongly API:

```python
from strongly import APIClient

client = APIClient()

try:
    session_id = "existing-session-id"  # Replace with your actual session ID

    # Delete chat session created
    session_data = client.delete_session(session_id)
    print("Session deleted successfully!")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Renaming an Existing Chat Session

To rename an existing chat session using the Strongly API:

```python
from strongly import APIClient

client = APIClient()

try:
    session_id = "existing-session-id"  # Replace with your actual session ID
    new_name = "My Renamed Chat Session"

    result = client.rename_session(session_id, new_name)
    print("Session renamed successfully!")
    print("Message:", result['message'])
except Exception as e:
    print(f"An error occurred: {str(e)}")
```


## Testing

We strive to maintain high code quality and reliability in this package. To this end, we've included a comprehensive test suite. Here's how you can run the tests and contribute to maintaining the package's quality.

### Prerequisites

Before running the tests, make sure you have the required testing dependencies installed. You can install them using pip:

```bash
pip install pytest pytest-cov
```

### Running the Tests

To run the entire test suite, follow these steps:

Open a terminal or command prompt.
Navigate to the root directory of the package.
Run the following command:

```bash
pytest
```

This command will discover and run all the tests in the tests/ directory.

### Understanding Test Output

The test output will show you:

* Which tests passed (marked with . or PASSED)
* Which tests failed (marked with F or FAILED)
* The overall test summary
* Code coverage report

### Running Specific Tests

If you want to run a specific test file or test function, you can do so by specifying the path:

```bash
# Run tests in a specific file
pytest tests/strongly.py

# Run a specific test function
pytest tests/strongly.py::test_authenticate_success
```

### Code Coverage

Our pytest.ini file is configured to run coverage reports automatically. After running the tests, you'll see a coverage report in the console output. For a more detailed report, you can run:

```bash
pytest --cov-report=html
```

This will generate an HTML coverage report in the htmlcov/ directory. Open htmlcov/index.html in a web browser to view it.

### Continuous Integration

We use GitHub Actions for continuous integration. Every pull request is automatically tested to ensure that new changes don't break existing functionality.

### Contributing to Tests

If you're adding new features or fixing bugs, please consider adding appropriate tests. This helps maintain the package's reliability and makes it easier for others to understand and verify your changes.

If you have any questions about testing or need help interpreting test results, please don't hesitate to reach out to our support team.


## Need Help? We're Here for You!

We're thrilled you're using our package and want to ensure you have the best experience possible. If you have any questions, run into any issues, or just want to share your feedback, we'd love to hear from you!

📧 **Contact us at**: [info@strongly.ai](mailto:info@strongly.ai)

Whether you're a coding wizard or just getting started, our team is always happy to assist. Don't hesitate to reach out – your input helps us improve and grow!

Thank you for being part of our community. We truly appreciate your support and look forward to hearing from you!

Happy coding! 🚀✨
