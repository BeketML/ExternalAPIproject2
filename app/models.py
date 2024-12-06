from sqlalchemy import Column, Integer, String
from app.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class AdminModel(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)