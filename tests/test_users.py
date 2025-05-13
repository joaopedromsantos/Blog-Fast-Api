def test_create_user(client):
    user_data = {
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "234hj45",
        "phone_number": "35999876765",
        "first_name": "João",
        "last_name": "Pedro",
        "gender": "M"
    }

    response = client.post("/signup/", json=user_data)

    assert response.status_code == 201

    data = response.json()
    assert data['result']['username'] == 'joao'
    assert data['result']['email'] == 'joao@gmail.com'
    assert data['message'] == "User registered successfully"


def test_login_user(client):
    user_data = {
        "username": "Rogerio",
        "email": "roger@gmail.com",
        "password": "456908kl",
        "phone_number": "35999873765",
        "first_name": "Rogerio",
        "last_name": "Freire",
        "gender": "M"
    }

    response = client.post("/signup/", json=user_data)

    assert response.status_code == 201

    login_data = {
        "username": "Rogerio",
        "password": "456908kl"
    }
    login_response = client.post("/login/", data=login_data)

    assert login_response.status_code == 200

    data = login_response.json()
    assert data['access_token'] != ""
    assert data['token_type'] == 'bearer'
