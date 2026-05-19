"""Shared OpenAPI 2.0 definitions and examples for Flasgger."""

EXAMPLE_USER_ID = "550e8400-e29b-41d4-a716-446655440000"
EXAMPLE_MOVIE_ID = "550e8400-e29b-41d4-a716-446655440001"
EXAMPLE_COMMENT_ID = "550e8400-e29b-41d4-a716-446655440010"
EXAMPLE_LIKE_ID = "550e8400-e29b-41d4-a716-446655440020"

COMMENT_EXAMPLE = {
    "id": EXAMPLE_COMMENT_ID,
    "text": "Nice movie",
    "user_id": EXAMPLE_USER_ID,
    "movie_id": EXAMPLE_MOVIE_ID,
    "hide": False,
}

LIKE_EXAMPLE = {
    "id": EXAMPLE_LIKE_ID,
    "user_id": EXAMPLE_USER_ID,
    "comment_id": EXAMPLE_COMMENT_ID,
    "comment": COMMENT_EXAMPLE,
}

ERROR_EXAMPLE = {
    "error": "service_error",
    "message": "Comment not found",
}

SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Moiami Comments Service API",
        "description": "REST API for movie comments and likes",
        "version": "1.0.0",
    },
    "host": "localhost:8007",
    "basePath": "/",
    "schemes": ["http"],
    "tags": [
        {"name": "Comments", "description": "Comment operations"},
        {"name": "Likes", "description": "Like operations"},
    ],
    "definitions": {
        "Comment": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "format": "uuid"},
                "text": {"type": "string"},
                "user_id": {"type": "string", "format": "uuid"},
                "movie_id": {"type": "string", "format": "uuid"},
                "hide": {"type": "boolean"},
            },
            "example": COMMENT_EXAMPLE,
        },
        "CommentCreate": {
            "type": "object",
            "required": ["text", "user_id", "movie_id"],
            "properties": {
                "text": {"type": "string"},
                "user_id": {"type": "string", "format": "uuid"},
                "movie_id": {"type": "string", "format": "uuid"},
            },
            "example": {
                "text": "Nice movie",
                "user_id": EXAMPLE_USER_ID,
                "movie_id": EXAMPLE_MOVIE_ID,
            },
        },
        "CommentUpdate": {
            "type": "object",
            "required": ["user_id"],
            "properties": {
                "user_id": {"type": "string", "format": "uuid"},
                "text": {"type": "string"},
            },
            "example": {
                "user_id": EXAMPLE_USER_ID,
                "text": "Updated text",
            },
        },
        "CommentDelete": {
            "type": "object",
            "required": ["user_id"],
            "properties": {
                "user_id": {"type": "string", "format": "uuid"},
            },
            "example": {"user_id": EXAMPLE_USER_ID},
        },
        "Like": {
            "type": "object",
            "properties": {
                "id": {"type": "string", "format": "uuid"},
                "user_id": {"type": "string", "format": "uuid"},
                "comment_id": {"type": "string", "format": "uuid"},
                "comment": {"$ref": "#/definitions/Comment"},
            },
            "example": LIKE_EXAMPLE,
        },
        "LikeCreate": {
            "type": "object",
            "required": ["user_id"],
            "properties": {
                "user_id": {"type": "string", "format": "uuid"},
            },
            "example": {"user_id": EXAMPLE_USER_ID},
        },
        "LikesCount": {
            "type": "object",
            "properties": {
                "likes_count": {"type": "integer"},
            },
            "example": {"likes_count": 2},
        },
        "MessageResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"},
            },
        },
        "Error": {
            "type": "object",
            "properties": {
                "error": {"type": "string"},
                "message": {"type": "string"},
            },
            "example": ERROR_EXAMPLE,
        },
    },
}
