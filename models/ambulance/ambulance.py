#! /usr/bin/python3
"""This is the Ambulance module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship


class Ambulance(BaseModel, Base):
    """This is the Ambulance class"""
    if models.storage_type == "db":
        __tablename__ = 'ambulances'
        ambulance_id = Column(Integer, primary_key=True, autoincrement=True)
        registration_number = Column(String(20), nullable=False)
        model = Column(String(50))
        capacity = Column(Integer, nullable=True)
        status = Column(Enum('Available', 'Busy', 'Out of Service'),
                        default='Available')
        driver_id = Column(Integer, ForeignKey('drivers.driver_id'),
                        nullable=True)
        ambu_owner_id = Column(Integer, ForeignKey('ambulance_owners.ambu_owner_id'),
                                    nullable=False)
        site_id = Column(Integer, ForeignKey('locations.location_id'),
                        nullable=False)
    else:
        registration_number = ""
        model = ""
        capacity = 0
        status = ""
        driver_id = ''
        ambu_owner_id = 0
        site_id = 0