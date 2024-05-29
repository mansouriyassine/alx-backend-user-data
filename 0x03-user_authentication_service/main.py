#!/usr/bin/env python3
"""
End-to-end integration test.
"""
import requests

BASE_URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Register a new user"""
    url = f"{BASE_URL}/users"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with wrong password"""
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 401, response.text


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials"""
    url = f"{BASE_URL}/sessions"
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200, response.text
    session_id = response.cookies.get('session_id')
    assert session_id is not None
    return session_id

def profile_unlogged() -> None:
    """Access profile without logging in"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, response.text


def profile_logged(session_id: str) -> None:
    """Access profile after logging in"""
    url = f"{BASE_URL}/profile"
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, response.text
    assert 'email' in response.json()

def log_out(session_id: str) -> None:
    """Log out"""
    url = f"{BASE_URL}/sessions"
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 302, response.text


def reset_password_token(email: str) -> str:
    """Get a reset password token"""
    url = f"{BASE_URL}/reset_password"
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200, response.text
    reset_token = response.json().get('reset_token')
    assert reset_token is not None
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using reset token"""
    url = f"{BASE_URL}/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    response = requests.put(url, data=data)
    assert response.status_code == 200, response.text
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
