import pytest
from unittest.mock import patch, Mock
from your_api_package import APIClient
from your_api_package.exceptions import AuthenticationError, APIError

def test_init_missing_env(monkeypatch):
    monkeypatch.delenv('API_HOST', raising=False)
    monkeypatch.delenv('API_KEY', raising=False)
    with pytest.raises(ValueError):
        APIClient()

def test_authenticate_success(api_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'sessionToken': 'test-session-token'}
    api_client.session.get.return_value = mock_response

    token = api_client.authenticate()

    assert token == 'test-session-token'
    assert api_client.session_token == 'test-session-token'
    api_client.session.get.assert_called_once_with(
        'https://api.example.com/api/v1/authenticate',
        params={'authenticateToken': 'test-api-key'}
    )

def test_authenticate_failure(api_client):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = 'Authentication failed'
    api_client.session.get.return_value = mock_response

    with pytest.raises(AuthenticationError):
        api_client.authenticate()

def test_call_api_success(api_client):
    api_client.session_token = 'test-session-token'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': 'test-data'}
    api_client.session.request.return_value = mock_response

    result = api_client.call_api('GET', '/test-endpoint')

    assert result == {'data': 'test-data'}
    api_client.session.request.assert_called_once_with(
        'GET',
        'https://api.example.com/test-endpoint',
        params={'sessionToken': 'test-session-token'}
    )

def test_call_api_session_expired(api_client):
    api_client.session_token = 'expired-token'
    mock_responses = [
        Mock(status_code=401, text='Unauthorized'),
        Mock(status_code=200, json=Mock(return_value={'data': 'test-data'}))
    ]
    api_client.session.request.side_effect = mock_responses
    api_client.authenticate = Mock(return_value='new-session-token')

    result = api_client.call_api('GET', '/test-endpoint')

    assert result == {'data': 'test-data'}
    assert api_client.authenticate.called
    assert api_client.session.request.call_count == 2

def test_call_api_failure(api_client):
    api_client.session_token = 'test-session-token'
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = 'Internal Server Error'
    api_client.session.request.return_value = mock_response

    with pytest.raises(APIError):
        api_client.call_api('GET', '/test-endpoint')

def test_get_data(api_client):
    api_client.call_api = Mock(return_value={'data': 'test-data'})

    result = api_client.get_data()

    assert result == {'data': 'test-data'}
    api_client.call_api.assert_called_once_with('GET', '/api/v1/getData')

def test_another_method(api_client):
    api_client.call_api = Mock(return_value={'result': 'success'})

    result = api_client.another_method('test-arg')

    assert result == {'result': 'success'}
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/anotherMethod',
        json={'someArg': 'test-arg'}
    )
