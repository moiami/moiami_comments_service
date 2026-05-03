from marshmallow import Schema, fields


class LikeCreateSchema(Schema):
    user_id = fields.UUID(required=True)


class LikeResponseSchema(Schema):
    id = fields.UUID()
    user_id = fields.UUID()
    comment_id = fields.UUID()
    created_at = fields.DateTime()


class LikesCountSchema(Schema):
    likes_count = fields.Integer()
