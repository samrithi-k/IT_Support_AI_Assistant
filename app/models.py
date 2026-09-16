from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Text

from .database import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    retrieved_context = Column(
        Text,
        nullable=False
    )

    ai_response = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )