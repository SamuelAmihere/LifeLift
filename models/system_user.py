#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from models.base_model import BaseModel, Base
from models import storage_type
import models
from models.review import Review

if storage_type == "db":
       systemUser_review = Table('system_user_review', Base.metadata,
                            Column(Integer,
                                   ForeignKey('system_users.id'),
                                   primary_key=True,
                                   nullable=False),
                            Column( Integer,
                                   ForeignKey('reviews.id'),
                                   primary_key=True,
                                   nullable=False)
                                   )

class SystemUser(BaseModel, Base):
    """This is the class for user
    """
    if storage_type == "db":
        __tablename__ = "system_users"
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        user_type = Column(String(128), nullable=False)
        reviews = relationship("Review", secondary=systemUser_review,
                               viewonly=False, back_populates="system_users")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        user_type = ""

        @property
        def reviews(self):
            """getter for reviews"""
            reviews = models.storage.all('Review')
            data = []
            result = []
            for review in reviews.values():
                if review.user_id == self.id:
                    data.append(review)
            for review in data:
                result.append(review.to_dict())
            return result