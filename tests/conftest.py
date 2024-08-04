import pytest
from unittest.mock import Mock
from strongly import APIClient

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv('API_HOST', 'https://api.example.com')
    monkeypatch.setenv('API_KEY', 'test-api-key')

@pytest.fixture
def mock_session():
    return Mock()

@pytest.fixture
def api_client(mock_env, mock_session):
    client = APIClient()
    client.session = mock_session
    return client
