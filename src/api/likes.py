from flask import Blueprint, request, jsonify
from http import HTTPStatus
from marshmallow import ValidationError as MarshmallowValidationError

from src.api.schemas.likes import LikeCreateSchema
from src.core.exceptions import ValidationError
from src.services.likes import LikeService

bp = Blueprint("likes", __name__, url_prefix="/api/v1/comments")
like_service = LikeService()


@bp.route("/<uuid:comment_id>/likes", methods=["POST"])
def create_like(comment_id):
    """
    Create a like for a comment
    ---
    tags:
      - Likes
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
        example: "550e8400-e29b-41d4-a716-446655440010"
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/LikeCreate'
    responses:
      201:
        description: Like created successfully
        schema:
          $ref: '#/definitions/Like'
        examples:
          application/json:
            id: "550e8400-e29b-41d4-a716-446655440020"
            user_id: "550e8400-e29b-41d4-a716-446655440000"
            comment_id: "550e8400-e29b-41d4-a716-446655440010"
            comment:
              id: "550e8400-e29b-41d4-a716-446655440010"
              text: "Nice movie"
              user_id: "550e8400-e29b-41d4-a716-446655440000"
              movie_id: "550e8400-e29b-41d4-a716-446655440001"
              hide: false
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
      409:
        description: User already liked this comment
        schema:
          $ref: '#/definitions/Error'
        examples:
          application/json:
            error: "service_error"
            message: "User already liked this comment"
    """
    try:
        schema = LikeCreateSchema()
        json_data = request.get_json(silent=True) or {}
        data = schema.load(json_data)
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    try:
        like = like_service.create_like(
            user_id=data["user_id"],
            comment_id=comment_id,
        )
        return jsonify(like.to_dict()), HTTPStatus.CREATED
    except ValueError:
        raise ValidationError("Invalid like model format")


@bp.route("/<uuid:comment_id>/likes", methods=["GET"])
def get_likes(comment_id):
    """
    Get all likes for a comment
    ---
    tags:
      - Likes
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
        example: "550e8400-e29b-41d4-a716-446655440010"
    responses:
      200:
        description: List of likes (may be empty)
        schema:
          type: array
          items:
            $ref: '#/definitions/Like'
        examples:
          application/json:
            - id: "550e8400-e29b-41d4-a716-446655440020"
              user_id: "550e8400-e29b-41d4-a716-446655440000"
              comment_id: "550e8400-e29b-41d4-a716-446655440010"
              comment:
                id: "550e8400-e29b-41d4-a716-446655440010"
                text: "Nice movie"
                user_id: "550e8400-e29b-41d4-a716-446655440000"
                movie_id: "550e8400-e29b-41d4-a716-446655440001"
                hide: false
    """
    likes = like_service.get_likes_by_comment(comment_id)
    return jsonify([like.to_dict() for like in likes]), HTTPStatus.OK


@bp.route("/<uuid:comment_id>/likes", methods=["DELETE"])
def delete_like(comment_id):
    """
    Remove a like from a comment
    ---
    tags:
      - Likes
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
        example: "550e8400-e29b-41d4-a716-446655440010"
      - in: body
        name: body
        required: true
        schema:
          $ref: '#/definitions/LikeCreate'
    responses:
      200:
        description: Like removed successfully
        schema:
          $ref: '#/definitions/MessageResponse'
        examples:
          application/json:
            message: "deleted"
      400:
        description: Validation error
        schema:
          $ref: '#/definitions/Error'
      404:
        description: Like not found
        schema:
          $ref: '#/definitions/Error'
        examples:
          application/json:
            error: "service_error"
            message: "Like not found"
    """
    try:
        schema = LikeCreateSchema()
        json_data = request.get_json(silent=True) or {}
        data = schema.load(json_data)
    except MarshmallowValidationError as e:
        raise ValidationError(str(e.messages))

    try:
        like_service.delete_like_by_comment_and_user(
            comment_id=comment_id,
            user_id=data["user_id"],
        )
        return jsonify({"message": "deleted"}), HTTPStatus.OK
    except ValueError:
        raise ValidationError("Invalid like ID format")


@bp.route("/<uuid:comment_id>/likes/count", methods=["GET"])
def get_likes_count(comment_id):
    """
    Get likes count for a comment
    ---
    tags:
      - Likes
    parameters:
      - name: comment_id
        in: path
        required: true
        type: string
        format: uuid
        example: "550e8400-e29b-41d4-a716-446655440010"
    responses:
      200:
        description: Likes count
        schema:
          $ref: '#/definitions/LikesCount'
        examples:
          application/json:
            likes_count: 2
      404:
        description: Comment not found
        schema:
          $ref: '#/definitions/Error'
        examples:
          application/json:
            error: "service_error"
            message: "Comment not found"
    """
    count = like_service.count_likes_by_comment(comment_id)
    return jsonify({"likes_count": count}), HTTPStatus.OK
