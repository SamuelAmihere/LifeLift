#! /usr/bin/env python3
"""
This module contains the Incident class
"""
from enum import Enum
from models.base_model import BaseModel
from models.patient import Patient_119 as Patient
from models.ambulance.ambulance import Ambulance
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table
import models
from models.base_model import Base

if models.storage_type == "db":
    incident_patients = Table('incident_patient', Base.metadata,
                                Column('incident_id', Integer,
                                    ForeignKey('incidents.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('patient_id', Integer,
                                    ForeignKey('patients.id'),
                                    primary_key=True,
                                    nullable=False)
                                )
    incident_ambulances = Table('incident_ambulance', Base.metadata,
                                Column('incident_id', Integer,
                                    ForeignKey('incidents.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('ambulance_id', Integer,
                                    ForeignKey('ambulances.id'),
                                    primary_key=True,
                                    nullable=False)
                                )


class Incident(BaseModel, Base):
    """This is the Incident class"""

    if models.storage_type == "db":

       __tablename__ = 'incidents'
       incident_type = Column(String(50), nullable=False)
       latitude = Column(Float, nullable=False)
       longitude = Column(Float, nullable=False)
       incident_status = Column(Enum('Pending', 'Resolved', 'Cancelled'),
                                   default='Pending')
       incident_description = Column(String(100), nullable=False)
       patients = relationship("Patient", secondary=incident_patients)
       ambulances = relationship("Ambulance", secondary=incident_ambulances, nullable = True)
    else:
       incident_type = ""
       latitude = 0.0
       longitude = 0.0
       incident_status = ""
       incident_description = ""
       patients = []
       ambulances = []
       @property
       def patients(self):
           """Getter for patients"""
           if len(self.patients) > 0:
               return self.patients
           return None
       @property
       def ambulances(self):
           """Getter for ambulances"""
           if len(self.ambulances) > 0:
               return self.ambulances
           return None
       
       @patients.setter
       def patients(self, value):
           """Setter for patients"""
           if isinstance(value, Patient) and value not in self.patients:
               self.patients.append(value)

       @ambulances.setter
       def ambulances(self, value):
           """Setter for ambulances"""
           if isinstance(value, Ambulance) and value not in self.ambulances:
               self.ambulances.append(value)