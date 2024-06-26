# not use in this version
from sqlalchemy import create_engine, Column, Integer, VARCHAR, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from ..cameraManagement.cameraEntity import Camera

# Create the engine
engine = create_engine('sqlite:///monitoring-and-evaluation.db', echo=True)

# Create a base class for declarative models
Base = declarative_base()

# Define your models using the base class


class Uniform(Base):
    __tablename__ = 'Uniform'
    Timestamp = Column(DateTime, primary_key=True)
    Compliance = Column(VARCHAR(255), nullable=False)
    Amount = Column(Integer, nullable=False)
    Camera_ID = Column(Integer, ForeignKey(Camera.Camera_ID), nullable=False)
    camera = relationship(Camera)
