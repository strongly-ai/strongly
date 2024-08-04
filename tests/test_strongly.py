import pytest
from unittest.mock import patch, Mock
from strongly import APIClient
from strongly.exceptions import AuthenticationError, APIError

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

def test_get_models(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Models retrieved successfully',
        'userId': 'test-user-id',
        'models': [
            {'id': '1', 'name': 'Model 1'},
            {'id': '2', 'name': 'Model 2'}
        ]
    })

    result = api_client.get_models()

    assert 'models' in result
    assert len(result['models']) == 2
    assert result['models'][0]['name'] == 'Model 1'
    assert result['userId'] == 'test-user-id'
    api_client.call_api.assert_called_once_with('GET', '/api/v1/models')

def test_get_applied_filters(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Applied filters retrieved successfully',
        'userId': 'test-user-id',
        'filters': [
            {
                "_id": "11",
                "name": "Address",
                "description": "A street address."
            },
            {
                "_id": "iYafk8FLdus5SGJy2",
                "name": "Food",
                "description": "This is a test of the topic filter to detect food related posts."
            }
        ]
    })

    result = api_client.get_applied_filters()

    assert 'filters' in result
    assert len(result['filters']) == 2
    assert result['filters'][0]['name'] == 'Address'
    assert result['filters'][1]['name'] == 'Food'
    assert 'checked' not in result['filters'][0]
    assert 'checked' not in result['filters'][1]
    assert result['userId'] == 'test-user-id'
    api_client.call_api.assert_called_once_with('GET', '/api/v1/filters')

def test_create_session(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Session created successfully',
        'sessionId': 'test-session-id'
    })

    result = api_client.create_session('Test Session')

    assert result['message'] == 'Session created successfully'
    assert result['sessionId'] == 'test-session-id'
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/session/create',
        json={'sessionName': 'Test Session'}
    )
