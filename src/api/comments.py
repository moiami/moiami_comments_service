from http import HTTPStatus

from flask_smorest import Blueprint
from flask.views import MethodView

from src.api.schemas.comments import (
    CommentCreateSchema,
    CommentResponseSchema,
    CommentUpdateSchema,
    CommentDeleteSchema,
)
from src.core.exceptions import ValidationError, ServiceError
from src.services.comments import CommentService

bp = Blueprint("comments", "comments", url_prefix="/api/v1/comments")
comment_service = CommentService()


@bp.route("/")
class CommentListResource(MethodView):
    @bp.arguments(CommentCreateSchema)
    @bp.response(HTTPStatus.CREATED, CommentResponseSchema)
    def post(self, data):
        try:
            comment = comment_service.create_comment(
                text=data["text"],
                user_id=data["user_id"],
                movie_id=data["movie_id"],
            )
            return comment.to_dict()
        except ValueError:
            raise ValidationError("Invalid comment model format")


@bp.route("/hide/<uuid:comment_id>")
class CommentHideResource(MethodView):
    @bp.response(HTTPStatus.OK)
    def post(self, comment_id):
        try:
            comment_service.hide_comment(comment_id)
            return {"message": "comment was hidden"}
        except ServiceError:
            raise ValidationError("Invalid comment ID")


@bp.route("/<uuid:comment_id>")
class CommentResource(MethodView):
    @bp.response(HTTPStatus.OK, CommentResponseSchema)
    def get(self, comment_id):
        try:
            comment = comment_service.get_comment(comment_id)
            return comment.to_dict()
        except ValueError:
            raise ValidationError("Invalid comment ID format")

    @bp.arguments(CommentUpdateSchema)
    @bp.response(HTTPStatus.OK, CommentResponseSchema)
    def put(self, data, comment_id):
        try:
            comment = comment_service.update_comment(
                comment_id=comment_id,
                text=data.get("text"),
                user_id=data["user_id"],
            )
            return comment.to_dict()
        except ValueError:
            raise ValidationError("Invalid UUID format")

    @bp.arguments(CommentDeleteSchema)
    @bp.response(HTTPStatus.OK)
    def delete(self, data, comment_id):
        try:
            comment_service.delete_comment(
                comment_id=comment_id,
                user_id=data["user_id"],
            )
            return {"message": "deleted"}
        except ValueError:
            raise ValidationError("Invalid user ID format")
