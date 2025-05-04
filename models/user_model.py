from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database import Model


class UserTable(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]

    task = relationship("TaskTable", back_populates="user")
