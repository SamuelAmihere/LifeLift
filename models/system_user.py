#!/usr/bin/python3
"""This is the user class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, String
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from models import storage_type


class Person(BaseModel, Base):
    """This is the class for Person
    """
    if storage_type == "db":
        __tablename__ = "persons"
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        gender = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
        email = Column(String(128), nullable=True)
    else:
        first_name = ""
        last_name = ""
        gender = ""
        phone_number = ""
        email = ""


class Patient(Person):
    """This is the Patient class"""
    if storage_type == "db":
        __tablename__ = 'patients'
        address_id = Column(String(60), ForeignKey('addresses.id'),
                            nullable=False)
        relative_phone = Column(String(20), nullable=True)
        incident_id = Column(String(60), ForeignKey('incidents.id'),
                             nullable=True)
    else:
        address_id = ""
        relative_phone = ""
        incident_id = ""


class InternalUser(Person):
    """This is the class for the internal user
    """
    if storage_type == "db":
        __tablename__ = "internal_users"
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        user_id = ""


class Staff(InternalUser):
    """This is the class defining a staff
    """
    if storage_type == "db":
        __tablename__ = "staff"
        staff_number = Column(String(128), nullable=False)
        status = Column(Enum("Active", "Inactive"), default="Active")
    else:
        staff_number = ""
        status = ""


class Driver(Staff):
    """This is the Driver class""" 
    if models.storage_type == "db":
        __tablename__ = 'drivers'
        license_number = Column(String(50), unique=True)
    else:
        license_number = ""


class Dispatcher(Staff):
    """This is the class for dispatcher
    """
    if storage_type == "db":
        __tablename__ = "dispatchers"
    else:
        pass

    def dispatch_ambulance(self, incident_id, hospital_id):
        """This is the method to dispatch ambulance"""
        pass