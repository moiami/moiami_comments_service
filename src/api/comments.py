from flask import Blueprint, request, jsonify
from http import HTTPStatus
from marshmallow import ValidationError as MarshmallowValidationError

from src.api.schemas.comments import (
    CommentCreateSchema,
    CommentUpdateSchema,
    CommentDeleteSchema,
)
from src.core.exceptions import ValidationError, ServiceError
from src.services.comments import CommentService

bp = Blueprint("comments", __name__, url_prefix="/api/v1/comments")
comment_service = CommentService()


@bp.route("/", methods=["POST"])
def create_comment():
    """
    Create a new comment
    ---
    tags:
      - Comments
    parameters:
      - in: body
        name: body
        required: true
    responses:
      201:
        description: Comment created successfully
      400:
        description: Validation error
    """
    try:
        schema = CommentCreateSchema()
        json_data = request.get_json(silent=True) or {}
        data = schema.load(json_data)
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    try:
        comment = comment_service.create_comment(
            text=data["text"],
            user_id=data["user_id"],
            movie_id=data["movie_id"],
        )

        response_data = comment.to_dict()
        response_data["id"] = str(comment.id)
        return jsonify(response_data), HTTPStatus.CREATED
    except ValueError:
        raise ValidationError("Invalid comment model format")


@bp.route("/hide/<uuid:comment_id>", methods=["POST"])
def hide_comment(comment_id):
    """
    Hide a comment
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
    responses:
      200:
        description: Comment hidden successfully
      400:
        description: Invalid comment ID
    """
    try:
        comment_service.hide_comment(comment_id)
        return jsonify({"message": "comment was hidden"}), HTTPStatus.OK
    except ServiceError:
        raise ValidationError("Invalid comment ID")


@bp.route("/<uuid:comment_id>", methods=["GET"])
def get_comment(comment_id):
    """
    Get comment by ID
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
    responses:
      200:
        description: Comment details
      400:
        description: Invalid comment ID format
    """
    try:
        comment = comment_service.get_comment(comment_id)
        return jsonify(comment.to_dict()), HTTPStatus.OK
    except ValueError:
        raise ValidationError("Invalid comment ID format")


@bp.route("/<uuid:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    """
    Update a comment
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
      - in: body
        name: body
        required: true
    responses:
      200:
        description: Comment updated
      400:
        description: Validation error
    """
    try:
        schema = CommentUpdateSchema()
        json_data = request.get_json(silent=True) or {}
        data = schema.load(json_data)
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    try:
        comment = comment_service.update_comment(
            comment_id=comment_id,
            text=data.get("text"),
            user_id=data["user_id"],
        )
        return jsonify(comment.to_dict()), HTTPStatus.OK
    except ValueError:
        raise ValidationError("Invalid UUID format")


@bp.route("/<uuid:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    """
    Delete a comment
    ---
    tags:
      - Comments
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
      - in: body
        name: body
        required: true
    responses:
      200:
        description: Comment deleted
      400:
        description: Validation error
    """
    try:
        schema = CommentDeleteSchema()
        json_data = request.get_json(silent=True) or {}
        data = schema.load(json_data)
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    try:
        comment_service.delete_comment(
            comment_id=comment_id,
            user_id=data["user_id"],
        )
        return jsonify({"message": "deleted"}), HTTPStatus.OK
    except ValueError:
        raise ValidationError("Invalid user ID format")
