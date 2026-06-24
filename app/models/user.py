import enum

from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy import Enum as SAEnum

from app.database import Base


class UserRole(str, enum.Enum):
    operator = "operator"
    supervisor = "supervisor"


class User(Base):
    __tablename__ = "users"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    username        = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role            = Column(SAEnum(UserRole), nullable=False, default=UserRole.operator)

    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
    )
