import uuid

from flask import Blueprint, request, jsonify

from src.core.exceptions import ValidationError
from src.services.comments import CommentService

bp = Blueprint("comments", __name__, url_prefix="/api/v1/comments")
comment_service = CommentService()

@bp.route("", methods=["POST"])
def create_comment():
    req = request.get_json()

    if not req.get("text"):
        raise ValidationError("Text is required")
    if not req.get("user_id"):
        raise ValidationError("User ID is required")
    if not req.get("movie_id"):
        raise ValidationError("Movie ID is required")

    try:
        comment = comment_service.create_comment(
            text=req["text"],
            user_id=uuid.UUID(req["user_id"]),
            movie_id=uuid.UUID(req["movie_id"])
        )
        return jsonify(comment.to_dict()), 201

    except ValueError:
        raise ValidationError()

@bp.route("/<uuid:comment_id>", methods=["GET"])
def get_comment(comment_id):
    comment = comment_service.get_comment(comment_id)
    return jsonify(comment.to_dict()), 200


@bp.route("/<uuid:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    data = request.get_json()

    if not data.get("user_id"):
        raise ValidationError("User ID is required")

    try:
        comment = comment_service.update_comment(
            comment_id=comment_id,
            text=data.get("text"),
            user_id=uuid.UUID(data["user_id"]),
        )
        return jsonify(comment.to_dict()), 200
    except ValueError:
        raise ValidationError("Invalid UUID format")


@bp.route("/<uuid:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    req = request.get_json()

    if not req or not req.get("user_id"):
        raise ValidationError("User ID is required")

    try:
        comment_service.delete_comment(comment_id, uuid.UUID(req["user_id"]))
        return "", 200
    except ValueError:
        raise ValidationError("Invalid user ID format")