#!/usr/bin/python3
"""This is the review class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from models import storage_type



class Review(BaseModel, Base):
    """This is the class for Review
    Attributes:
        ambulance_id: place id
        user_id: user id
        text: review description
    """
    if storage_type == "db":
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        stars = Column(Float, nullable=False)
    else:
        text = ""
        stars = 0.0


class ReviewSystemUser(BaseModel, Base):
    """This is the class for Review
    Attributes:
        ambulance_id: place id
        user_id: user id
        text: review description
    """
    if storage_type == "db":
        __tablename__ = "review_systemUsers"
        review_id = Column(Integer, ForeignKey('reviews.id'))
        systemUser_id = Column(Integer, ForeignKey('system_users.id'))
    else:
        review_id = ""
        systemUser_id = ""

class ReviewService(BaseModel, Base):
    """This is the class for Review
    Attributes:
        ambulance_id: place id
        user_id: user id
        text: review description
    """
    if storage_type == "db":
        __tablename__ = "review_services"
        review_id = Column(Integer, ForeignKey('reviews.id'))
        service_id = Column(Integer, ForeignKey('services.id'))
    else:
        review_id = ""
        service_id = ""