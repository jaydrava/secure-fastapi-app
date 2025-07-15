from app.utils import hash_password, verify_password
from app.schemas import UserCreate
import pytest


def test_hash_and_verify():
    raw = "MyStr0ngP@ss!"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed)


def test_usercreate_schema_valid():
    payload = {"username": "jay", "email": "jay@example.com", "password": "Secret123!"}
    user = UserCreate(**payload)
    assert user.username == "jay"


@pytest.mark.parametrize(
    "bad_email",
    ["not-an-email", "noatsign.com", "foo@bar"],
)
def test_usercreate_bad_email(bad_email):
    with pytest.raises(ValueError):
        UserCreate(username="a", email=bad_email, password="123456")
