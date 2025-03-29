import pytest, re

def phone_validator_from_app(phone):
        phone_parsed = re.sub(r'[\- ().]','',phone)
    
        if phone_parsed.startswith(('+7')):
            if len(phone_parsed) == 12:
                phone_parsed = phone_parsed[2:]
                if re.search(r'[^\d]', phone_parsed):
                    return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
                else:
                    return f"8-{phone_parsed[:3]}-{phone_parsed[3:5]}-{phone_parsed[5:7]}-{phone_parsed[7:]}"
            else:
                return "Недопустимый ввод. Неверное количество цифр."
                
        elif len(phone_parsed) == 11 and phone_parsed.startswith('8'):
            phone_parsed = phone_parsed[1:]
            if re.search(r'[^\d]', phone_parsed):
                return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
            else:
                return f"8-{phone_parsed[:3]}-{phone_parsed[3:5]}-{phone_parsed[5:7]}-{phone_parsed[7:]}"
            
        elif len(phone_parsed) == 10:
            if re.search(r'[^\d]', phone_parsed):
                return "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
            else:
                return f"8-{phone_parsed[:3]}-{phone_parsed[3:6]}-{phone_parsed[6:8]}-{phone_parsed[8:]}"

        else:  
            return "Недопустимый ввод. Неверное количество цифр."

def test_urlparams_page(client):
    response = client.get("/urlparams?name=Vova&age=20&hobby=yachting")
    assert response.status_code == 200
    assert "name" in response.get_data(as_text=True)
    assert "age" in response.get_data(as_text=True)
    assert "hobby" in response.get_data(as_text=True)
    page_content = response.get_data(as_text=True)
    assert "Ключ: name — Значение: Vova" in page_content
    assert "Ключ: age — Значение: 20" in page_content
    assert "Ключ: hobby — Значение: yachting" in page_content
    
def test_urlparams_page_noparams(client):
    response = client.get("/urlparams")
    assert response.status_code == 200
    assert "Нет переданных параметров" in response.get_data(as_text=True)
    
def test_headers_page(client):
    headers = {
        "User-Agent": "pytest-client",
        "Custom-Header": "CustomValue"
    }
    response = client.get("/headers", headers=headers)

    assert response.status_code == 200

    page_content = response.get_data(as_text=True)

    for key, value in headers.items():
        expected_text = f"Заголовок: {key} — Значение: {value}"
        assert expected_text in page_content
        
def test_cookie_assertion(client):
    response = client.get("/cookies")
    assert response.status_code == 200
    assert "MY_COOKIE=\"IS WORKING!\"" in response.headers.get("Set-Cookie", "")
    
def test_cookie_delete(client):
    client.get("/cookies")  
    response = client.get("/cookies")
    assert "MY_COOKIE=IS WORKING!" not in response.headers.get("Set-Cookie", "")
    
def test_form_page(client):
    data = {"phone": "+79991234567"}
    response = client.post("/", data = data)
    assert response.status_code == 200
    
    page_content = response.get_data(as_text=True)
    print(page_content) 

    assert '<input type="text" id="phone" name="phone" class="form-control mb-3' in page_content
    assert 'value="+79991234567"' in page_content
    
@pytest.mark.parametrize("input_phone, expected_output", [
    ("+7 (999) 123-45-67", "8-999-12-34-567"),
    ("8(999)1234567", "8-999-12-34-567"),
    ("999.123.45.67", "8-999-123-45-67"),
    ("123", "Недопустимый ввод. Неверное количество цифр."),
    ("123123aabb", "Недопустимый ввод. В номере телефона встречаются недопустимые символы."),
    ("+7 (999) 1ab-c5-67", "Недопустимый ввод. В номере телефона встречаются недопустимые символы."),
    ("8(9+9)1234567", "Недопустимый ввод. В номере телефона встречаются недопустимые символы."),
    ("+7(213)", "Недопустимый ввод. Неверное количество цифр."),
    ("..........", "Недопустимый ввод. Неверное количество цифр.")
])
def test_phone_validator_function(input_phone, expected_output):
    assert phone_validator_from_app(input_phone) == expected_output
    
def test_form_page_bootstrap(client):
    data = {"phone": "8964777aa22"}
    response = client.post("/", data = data)
    assert response.status_code == 200
    
    page_content = response.get_data(as_text=True)
    print(page_content) 

    assert '<div class="invalid-feedback">' in page_content
    assert  "Недопустимый ввод. В номере телефона встречаются недопустимые символы." in page_content
    assert 'class="form-control mb-3 is-invalid"' in page_content
    
def test_form_page_phone_check(client):
    data = {"phone": "+79991234567"}
    response = client.post("/", data = data)
    assert response.status_code == 200
    
    page_content = response.get_data(as_text=True)
    print(page_content) 

    assert "Отформатированный телефон: 8-999-12-34-567" in page_content