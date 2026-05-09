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
