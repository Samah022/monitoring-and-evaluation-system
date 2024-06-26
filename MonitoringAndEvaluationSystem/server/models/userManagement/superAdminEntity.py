from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

# Create the engine
engine = create_engine('sqlite:///monitoring-and-evaluation.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define your models using the base class


class Super_Admin(Base):
    __tablename__ = 'Super_Admin'
    SuperAdmin_ID = Column(Integer, primary_key=True, autoincrement=True)
    Email = Column(String, unique=True, nullable=False)
    Password = Column(String, nullable=False)
