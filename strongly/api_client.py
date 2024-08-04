import os
from dotenv import load_dotenv
import requests
from .exceptions import AuthenticationError, APIError

class APIClient:
    def __init__(self, env_file='.env'):
        load_dotenv(env_file)

        self.host = os.getenv('API_HOST')
        self.api_key = os.getenv('API_KEY')
        self.session = requests.Session()
        self._auth_token = None

        if not self.host or not self.api_key:
            raise ValueError("API_HOST and API_KEY must be set in the .env file or as environment variables")

    def authenticate(self):
        url = f"{self.host}/api/v1/authenticate"
        headers = {'X-API-Key': self.api_key}

        response = self.session.get(url, headers=headers)

        if response.status_code != 200:
            raise AuthenticationError(f"Authentication failed: {response.text}")

        data = response.json()
        self._auth_token = data.get('authToken')
        if not self._auth_token:
            raise AuthenticationError("No auth token received from authentication endpoint")
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
