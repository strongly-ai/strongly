from strongly.exceptions import AuthenticationError, APIError

def test_authentication_error():
    error = AuthenticationError("Test authentication error")
    assert str(error) == "Test authentication error"

def test_api_error():
    error = APIError("Test API error")
    assert str(error) == "Test API error"
