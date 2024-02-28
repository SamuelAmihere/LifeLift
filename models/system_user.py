#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy.ext.declarative import declarative_base
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, Integer, String
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


class Person(BaseModel, Base):
    """This is the class for Person
    """
    if storage_type == "db":
        __tablename__ = "persons"
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        gender = Column(String(128), nullable=False)
    else:
        first_name = ""
        last_name = ""
        gender = ""


class SystemUser(Person, Base):
    """This is the class for user
    """
    if storage_type == "db":
        __tablename__ = "system_users"
        email = Column(String(128), nullable=True)
        phone_number = Column(String(128), nullable=False)
        reviews = relationship("Review", secondary=systemUser_reviews,
                               back_populates="system_users", nullable=True)
    else:
        email = ""
        phone_number = ""
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


class Patient_119(SystemUser, Base):
    """This is the Patient class"""
    if storage_type == "db":
        __tablename__ = 'patients'
        address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
        relative_phone = Column(String(20), nullable=True)
    else:
        address_id = ""
        relative_phone = ""


class InternalUser(SystemUser, Base):
    """This is the class for the internal user
    """
    if storage_type == "db":
        __tablename__ = "internal_users"
        password = Column(String(128), nullable=False, default="password",
                          server_default="password")
    else:
        password = ""


class Staff(SystemUser, Base):
    """This is the class defining a staff
    """
    if storage_type == "db":
        __tablename__ = "staff"
        staff_number = Column(String(128), nullable=False)
        role = Column(String(128), nullable=False)
        status = Column(Enum("Active", "Inactive"), default="Active")
    else:
        staff_number = ""
        role = ""
        status = ""


class Driver(Staff, Base):
    """This is the Driver class""" 
    if models.storage_type == "db":
        __tablename__ = 'drivers'
        license_number = Column(String(50), unique=True)
    else:
        license_number = ""


class Dispatcher(Staff, Base):
    """This is the class for dispatcher
    """
    if storage_type == "db":
        __tablename__ = "dispatchers"
    else:
        pass

    def dispatch_ambulance(self, incident_id, hospital_id):
        """This is the method to dispatch ambulance"""
        pass