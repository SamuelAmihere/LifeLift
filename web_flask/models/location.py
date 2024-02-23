#! /usr/bin/python3
"""This is the Location module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.ambulance import Ambulance
from models.hospital import Hospital


class Location(BaseModel, Base):
    """This is the Location class"""
    def __init__(self, *args, **kwargs):
        """This method initializes a new instance of the Location class"""
        super().__init__(*args, **kwargs)

    if models.storage_type == "db":
        __tablename__ = 'locations'
        location_id = Column(Integer, primary_key=True, autoincrement=True)
        name = Column(String(100), nullable=False)
        address = Column(String(100), nullable=True)
        country = Column(String(50), nullable=True)
        city = Column(String(50), nullable=False)
        state = Column(String(50), nullable=True)
        zip_code = Column(String(10), nullable=True)
        ambulances = relationship("Ambulance", backref="location")
        hospitals = relationship("Hospital", backref="location")
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