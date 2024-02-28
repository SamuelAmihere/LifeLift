#!/usr/bin/python3
"""This is the review class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float
from models import storage_type



class Review(BaseModel, Base):
    """This is the class for Reviews
    """
    if storage_type == "db":
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        stars = Column(Float, nullable=False)
    else:
        text = ""
        stars = 0.0


class ReviewSystemUser(Review):
    """This is the class for Review by system user
    """
    if storage_type == "db":
        __tablename__ = "review_systemUsers"
        internal_user_id = Column(String(60),
                          ForeignKey('internal_users.id'),
                          nullable=False,
                          primary_key=True)
    else:
        pass


class ReviewService(Review):
    """This is the class for Review by service user
    """
    if storage_type == "db":
        __tablename__ = "review_services"
        patient_id = Column(String(60),
                          ForeignKey('patients.id'),
                          nullable=False,
                          primary_key=True)
        service_id = Column(String(60),
                          ForeignKey('service.id'),
                          nullable=False,
                          primary_key=True)
    else:
        pass