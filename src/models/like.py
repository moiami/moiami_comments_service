import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.core.db import db


class Like(db.Model):

    __tablename__ = "likes"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(), nullable=False)
    comment_id = Column(UUID(), ForeignKey("comments.id"), nullable=False)
    comment = db.relationship("Comment", backref="likes")

    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "comment_id": str(self.comment_id),
            "comment": self.comment.to_dict() if self.comment else None,
        }