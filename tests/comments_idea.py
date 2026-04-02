# class TestComments:
#     def __init__(self, client):
#         response = client.post("/api/v1/comments", json={
#             "text": "Nice",
#             "user_id": "qweasdb-123asdb-asdqw"
#         })
#         self.test_comment_id = response.get_json()["id"]

#     # and put tests here. The problem is - I check test_create_comment right inside init. That looks bad