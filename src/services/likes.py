from uuid import UUID
from http import HTTPStatus

from src.core.db import db
from src.core.exceptions import ServiceError
from src.models.comment import Comment
from src.models.like import Like

# from src.services.resource_client import ResourceClient
from sqlalchemy.exc import IntegrityError


class LikeService:
    def create_like(self, user_id: UUID, comment_id: UUID) -> Like:
        # resource_client = ResourceClient(current_app.config["RESOURCE_SERVICE_URL"])
        # if not resource_client.movie_exists(movie_id):
        #     raise ServiceError("Movie not found in resource-service", status_code=404)

        like = Like(user_id=user_id, comment_id=comment_id)
        db.session.add(like)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ServiceError(
                "User already liked this comment", status_code=HTTPStatus.CONFLICT
            )
        return like

    def get_like(self, like_id: UUID) -> Like:
        like = db.session.get(Like, like_id)
        if like is None:
            raise ServiceError("Like not found", status_code=HTTPStatus.NOT_FOUND)
        return like

    def get_likes_by_comment(self, comment_id: UUID) -> list[Like]:
        return Like.query.filter_by(comment_id=comment_id).all()

    def count_likes_by_comment(self, comment_id: UUID) -> int:
        comment = db.session.get(Comment, comment_id)
        if comment is None:
            raise ServiceError("Comment not found", status_code=HTTPStatus.NOT_FOUND)

        return Like.query.filter_by(comment_id=comment_id).count()

    def delete_like_by_comment_and_user(self, comment_id: UUID, user_id: UUID) -> None:
        like = Like.query.filter_by(comment_id=comment_id, user_id=user_id).first()
        if like is None:
            raise ServiceError("Like not found", status_code=HTTPStatus.NOT_FOUND)
        db.session.delete(like)
        db.session.commit()
