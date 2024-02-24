#! /usr/bin/python3
"""This is the Ambulance module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.location import Location, location_ambulance
from models.patient import Patient, ambulance_patient
from models.ambulance.ambu_operator import AmbulanceOwner
from models.ambulance.ambu_operator import AmbulanceStaff
from models.driver import Driver
from sqlalchemy import Table
from models.patient import Patient

# This is the association table for the many-to-many relationship between
# patients and ambulances
ambulance_patient = Table('ambulance_patient', Base.metadata,
                                Column('ambulance_id', Integer,
                                           ForeignKey('ambulances.ambulance_id'),
                                           primary_key=True,
                                           nullable=False),
                                Column('patient_id', Integer,
                                           ForeignKey('patients.patient_id'),
                                           primary_key=True,
                                           nullable=False)
                        )


class Ambulance(BaseModel, Base):
    """This is the Ambulance class"""
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
    locations_ambulances = relationship("Location",
                                        secondary=location_ambulance)