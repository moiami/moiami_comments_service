import uuid
import pytest
from http import HTTPStatus

from src.services.comments import CommentService
from src.core.exceptions import ServiceError

USER_ID = uuid.uuid4()
MOVIE_ID = uuid.uuid4()


@pytest.fixture
def service():
    return CommentService()


def test_create_comment(db, service):
    comment = service.create_comment(
        text="Great movie",
        user_id=USER_ID,
        movie_id=MOVIE_ID,
    )
    assert comment.id is not None
    assert comment.text == "Great movie"
    assert comment.user_id == USER_ID


def test_get_comment(db, service):
    comment = service.create_comment("Hello", USER_ID, MOVIE_ID)
    fetched = service.get_comment(comment.id)
    assert fetched.id == comment.id


def test_get_comment_not_found(db, service):
    with pytest.raises(ServiceError) as exc:
        service.get_comment(uuid.uuid4())
    assert exc.value.status_code == HTTPStatus.NOT_FOUND


def test_update_comment(db, service):
    comment = service.create_comment("Original", USER_ID, MOVIE_ID)
    updated = service.update_comment(comment.id, text="Updated", user_id=USER_ID)
    assert updated.text == "Updated"


def test_update_comment_wrong_user(db, service):
    comment = service.create_comment("Original", USER_ID, MOVIE_ID)
    with pytest.raises(ServiceError) as exc:
        service.update_comment(comment.id, text="Hacked", user_id=uuid.uuid4())
    assert exc.value.status_code == HTTPStatus.FORBIDDEN


def test_delete_comment(db, service):
    comment = service.create_comment("To delete", USER_ID, MOVIE_ID)
    service.delete_comment(comment.id, USER_ID)
    with pytest.raises(ServiceError):
        service.get_comment(comment.id)


def test_delete_comment_wrong_user(db, service):
    comment = service.create_comment("Mine", USER_ID, MOVIE_ID)
    with pytest.raises(ServiceError) as exc:
        service.delete_comment(comment.id, uuid.uuid4())
    assert exc.value.status_code == HTTPStatus.FORBIDDEN
