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
from models.review import Review, ReviewSystemUser

if storage_type == "db":
    systemUser_reviews = Table('systemUser_review', Base.metadata,
                                Column('systemUser_id', Integer,
                                    ForeignKey('system_users.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('review_systemUsers_id', Integer,
                                    ForeignKey('review_systemUsers.id'),
                                    primary_key=True,
                                    nullable=False)
                                )


class SystemUser(BaseModel, Base):
    """This is the class for user
    """
    if storage_type == "db":
        __tablename__ = "system_users"
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False, default="password",
                          server_default="password")
        user_type = Column(String(128), nullable=False)
        reviews = relationship("Review", secondary=systemUser_reviews,
                               back_populates="system_users", nullable=True)
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
        user_type = ""
        reviews = []

        @property
        def reviews(self):
            """Getter for reviews
            """
            if len(self.reviews) > 0:
                return self.reviews
            return None
        @reviews.setter
        def reviews(self, value: ReviewSystemUser):
            """Setter for reviews
            """
            if type(value) == Review and value not in self.reviews:
                self.reviews.append(value)

    def is_valid_password(self, password: str) -> bool:
        """This method checks if the password is valid
        """
        # TODO: Implement this method
        pass