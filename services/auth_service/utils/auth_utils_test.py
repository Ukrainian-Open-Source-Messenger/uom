from utils.auth import hash_password, verify_password, create_token
import pytest


def test_hash_password():
    hashed = hash_password("password")
    assert hashed is not None
    assert isinstance(hashed, str)
    assert verify_password("password", hashed) is True

def test_create_token():
    token = create_token("1", "username")
    assert token is not None
    assert isinstance(token, str)

