import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class Comment(db.Model):

    __tablename__ = "comments"

    id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    text = Column(String(4000), nullable=False)
    user_id = Column(UUID(), nullable=False)
    movie_id = Column(UUID(), nullable=False)
    hide = Column(Boolean, default=False, nullable=False)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "text": self.text,
            "user_id": str(self.user_id),
            "movie_id": str(self.movie_id),
            "hide": self.hide,
        }