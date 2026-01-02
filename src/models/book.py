from src.database.connection import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    author: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    rating: Mapped[float] = mapped_column()  # e.g., 4.5

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title}, author={self.author}, rating={self.rating})"
