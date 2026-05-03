from http import HTTPStatus

from flask_smorest import Blueprint
from flask.views import MethodView

from src.api.schemas.likes import LikeCreateSchema, LikeResponseSchema, LikesCountSchema
from src.core.exceptions import ValidationError
from src.services.likes import LikeService

bp = Blueprint("likes", "likes", url_prefix="/api/v1/comments")
like_service = LikeService()


@bp.route("/<uuid:comment_id>/likes")
class LikesResource(MethodView):
    @bp.arguments(LikeCreateSchema)
    @bp.response(HTTPStatus.CREATED, LikeResponseSchema)
    def post(self, data, comment_id):
        try:
            like = like_service.create_like(
                user_id=data["user_id"],
                comment_id=comment_id,
            )
            return like.to_dict()
        except ValueError:
            raise ValidationError("Invalid like model format")

    @bp.response(HTTPStatus.OK, LikeResponseSchema(many=True))
    def get(self, comment_id):
        likes = like_service.get_likes_by_comment(comment_id)
        return [like.to_dict() for like in likes]

    @bp.arguments(LikeCreateSchema)
    @bp.response(HTTPStatus.OK)
    def delete(self, data, comment_id):
        try:
            like_service.delete_like_by_comment_and_user(
                comment_id=comment_id,
                user_id=data["user_id"],
            )
            return {"message": "deleted"}
        except ValueError:
            raise ValidationError("Invalid like ID format")


@bp.route("/<uuid:comment_id>/likes/count")
class LikesCountResource(MethodView):
    @bp.response(HTTPStatus.OK, LikesCountSchema)
    def get(self, comment_id):
        count = like_service.count_likes_by_comment(comment_id)
        return {"likes_count": count}
