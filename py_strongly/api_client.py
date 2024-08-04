import os
import requests
from dotenv import load_dotenv
from .exceptions import AuthenticationError, APIError

load_dotenv()

class APIClient:
    def __init__(self):
        self.host = os.getenv('API_HOST')
        self.key = os.getenv('API_KEY')
        self.session_token = None
        self.session = requests.Session()

        if not self.host or not self.key:
            raise ValueError("API_HOST and API_KEY must be set in environment variables")

    def authenticate(self):
        url = f"{self.host}/api/v1/authenticate"
        response = self.session.get(url, params={'authenticateToken': self.key})

        if response.status_code != 200:
            raise AuthenticationError(f"Authentication failed: {response.text}")

        data = response.json()
        self.session_token = data['sessionToken']
        return self.session_token

    def get_models(self):
        """
        Fetch all models from the API.

        Returns:
            dict: A dictionary containing the models and other response data.

        Raises:
            APIError: If the API call fails.
        """
        return self.call_api('GET', '/api/v1/models')

    def call_api(self, method, endpoint, **kwargs):
        if not self.session_token:
            self.authenticate()

        url = f"{self.host}{endpoint}"
        kwargs['params'] = kwargs.get('params', {})
        kwargs['params']['sessionToken'] = self.session_token

        response = self.session.request(method, url, **kwargs)

        if response.status_code == 401:  # Unauthorized, session might have expired
            self.session_token = None
            self.authenticate()
            kwargs['params']['sessionToken'] = self.session_token
            response = self.session.request(method, url, **kwargs)

        if response.status_code != 200:
            raise APIError(f"API call failed: {response.text}")

        return response.json()
