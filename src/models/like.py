import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Like(db.Model):

    __tablename__ = "likes"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(), nullable=False)
    comment_id = Column(UUID(), nullable=False)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "comment_id": str(self.comment_id),
        }