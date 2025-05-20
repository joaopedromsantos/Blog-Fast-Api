import pytest


def get_headers(token):
    return {"Authorization": f"Bearer {token}"}


def create_post(client, token, title="Post Padrão", content="Conteúdo padrão", author_id=1):
    headers = get_headers(token)
    post_data = {
        "title": title,
        "author_id": author_id,
        "content": content,
    }
    response = client.post("/posts/", data=post_data, files={}, headers=headers)
    assert response.status_code == 201
    return response.json()['result']


def test_create_post(client, token):
    post = create_post(client, token, title="Teste de POST", content="ISSO É APENAS TESTE")
    assert post["title"] == "Teste de POST"


def test_get_post(client, token):
    post = create_post(client, token, title="Post para GET", content="Conteúdo de teste para GET")

    response = client.get(f"/posts?post_id={post['id']}", headers=get_headers(token))
    assert response.status_code == 200

    data = response.json()
    assert data['result']['title'] == "Post para GET"


def test_delete_post(client, token):
    post = create_post(client, token, title="Post para DELETE", content="Conteúdo para DELETE")

    delete_response = client.delete(f"/posts/{post['id']}", headers=get_headers(token))
    assert delete_response.status_code == 204

    get_response = client.get(f"/posts?post_id={post['id']}", headers=get_headers(token))
    assert get_response.status_code == 404


def test_update_post(client, token):
    post = create_post(client, token, title="Post original", content="Conteúdo original")

    update_data = {
        "title": "Post atualizado",
        "content": "Novo conteúdo editado"
    }

    update_response = client.put(
        f"/posts/{post['id']}",
        data=update_data,
        files={},
        headers=get_headers(token)
    )
    assert update_response.status_code == 200
    updated = update_response.json()["result"]
    assert updated["title"] == "Post atualizado"
