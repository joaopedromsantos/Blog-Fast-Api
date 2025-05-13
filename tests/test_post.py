def test_create_post(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {
          "title": "Teste de POST",
          "author_id": 0,
          "cover_image_url": "https://th.bing.com/th/id/OIP.1CbHBsd3Jr28rK54t_Mr2gHaD8?cb=iwp2&rs=1&pid=ImgDetMain",
          "content": "ISSO É APENAS TESTE"
        }

    response = client.post("/posts/", json=post_data, headers=headers)

    assert response.status_code == 201

    data = response.json()
    assert data['result']['title'] == 'Teste de POST'


def test_get_post(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {
        "title": "Post para GET",
        "author_id": 0,
        "cover_image_url": "https://example.com/image.png",
        "content": "Conteúdo de teste para GET"
    }
    create_response = client.post("/posts/", json=post_data, headers=headers)
    assert create_response.status_code == 201

    get_response = client.get("/posts?post_id=0", headers=headers)
    assert get_response.status_code == 200

    data = get_response.json()
    assert data['result'][0]['title'] == "Post para GET"


def test_delete_post(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {
        "title": "Post para DELETE",
        "author_id": 0,
        "cover_image_url": "https://example.com/image.png",
        "content": "Conteúdo de teste para DELETE"
    }

    create_response = client.post("/posts/", json=post_data, headers=headers)
    assert create_response.status_code == 201
    post_id = create_response.json()['result']['id']

    delete_response = client.delete(f"/posts/{post_id}", headers=headers)
    assert delete_response.status_code == 204

    get_response = client.get(f"/posts?post_id={post_id}", headers=headers)
    assert get_response.status_code == 404


def test_update_post(client, token):
    headers = {"Authorization": f"Bearer {token}"}
    post_data = {
        "title": "Post original",
        "author_id": 0,
        "cover_image_url": "https://example.com/original.png",
        "content": "Conteúdo original"
    }

    create_response = client.post("/posts/", json=post_data, headers=headers)
    assert create_response.status_code == 201

    post_id = create_response.json()['result']['id']
    update_data = {
        "title": "Post atualizado",
        "cover_image_url": "https://example.com/atualizado.png",
        "content": "Novo conteúdo editado"
    }

    update_response = client.put(f"/posts/{post_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200
    data = update_response.json()

    assert data['result']['title'] == "Post atualizado"

