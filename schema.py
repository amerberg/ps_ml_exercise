from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_handle = Column(Integer, primary_key=True)
    #TODO: make the length customizable. For now, 512 has been confirmed to be sufficient.
    most_similar = Column(String(length=512))