from app.core.security import hash_password, verify_password



def test_verify_password_accepts_correct_password():
    my_password = "super_password"
    hashed = hash_password(my_password)
    assert verify_password(my_password, hashed) is True


def test_verify_password_rejects_incorrect_password():
    my_password = "super_password"
    hashed = hash_password("incorrect_password")
    assert verify_password(my_password, hashed) is False


def test_password_hasher_does_not_return_plaintext():
    my_password = "super_password"
    hashed = hash_password
    assert hashed != my_password
