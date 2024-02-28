#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy.ext.declarative import declarative_base
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String
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
    else:
        first_name = ""
        last_name = ""
        gender = ""


class SystemUser(Person):
    """This is the class for user
    """
    if storage_type == "db":
        __tablename__ = "system_users"
        email = Column(String(128), nullable=True)
        phone_number = Column(String(128), nullable=False)
    else:
        email = ""
        phone_number = ""

    def is_valid_password(self, password: str) -> bool:
        """This method checks if the password is valid
        """
        # TODO: Implement this method
        pass


class Patient_119(SystemUser):
    """This is the Patient class"""
    if storage_type == "db":
        __tablename__ = 'patients'
        address_id = Column(Integer, ForeignKey('addresses.id'),
                            nullable=False)
        relative_phone = Column(String(20), nullable=True)
        incident_id = Column(Integer, ForeignKey('incidents.id'),
                             nullable=True)
    else:
        address_id = ""
        relative_phone = ""


class InternalUser(SystemUser):
    """This is the class for the internal user
    """
    if storage_type == "db":
        __tablename__ = "internal_users"
        password = Column(String(128), nullable=False,
                          default="password",
                          server_default="password")
        user_type = Column(Enum("Admin", "Operator", "Dispatcher", "Driver", "Hospital"), nullable=False)
    else:
        password = ""


class Staff(SystemUser):
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