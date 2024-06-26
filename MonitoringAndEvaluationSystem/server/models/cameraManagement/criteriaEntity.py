from sqlalchemy import create_engine, Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from .cameraEntity import Camera

# Create the engine
engine = create_engine('sqlite:///monitoring-and-evaluation.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define your models using the base class


class Criteria(Base):
    __tablename__ = 'Criteria'
    Name = Column(VARCHAR(255), primary_key=True, nullable=False)
    Camera_ID = Column(Integer, ForeignKey(Camera.Camera_ID),
                       primary_key=True, nullable=False)
    camera = relationship(Camera)
