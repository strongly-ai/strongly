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

    def get_data(self):
        return self.call_api('GET', '/api/v1/getData')

    def another_method(self, some_arg):
        return self.call_api('POST', '/api/v1/anotherMethod', json={'someArg': some_arg})

    # Add more methods as needed for your API endpoints
