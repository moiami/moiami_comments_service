def create_comment_example(client, text: str):
    response = client.post(
        "/api/v1/comments",
        json={
            "text": text,
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "movie_id": "550e8400-e29b-41d4-a716-446655440001",
        },
    )
    return response


def test_create_comment(client):
    response = create_comment_example(client, "Nice movie")
    assert response.status_code == 201


def test_create_invalid_comment(client):
    response = client.post("/api/v1/comments", json={"text": "Nice movie"})
    assert response.status_code == 400


def test_get_comment(client):
    response = create_comment_example(client, "Nice movie")
    if response.status_code != 201:
        raise Exception(f"Failed to create comment: {response.get_data(as_text=True)}")
    comment_id = response.get_json()["id"]

    response = client.get(f"/api/v1/comments/{comment_id}")
    assert response.status_code == 200
    assert response.get_json()["text"] == "Nice movie"


def test_update_comment(client):
    response = create_comment_example(client, "Nice movie")
    if response.status_code != 201:
        raise Exception(f"Failed to create comment: {response.get_data(as_text=True)}")
    comment_id = response.get_json()["id"]

    response = client.put(
        f"/api/v1/comments/{comment_id}",
        json={
            "text": "Awesome movie",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    )
    assert response.status_code == 200
    assert response.get_json()["text"] == "Awesome movie"


def test_delete_comment(client):
    response = create_comment_example(client, "Nice movie")
    if response.status_code != 201:
        raise Exception(f"Failed to create comment: {response.get_data(as_text=True)}")
    comment_id = response.get_json()["id"]

    response = client.delete(
        f"/api/v1/comments/{comment_id}",
        json={
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
        },
    )
    assert response.status_code == 200
