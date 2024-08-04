import os
from dotenv import load_dotenv
import requests
from .exceptions import AuthenticationError, APIError

class APIClient:
    def __init__(self, env_file='.env', test_env=None):
        if test_env is None:
            load_dotenv(env_file)
            self.host = os.getenv('API_HOST')
            self.api_key = os.getenv('API_KEY')
        else:
            self.host = test_env.get('API_HOST')
            self.api_key = test_env.get('API_KEY')

        if not self.host or not self.api_key:
            raise ValueError("API_HOST and API_KEY must be set in the .env file or as environment variables")

        self.session = requests.Session()
        self._auth_token = None

    def authenticate(self):
        url = f"{self.host}/api/v1/authenticate"
        headers = {'X-API-Key': self.api_key}

        response = self.session.get(url, headers=headers)

        if response.status_code != 200:
            raise AuthenticationError(f"Authentication failed: {response.text}")

        data = response.json()
        self._auth_token = data.get('authToken')
        if not self._auth_token:
            raise AuthenticationError("No session token received from authentication endpoint")
        return self._auth_token

    @property
    def auth_token(self):
        if not self._auth_token:
            self.authenticate()
        return self._auth_token

    def call_api(self, method, endpoint, **kwargs):
        headers = kwargs.pop('headers', {})
        headers['X-API-Key'] = self.api_key
        headers['X-Auth-Token'] = self.auth_token

        url = f"{self.host}{endpoint}"
        response = self.session.request(method, url, headers=headers, **kwargs)

        if response.status_code == 401:  # Unauthorized, token might have expired
            self._auth_token = None  # Clear the token
            self.authenticate()  # Re-authenticate
            headers['X-Auth-Token'] = self.auth_token  # Update the token in headers
            response = self.session.request(method, url, headers=headers, **kwargs)  # Retry the request

        if response.status_code != 200:
            raise APIError(f"API call failed: {response.text}")

        return response.json()

    def get_applied_filters(self):
        """
        Fetch the applied filters from the API.

        Returns:
            dict: A dictionary containing the applied filters and other response data.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/filters')

    def get_models(self):
        """
        Fetch all models from the API.

        Returns:
            dict: A dictionary containing the models and other response data.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/models')

    def create_session(self, session_name):
        """
        Create a new chat session.

        Args:
            session_name (str): The name of the session to create.

        Returns:
            dict: A dictionary containing the session ID and other response data.

        Raises:
            APIError: If the API call fails.
        """
        data = {"sessionName": session_name}
        return self.call_api('POST', '/api/v1/session/create', json=data)

    def delete_session(self, session_id):
        """
        Delete a chat session.

        Args:
            session_id (str): The _id of the session to delete.

        Returns:
            dict: A dictionary containing response data.

        Raises:
            APIError: If the API call fails.
        """
        if not isinstance(session_id, str) or not session_id:
            raise ValueError("session_id must be a non-empty string")
        data = {"sessionId": session_id}
        return self.call_api('POST', '/api/v1/session/delete', json=data)

    def rename_session(self, session_id, new_name):
        """
        Rename a chat session.

        Args:
            session_id (str): The ID of the session to rename.
            new_name (str): The new name for the session.

        Returns:
            dict: A dictionary containing response data.

        Raises:
            APIError: If the API call fails or if a session with the new name already exists.
            ValueError: If session_id or new_name is invalid.
        """
        if not session_id or not isinstance(session_id, str):
            raise ValueError("session_id must be a non-empty string")
        if not new_name or not isinstance(new_name, str):
            raise ValueError("new_name must be a non-empty string")

        data = {"sessionId": session_id, "newName": new_name}
        return self.call_api('POST', '/api/v1/session/rename', json=data)

    def check_token_usage(self):
        """
        Check the token usage for the current user.

        Returns:
            dict: A dictionary containing token usage information.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/tokens')

    def filter_text(self, text):
        """
        Filter the given text using applicable filters.

        Args:
            text (str): The text to be filtered.

        Returns:
            dict: A dictionary containing the filtered text, filter counts, and hash map.

        Raises:
            APIError: If the API call fails.
            ValueError: If text is invalid.
        """
        if not text or not isinstance(text, str):
            raise ValueError("text must be a non-empty string")

        data = {"text": text}
        return self.call_api('POST', '/api/v1/filterText', json=data)

    def submit_prompt(self, session, message, model, filter_counts=None, context_prompts=None):
        """
        Submit a prompt to the ChatGPT model.

        Args:
            session (dict): A dictionary containing 'sessionId' and 'sessionName'.
            message (str): The prompt message to send.
            model (str): The name of the model to use.
            filter_counts (dict, optional): A dictionary of filter counts.
            context_prompts (list, optional): A list of context prompts.

        Returns:
            dict: The response from the ChatGPT model.

        Raises:
            APIError: If the API call fails.
            ValueError: If required parameters are missing or invalid.
        """
        if not isinstance(session, dict) or 'sessionId' not in session or 'sessionName' not in session:
            raise ValueError("session must be a dictionary containing 'sessionId' and 'sessionName'")
        if not message or not isinstance(message, str):
            raise ValueError("message must be a non-empty string")
        if not model or not isinstance(model, str):
            raise ValueError("model must be a non-empty string")

        data = {
            "session": session,
            "message": message,
            "model": model,
            "filterCounts": filter_counts or {},
            "contextPrompts": context_prompts or []
        }
        return self.call_api('POST', '/api/v1/submitPrompt', json=data)
