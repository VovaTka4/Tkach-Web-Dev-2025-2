import pytest, re

from app.validators.password_validator import password_validator

@pytest.mark.parametrize("input_password, expected_output", [
    ("1", "Пароль должен содержать как минимум 8 символов!"),
    ("h3aK9vBzM1qXeLp7CgQ0Tw2AnRUYfsd5XtjZcPmvoG8lyNbHWEDrV6pFikO4JMXau0YgR9Kt7BLiwhQYFeAVPnxscbZqdrT5omv2XUpG1lsj34WCE96kNDyMt712345678", "Пароль должен содержать не более 128 символов!"),
    ("abracadabra", "Пароль должен содержать хотя бы одну заглавную букву!"),
    ("ABRACADABRA", "Пароль должен содержать хотя бы одну строчную букву!"),
    ("Abracadabra", "Пароль должен содержать хотя бы одну цифру!"),
    ("Abracadabra 52", "Пароль не должен содержать пробелов!"),
    ("Abracadabra€42", "Используются запрещенные символы! Вводите только латинские или кириллические буквы, цифры 0-9, а также любые из спец. символов: ~ ! ? @ # $ % ^ & * _ - + ( ) [ ] { } > < / \ | \" ' . , : ;"),
    ("Abracadabra15", None)
])
def test_password_validation(input_password, expected_output):
    assert password_validator(input_password) == expected_output
