from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text, String, func, DateTime, Integer

class Base(DeclarativeBase):
    pass

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

# Petit utilitaire pour tester la DB
def db_now(session):
    return session.execute(text("SELECT CURRENT_DATE")).scalar_one()
