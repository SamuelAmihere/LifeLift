#! /usr/bin/python3
"""This is the Ambulance Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime


if models.storage_type == "db":
    staff_drivers = Table('staff_drivers', Base.metadata,
                            Column('staff_id', Integer, ForeignKey('staff.id')),
                            Column('driver_id', Integer, ForeignKey('drivers.id'))
                            )


class Driver(BaseModel, Base):
    """This is the Driver class"""
    if models.storage_type == "db":
        __tablename__ = 'drivers'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        license_number = Column(String(50), unique=True)

    else:
        first_name = ""
        last_name = ""
        email = ""
        license_number = ""
        status = ""
        @property
        def status(self):
            """This method returns the status of the driver"""
            return self.status

        @status.setter
        def status(self, value):
            """This method sets the status of the driver"""
            self.status = value


class AmbulanceOwner(BaseModel, Base):
    """This is the Ambulance Operator class"""
    if models.storage_type == "db":
        __tablename__ = 'ambulance_owners'
        name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True)
        phone = Column(String(20))
        address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
        status = Column(Enum('Active', 'Inactive'), default='Active')
        ambulances = relationship("Ambulance", backref="ambulance_owners",
                              cascade="all, delete-orphan")
        drivers = relationship("Driver", backref="ambulance_owners",
                                cascade="all, delete-orphan")
    else:
        name = ""
        email = ""
        phone = ""
        address_id = ""
        status = "Active"
        available_ambulances = []
        available_drivers = []

        @property
        def ambulances(self):
            """This method returns a list of all ambulances
            owned by this operator
            """
            if len(self.available_ambulances) > 0:
                return self.available_ambulances
            return None

        @ambulances.setter
        def ambulances(self, value):
            """This method sets the list of all ambulances
            owned by this operator
            """
            if value not in self.available_ambulances:
                self.available_ambulances = value
        @property
        def drivers(self):
            """This method returns a list of all drivers
            owned by this operator
            """
            if len(self.available_drivers) > 0:
                return self.available_drivers
            return None

        @drivers.setter
        def drivers(self, value):
            """This method sets the list of all drivers
            owned by this operator
            """
            if value not in self.available_drivers:
                self.available_drivers = value
    
    def assign_driver_to_ambulance(self, driver_id:str, ambulance_id:str):
        """This method adds staff to an ambulance"""
        data = models.storage.all()
        ambus = {}
        for key, value in data.items():
            if 'Ambulance.' in key:
                ambus[key] = value
        ambu = ambus.get('Ambulance.'+ambulance_id)
        if ambu is not None:
            ambu.driver_id = driver_id
            ambu.updated_at = datetime.utcnow()
        ambus['Ambulance.'+ambulance_id] = ambu
    
        if ambu is not None:
            data.update(ambus)
            models.storage.save()
        return False
    
    # def remove_driver_from_ambulance(self, driver:Driver, ambulance:Ambulance):
    #     """This method removes driver from an ambulance"""
    #     if isinstance(driver, Driver) == False or\
    #         isinstance(ambulance, Ambulance) == False or\
    #         ambulance not in self.ambulances:
    #         return False
    #     self.ambulances.ambulance.remove(driver)
    #     return True