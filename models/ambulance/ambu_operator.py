#! /usr/bin/python3
"""This is the Ambulance Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.ambulance.ambulance import Ambulance
from models.location import Address
from models.ambulance.driver import Driver


class AmbulanceStaff(BaseModel, Base):
    """This is the Ambulance Staff class"""
    __tablename__ = 'ambulance_staff'
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    role = Column(String(100), nullable=False)


class AmbulanceOwner(BaseModel, Base):
    """This is the Ambulance Operator class"""
    __tablename__ = 'ambulance_owners'
    ambu_owner_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address_id = Column(Integer, ForeignKey('addresses.address_id'), nullable=False)

    status = Column(Enum('Active', 'Inactive'), default='Active')
    if models.storage_type != "db":
        ambulances = relationship("Ambulance", backref="ambulance_owners",
                              cascade="all, delete-orphan")
        staff = relationship("AmbulanceStaff", backref="ambulance_owners",
                                cascade="all, delete-orphan")
        drivers = relationship("Driver", backref="ambulance_owners",
                                cascade="all, delete-orphan")
    else:
        @property
        def ambulances(self):
            """This method returns a list of all ambulances
            owned by this operator
            """
            ambulances = models.storage.all(Ambulance)
            data = []
            results = []
            for ambulance in ambulances:
                if ambulance.ambu_owner_id == self.id:
                    data.append(ambulance)
            for ambulance in data:
                results.append(ambulance.to_dict())
            return results
        @property
        def staff(self):
            """This method returns a list of all staff
            owned by this operator
            """
            staff = models.storage.all(AmbulanceStaff)
            data = []
            results = []
            for member in staff:
                if member.owner_id == self.id:
                    data.append(member)
            for member in data:
                results.append(member.to_dict())
            return results
        @property
        def drivers(self):
            """This method returns a list of all drivers
            owned by this operator
            """
            drivers = models.storage.all(Driver)
            data = []
            results = []
            for driver in drivers:
                if driver.owner_id == self.id:
                    data.append(driver)
            for driver in data:
                results.append(driver.to_dict())
            return results