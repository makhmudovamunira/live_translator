from sqlalchemy import Column, String, Integer, Text
from sqlalchemy_utils import ChoiceType
from database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(Text, nullable=False)
    email = Column(String(50), nullable=False)
    def __repr__(self):
        return '<User:{self.username}>'