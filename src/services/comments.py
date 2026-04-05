from uuid import UUID
from http import HTTPStatus

from flask import current_app

from src.core.db import db
from src.core.exceptions import ServiceError
from src.models.comment import Comment
# from src.services.resource_client import ResourceClient


class CommentService:

    def create_comment(self, text: str, user_id: UUID, movie_id: UUID) -> Comment:
        # resource_client = ResourceClient(current_app.config["RESOURCE_SERVICE_URL"])
        # if not resource_client.movie_exists(movie_id):
        #     raise ServiceError("Movie not found in resource-service", status_code=404)

        comment = Comment(text=text, user_id=user_id, movie_id=movie_id)
        db.session.add(comment)
        db.session.commit()
        return comment

    def get_comment(self, comment_id: UUID) -> Comment:
        comment = db.session.get(Comment, comment_id)
        if comment is None:
            raise ServiceError("Comment not found", status_code=HTTPStatus.NOT_FOUND)
        return comment

    def update_comment(self, comment_id: UUID, text: str | None, user_id: UUID) -> Comment:
        comment = self.get_comment(comment_id)

        if comment.user_id != user_id:
            raise ServiceError(
                "User is not the owner of this comment", status_code=HTTPStatus.FORBIDDEN)

        if text is not None:
            comment.text = text

        db.session.commit()
        return comment

    def delete_comment(self, comment_id: UUID, user_id: UUID) -> None:
        comment = self.get_comment(comment_id)

        if comment.user_id != user_id:
            raise ServiceError(
                "User is not the owner of this comment", status_code=HTTPStatus.FORBIDDEN)

        db.session.delete(comment)
        db.session.commit()
