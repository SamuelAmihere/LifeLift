#!/usr/bin/python3
"""This is the user class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Enum, String
from sqlalchemy import ForeignKey
from sqlalchemy import Column, String
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
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


class Patient(BaseModel, Base):
    """This is the Patient class"""
    if storage_type == "db":
        __tablename__ = 'patients'
        person_id = Column(String(60), ForeignKey('persons.id'), nullable=False)
        address_id = Column(String(60), ForeignKey('addresses.id'),
                            nullable=False)
        relative_phone = Column(String(20), nullable=True)
        incident_id = Column(String(60), ForeignKey('incidents.id'),
                             nullable=True)
        address = relationship("Address", back_populates="patients")

    else:
        address_id = ""
        relative_phone = ""
        incident_id = ""
        person_id = ""
        address = ""


class InternalUser(BaseModel, Base):
    """This is the class for the internal user
    """
    if storage_type == "db":
        __tablename__ = "internal_users"
        person_id = Column(String(60), ForeignKey('persons.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        user_id = ""
        person_id = ""


class Staff(BaseModel, Base):
    """This is the class defining a staff
    """
    if storage_type == "db":
        __tablename__ = "staff"
        internal_user_id = Column(String(60), ForeignKey('internal_users.id'),
                                  nullable=False)
        staff_number = Column(String(128), nullable=False)
        status = Column(Enum("Active", "Inactive"), default="Active")
        company_id = Column(String(60), ForeignKey('companies.id'), nullable=False)
        company = relationship("Company", back_populates="staff")
    else:
        internal_user_id = ""
        staff_number = ""
        status = ""

class AmbulanceStaff(BaseModel, Base):
    """This is the class for the ambulance staff
    """
    if storage_type == "db":
        __tablename__ = "ambulance_staff"
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
        ambulance_id = Column(String(60), ForeignKey('ambulances.id'),
                              nullable=False)
        ambulance = relationship("Ambulance", back_populates="ambulance_staff")
    else:
        staff_id = ""
        ambulance_id = ""

class Driver(BaseModel, Base):
    """This is the Driver class""" 
    if models.storage_type == "db":
        __tablename__ = 'drivers'
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
        license_number = Column(String(50), unique=True)
    else:
        staff_id = ""
        license_number = ""


class Dispatcher(BaseModel, Base):
    """This is the class for dispatcher
    """
    if storage_type == "db":
        __tablename__ = "dispatchers"
        staff_id = Column(String(60), ForeignKey('staff.id'), nullable=False)
    else:
        staff_id = ""

    def dispatch_ambulance(self, incident_id, hospital_id):
        """This is the method to dispatch ambulance"""
        pass