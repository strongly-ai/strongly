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


## Usage

### Fetching Models

To fetch models available to account from the Strongly API:

```python
from py_strongly import APIClient

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
from py_strongly import APIClient

client = APIClient()

try:
    filters_data = client.get_applied_filters()
    print("Applied Filters:", filters_data['filters'])
    print("User ID:", filters_data['userId'])
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

### Apply Filters To Text

To Do

### Prompt Large Language Model

To Do

### Fetching Account Tokens

To Do

### Create Session

To Do

### Remove Session

To Do

### Update Session

To Do

### Archive Session

To Do


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
We use [CI service name, e.g., GitHub Actions] for continuous integration. Every pull request is automatically tested to ensure that new changes don't break existing functionality.

### Contributing to Tests
If you're adding new features or fixing bugs, please consider adding appropriate tests. This helps maintain the package's reliability and makes it easier for others to understand and verify your changes.

If you have any questions about testing or need help interpreting test results, please don't hesitate to reach out to our support team.




## Need Help? We're Here for You!

We're thrilled you're using our package and want to ensure you have the best experience possible. If you have any questions, run into any issues, or just want to share your feedback, we'd love to hear from you!

📧 **Contact us at**: [info@strongly.ai](mailto:info@strongly.ai)

Whether you're a coding wizard or just getting started, our team is always happy to assist. Don't hesitate to reach out – your input helps us improve and grow!

Thank you for being part of our community. We truly appreciate your support and look forward to hearing from you!

Happy coding! 🚀✨
