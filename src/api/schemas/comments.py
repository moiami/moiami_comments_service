from marshmallow import Schema, fields


class CommentCreateSchema(Schema):
    text = fields.String(required=True)
    user_id = fields.UUID(required=True)
    movie_id = fields.UUID(required=True)


class CommentUpdateSchema(Schema):
    text = fields.String(required=False)
    user_id = fields.UUID(required=True)


class CommentDeleteSchema(Schema):
    user_id = fields.UUID(required=True)


class CommentResponseSchema(Schema):
    id = fields.UUID()
    text = fields.String()
    user_id = fields.UUID()
    movie_id = fields.UUID()
    hide = fields.Boolean()
    created_at = fields.DateTime(allow_none=True)
