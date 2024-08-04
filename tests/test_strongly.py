import pytest
from unittest.mock import patch, Mock
from strongly import APIClient
from strongly.exceptions import AuthenticationError, APIError

def test_init_missing_env(monkeypatch):
    monkeypatch.delenv('API_HOST', raising=False)
    monkeypatch.delenv('API_KEY', raising=False)
    with pytest.raises(ValueError):
        APIClient(test_env={})  # Pass an empty dict as test_env

def test_authenticate_success(api_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'authToken': 'test-auth-token'}
    api_client.session.get.return_value = mock_response

    token = api_client.authenticate()

    assert token == 'test-auth-token'
    assert api_client._auth_token == 'test-auth-token'  # Changed from session_token to _auth_token
    api_client.session.get.assert_called_once_with(
        f"{api_client.host}/api/v1/authenticate",
        headers={'X-API-Key': api_client.api_key}
    )

def test_authenticate_failure(api_client):
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = 'Authentication failed'
    api_client.session.get.return_value = mock_response

    with pytest.raises(AuthenticationError):
        api_client.authenticate()

def test_call_api_success(api_client):
    api_client.authenticate = Mock(return_value='test-session-token')
    api_client._auth_token = 'test-session-token'
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'data': 'test-data'}
    api_client.session.request.return_value = mock_response

    result = api_client.call_api('GET', '/test-endpoint')

    assert result == {'data': 'test-data'}
    api_client.session.request.assert_called_once_with(
        'GET',
        'https://api.example.com/test-endpoint',
        headers={'X-API-Key': 'test-api-key', 'X-Auth-Token': 'test-session-token'}
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
    api_client.authenticate = Mock(return_value='test-session-token')
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

# New test function for delete_session
def test_delete_session(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Session deleted successfully'
    })

    session_id = 'test-session-id'
    result = api_client.delete_session(session_id)

    assert result['message'] == 'Session deleted successfully'
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/session/delete',
        json={'sessionId': session_id}
    )

def test_delete_session_api_error(api_client):
    api_client.call_api = Mock(side_effect=APIError("API call failed"))

    session_id = 'test-session-id'
    with pytest.raises(APIError):
        api_client.delete_session(session_id)

def test_delete_session_invalid_id(api_client):
    invalid_ids = [None, "", 123, []]

    for invalid_id in invalid_ids:
        with pytest.raises(ValueError):
            api_client.delete_session(invalid_id)

def test_rename_session(api_client):
    api_client.call_api = Mock(return_value={
        'message': 'Session renamed successfully'
    })

    session_id = 'test-session-id'
    new_name = 'New Test Session Name'
    result = api_client.rename_session(session_id, new_name)

    assert result['message'] == 'Session renamed successfully'
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/session/rename',
        json={'sessionId': session_id, 'newName': new_name}
    )

def test_rename_session_existing_name(api_client):
    api_client.call_api = Mock(side_effect=APIError("A session with this name already exists"))

    session_id = 'test-session-id'
    new_name = 'Existing Session Name'
    with pytest.raises(APIError, match="A session with this name already exists"):
        api_client.rename_session(session_id, new_name)

def test_rename_session_invalid_input(api_client):
    invalid_inputs = [
        (None, 'New Name'),
        ('', 'New Name'),
        ('session-id', None),
        ('session-id', ''),
        (123, 'New Name'),
        ('session-id', 123),
    ]

    for session_id, new_name in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.rename_session(session_id, new_name)

def test_rename_session_not_found(api_client):
    api_client.call_api = Mock(side_effect=APIError("Session not found"))

    session_id = 'non-existent-session-id'
    new_name = 'New Name'
    with pytest.raises(APIError, match="Session not found"):
        api_client.rename_session(session_id, new_name)


def test_check_token_usage(api_client):
    mock_response = {
        'isOverLimit': False,
        'isRestricted': False,
        'userTokenUsage': 5000,
        'planTokenLimit': 10000,
        'companyTokensAvailable': 5000,
        'purchasedTokens': 2000,
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.check_token_usage()

    assert result == mock_response
    api_client.call_api.assert_called_once_with('GET', '/api/v1/tokens')

def test_check_token_usage_over_limit(api_client):
    mock_response = {
        'isOverLimit': True,
        'isRestricted': False,
        'userTokenUsage': 15000,
        'planTokenLimit': 10000,
        'companyTokensAvailable': 0,
        'purchasedTokens': 5000,
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.check_token_usage()

    assert result == mock_response
    assert result['isOverLimit']
    api_client.call_api.assert_called_once_with('GET', '/api/v1/tokens')

def test_check_token_usage_restricted(api_client):
    mock_response = {
        'isOverLimit': True,
        'isRestricted': True,
        'userTokenUsage': 15000,
        'planTokenLimit': 10000,
        'companyTokensAvailable': 0,
        'purchasedTokens': 0,
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.check_token_usage()

    assert result == mock_response
    assert result['isOverLimit']
    assert result['isRestricted']
    api_client.call_api.assert_called_once_with('GET', '/api/v1/tokens')

def test_filter_text(api_client):
    mock_response = {
        'filteredText': 'This is a [1:sensitive] message.',
        'filterCounts': {'1': 1},
        'hashMap': {'[1:sensitive]': 'confidential'}
    }
    api_client.call_api = Mock(return_value=mock_response)

    result = api_client.filter_text("This is a confidential message.")

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/filterText',
        json={'text': "This is a confidential message."}
    )

def test_filter_text_invalid_input(api_client):
    invalid_inputs = [None, "", 123, []]

    for invalid_input in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.filter_text(invalid_input)

def test_submit_prompt(api_client):
    mock_response = {
        'content': 'This is a response from the ChatGPT model.'
    }
    api_client.call_api = Mock(return_value=mock_response)

    session = {'sessionId': 'test-session-id', 'sessionName': 'Test Session'}
    message = "What is the capital of France?"
    model = "gpt-3.5-turbo"

    result = api_client.submit_prompt(session, message, model)

    assert result == mock_response
    api_client.call_api.assert_called_once_with(
        'POST',
        '/api/v1/submitPrompt',
        json={
            'session': session,
            'message': message,
            'model': model,
            'filterCounts': {},
            'contextPrompts': []
        }
    )

def test_submit_prompt_topic_match(api_client):
    error_message = 'Your message contains content related to the following restricted topics: Sensitive Topic'
    api_client.call_api = Mock(side_effect=APIError(error_message))

    session = {'sessionId': 'test-session-id', 'sessionName': 'Test Session'}
    message = "This is a sensitive message."
    model = "gpt-3.5-turbo"

    with pytest.raises(APIError) as excinfo:
        api_client.submit_prompt(session, message, model)

    assert str(excinfo.value) == error_message

def test_submit_prompt_invalid_input(api_client):
    invalid_inputs = [
        ({}, "message", "model"),
        ({"sessionId": "id"}, "message", "model"),
        ({"sessionName": "name"}, "message", "model"),
        ({"sessionId": "id", "sessionName": "name"}, "", "model"),
        ({"sessionId": "id", "sessionName": "name"}, "message", ""),
    ]

    for session, message, model in invalid_inputs:
        with pytest.raises(ValueError):
            api_client.submit_prompt(session, message, model)
