import uuid
from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ARRAY, Float  # or from sqlalchemy.dialects.postgresql
from pgvector.sqlalchemy import Vector

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)
    genre = Column(String)
    isbn = Column(String)
    available = Column(Boolean, default=True)

    description = Column(String, nullable=True)
    embedding = Column(ARRAY(Float), nullable=True)  # Ready for semantic search
