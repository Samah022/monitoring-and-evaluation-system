from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, VARCHAR
from sqlalchemy.orm import declarative_base

# Create the engine
engine = create_engine('sqlite:///monitoring-and-evaluation.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define your models using the base class


class Camera(Base):
    __tablename__ = 'Camera'
    Camera_ID = Column(Integer, primary_key=True,
                       autoincrement=True, nullable=False)
    Name = Column(VARCHAR(255), nullable=False)
    Link = Column(VARCHAR(255), unique=True, nullable=False)


# in the cloud only


class NewCameraEntity(BaseModel):
    name: str
    link: str
    criteria: list  # may this wrong as user may not enter criteria


class GetCameraEntity(BaseModel):
    id: int
    name: str
    link: str
    criteria: list
