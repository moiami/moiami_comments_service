from marshmallow import Schema, fields


class LikeCreateSchema(Schema):
    user_id = fields.UUID(required=True)
