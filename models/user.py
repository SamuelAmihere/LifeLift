#!/usr/bin/python3
"""This is the user class"""
from models import models
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.ambulance.ambulance import Ambulance
from models.review import Review


class User(BaseModel, Base):
    """This is the class for user
    Attributes:
        email: email address
        password: password for you login
        first_name: first name
        last_name: last name
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    user_type = Column(String(128), nullable=False)
    ambulances = relationship("Ambulance", cascade='all, delete, delete-orphan',
                          backref="user", nullable=True)
    
    if models.storage_type != "db":
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                           backref="user")