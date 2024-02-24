#! /usr/bin/python3
"""This is the Location module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.hospital import Hospital
from models.ambulance.ambulance import Ambulance


class Address(BaseModel, Base):
    """This is the Address class"""
    __tablename__ = 'addresses'
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(100), nullable=False)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False)
    zipcode = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)


# This is the association table for the many-to-many relationship between
# locations and ambulances
location_ambulance = Table('location_ambulance', Base.metadata,
                            Column('location_id', Integer,
                                   ForeignKey('locations.location_id'),
                                   primary_key=True,
                                   nullable=False),
                            Column('ambulance_id', Integer,
                                   ForeignKey('ambulances.ambulance_id'),
                                   primary_key=True,
                                   nullable=False)
                            )

class Location(BaseModel, Base):
    """This is the Location class"""
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(Integer, ForeignKey('addresses.address_id'), nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)

    if models.storage_type == "db":
        hospitals = relationship("Hospital", backref="location",
                                 cascade="all, delete-orphan")
        ambulances = relationship("Ambulance", secondary=location_ambulance,
                                  backref="location", cascade="all, delete-orphan")
    else:
        name = ""
        address = ""
        city = ""
        state = ""
        zip_code = ""
        country = ""

        @property
        def ambulances(self):
            """This method returns a list of all ambulances at this location"""
            ambulances = models.storage.all(Ambulance)
            data =[]
            results = []
            for ambulance in ambulances.values():
                if ambulance.location_id == self.id:
                    data.append(ambulance)
            for ambulance in data:
                results.append(ambulance.to_dict())
            return results
        
        @property
        def hospitals(self):
            """This method returns a list of all hospitals at this location"""
            hospitals = models.storage.all(Hospital)
            data =[]
            results = []
            for hospital in hospitals.values():
                if hospital.location_id == self.id:
                    data.append(hospital)
            for hospital in data:
                results.append(hospital.to_dict())
            return results