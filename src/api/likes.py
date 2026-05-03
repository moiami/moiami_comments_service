import uuid
from http import HTTPStatus

from flask import Blueprint, request, jsonify

from src.core.exceptions import ValidationError
from src.services.likes import LikeService

bp = Blueprint("likes", __name__, url_prefix="/api/v1/comments")
like_service = LikeService()

@bp.route("/<uuid:comment_id>/likes", methods=["POST"])
def create_like(comment_id):
    req = request.get_json()

    if not req.get("user_id"):
        raise ValidationError("User ID is required")
    if not req.get("comment_id"):
        raise ValidationError("Comment ID is required")

    try:
        like = like_service.create_like(
            user_id=uuid.UUID(req["user_id"]),
            comment_id=uuid.UUID(req["comment_id"]),
        )
        return jsonify(like.to_dict()), HTTPStatus.CREATED

    except ValueError:
        raise ValidationError("Invalid like model format")

@bp.route("/<uuid:comment_id>/likes", methods=["GET"])
def get_likes_for_comment(comment_id):
    # Flask handles UUID conversion, so comment_id is valid. Otherwise, Flask returns 404 to user.
    likes = like_service.get_likes_by_comment(comment_id)
    return jsonify([like.to_dict() for like in likes]), HTTPStatus.OK


@bp.route("/<uuid:comment_id>/likes/count", methods=["GET"])
def count_likes_for_comment(comment_id):
    likes_count = like_service.count_likes_by_comment(comment_id)
    return jsonify({"likes_count": likes_count}), HTTPStatus.OK


@bp.route("/<uuid:comment_id>/likes", methods=["DELETE"])
def delete_like(comment_id):
    req = request.get_json()

    if not req or not req.get("user_id"):
        raise ValidationError("User ID is required")

    try:
        like_service.delete_like_by_comment_and_user(
            comment_id=comment_id,
            user_id=uuid.UUID(req["user_id"]),
        )
        return "", HTTPStatus.OK
    except ValueError:
        raise ValidationError("Invalid like ID format")
