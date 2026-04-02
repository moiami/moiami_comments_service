def create_comment_example(client, text: str):
    response = client.post("/api/v1/comments", json={
        "text": text,
        "user_id": "qweasdb-123asdb-asdqw"
    })
    return response

def test_create_like(client):
    response_comment = create_comment_example(client, "Nice movie")
    if response_comment.status_code != 201:
        raise Exception(f"Failed to create comment: {response_comment.get_data(as_text=True)}")
    comment_id = response_comment.get_json()["id"]
    
    response_like = client.post(f"/api/v1/comments/{comment_id}/likes", json={
        "user_id": "qweasdb-123asdb-asdqw",
        "comment_id": comment_id
    })
    assert response_like.status_code == 201

def test_create_invalid_like(client):
    response_comment = create_comment_example(client, "Nice movie")
    if response_comment.status_code != 201:
        raise Exception(f"Failed to create comment: {response_comment.get_data(as_text=True)}")
    comment_id = response_comment.get_json()["id"]

    response_like = client.post(f"/api/v1/comments/{comment_id}/likes", json={
        "user_id": "qweasdb-123asdb-asdqw",
    })
    assert response_like.status_code == 400

def test_get_likes_by_comment(client):
    # Create comment
    response_comment = create_comment_example(client, "Nice movie")
    if response_comment.status_code != 201:
        raise Exception(f"Failed to create comment: {response_comment.get_data(as_text=True)}")
    comment_id = response_comment.get_json()["id"]

    # Create likes
    response_like = client.post(f"/api/v1/comments/{comment_id}/likes", json={
        "user_id": "qweasdb-123asdb-asdqw",
        "comment_id": comment_id
    })
    if response_like.status_code != 201:
        raise Exception(f"Failed to create like: {response_like.get_data(as_text=True)}")
    
    response_like = client.post(f"/api/v1/comments/{comment_id}/likes", json={
        "user_id": "qweasdb-123asdb-asdqwabc",
        "comment_id": comment_id
    })
    if response_like.status_code != 201:
        raise Exception(f"Failed to create like: {response_like.get_data(as_text=True)}")

    response = client.get(f"/api/v1/comments/{comment_id}/likes")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_delete_like(client):
    response = create_comment_example(client, "Nice movie")
    if response.status_code != 201:
        raise Exception(f"Failed to create comment: {response.get_data(as_text=True)}")
    comment_id = response.get_json()["id"]

    # Create like
    response_like = client.post(f"/api/v1/comments/{comment_id}/likes", json={
        "user_id": "qweasdb-123asdb-asdqw",
        "comment_id": comment_id
    })
    if response_like.status_code != 201:
        raise Exception(f"Failed to create like: {response_like.get_data(as_text=True)}")

    response = client.delete(f"/api/v1/comments/{comment_id}/likes", json={
        "user_id": "qweasdb-123asdb-asdqw"
    })
    assert response.status_code == 200