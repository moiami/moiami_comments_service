import uuid
import pytest
from http import HTTPStatus

from src.services.comments import CommentService
from src.services.likes import LikeService
from src.core.exceptions import ServiceError

USER_ID = uuid.uuid4()
OTHER_USER_ID = uuid.uuid4()
MOVIE_ID = uuid.uuid4()


@pytest.fixture
def comment_service():
    return CommentService()


@pytest.fixture
def like_service():
    return LikeService()


@pytest.fixture
def comment(db, comment_service):
    # most like tests need an existing comment
    return comment_service.create_comment("Test comment", USER_ID, MOVIE_ID)


def test_create_like(db, like_service, comment):
    like = like_service.create_like(user_id=USER_ID, comment_id=comment.id)
    assert like.id is not None
    assert like.comment_id == comment.id
    assert like.user_id == USER_ID


def test_get_likes_by_comment(db, like_service, comment):
    like_service.create_like(USER_ID, comment.id)
    like_service.create_like(OTHER_USER_ID, comment.id)
    likes = like_service.get_likes_by_comment(comment.id)
    assert len(likes) == 2


def test_get_likes_by_comment_empty(db, like_service, comment):
    likes = like_service.get_likes_by_comment(comment.id)
    assert likes == []


def test_delete_like(db, like_service, comment):
    like_service.create_like(USER_ID, comment.id)
    like_service.delete_like_by_comment_and_user(comment.id, USER_ID)
    likes = like_service.get_likes_by_comment(comment.id)
    assert len(likes) == 0


def test_delete_like_not_found(db, like_service, comment):
    with pytest.raises(ServiceError) as exc:
        like_service.delete_like_by_comment_and_user(comment.id, USER_ID)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND


def test_delete_like_wrong_user(db, like_service, comment):
    like_service.create_like(USER_ID, comment.id)
    with pytest.raises(ServiceError) as exc:
        like_service.delete_like_by_comment_and_user(comment.id, OTHER_USER_ID)
    assert exc.value.status_code == HTTPStatus.NOT_FOUND