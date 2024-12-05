from sqlalchemy import Column, CHAR, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Adminn(Base):
    __tablename__ = "Admin"
    
    username = Column(VARCHAR(30))
    email = Column(VARCHAR(50), primary_key=True)
    senha = Column(VARCHAR(100))

    
