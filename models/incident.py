#! /usr/bin/env python3
"""
This module contains the Incident class
"""
from datetime import datetime
from models.base_model import BaseModel
from models.patient import Patient
from models.ambulance.ambulance import Ambulance
from models.location import Location
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import Table
import models
from models.base_model import Base


class Incident(BaseModel, Base):
    """This is the Incident class"""
    __tablename__ = 'incidents'
    incident_id = Column(Integer, primary_key=True, autoincrement=True)
    incident_type = Column(String(50), nullable=False)
    incident_date = Column(DateTime, default=datetime.now())
    incident_location = Column(Integer, ForeignKey('locations.location_id'),
                               nullable=False)
    incident_status = Column(ENUM('Pending', 'Resolved', 'Cancelled'),
                             default='Pending')
    incident_description = Column(String(100), nullable=False)
    incident_patients = relationship("Patient", secondary=Table('incident_patient',
                                                               Base.metadata,
                                                               Column('incident_id',
                                                                      Integer,
                                                                      ForeignKey('incidents.incident_id'),
                                                                      primary_key=True,
                                                                      nullable=False),
                                                               Column('patient_id',
                                                                      Integer,
                                                                      ForeignKey('patients.patient_id'),
                                                                      primary_key=True,
                                                                      nullable=False)
                                                               )
                                    )
    incident_ambulances = relationship("Ambulance", secondary=Table('incident_ambulance',
                                                                   Base.metadata,
                                                                   Column('incident_id',
                                                                          Integer,
                                                                          ForeignKey('incidents.incident_id'),
                                                                          primary_key=True,
                                                                          nullable=False),
                                                                   Column('ambulance_id',
                                                                          Integer,
                                                                          ForeignKey('ambulances.ambulance_id'),
                                                                          primary_key=True,
                                                                          nullable=False)
                                                                   )
                                      )
    incident_location = relationship("Location", back_populates="incidents")