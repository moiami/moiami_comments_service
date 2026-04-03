import uuid

from flask import Blueprint, request, jsonify

from src.core.exceptions import ValidationError
from src.services.likes import LikeService

bp = Blueprint("likes", __name__, url_prefix="/api/v1/comments/likes")
like_service = LikeService()

@bp.route("", methods=["POST"])
def create_like():
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
        return jsonify(like.to_dict()), 201

    except ValueError:
        raise ValidationError("Invalid like model format")

@bp.route("/<uuid:comment_id>", methods=["GET"])
def get_likes_for_comment(comment_id):
    try:
        likes = like_service.get_likes_by_comment(comment_id)
        return jsonify([like.to_dict() for like in likes]), 200
    except ValueError:
        raise ValidationError("Invalid comment ID format")


@bp.route("/<uuid:like_id>", methods=["DELETE"])
def delete_like(like_id):
    req = request.get_json()

    if not req or not req.get("user_id"):
        raise ValidationError("User ID is required")

    try:
        like_service.delete_like(like_id, uuid.UUID(req["user_id"]))
        return "", 200
    except ValueError:
        raise ValidationError("Invalid like ID format")
