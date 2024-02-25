#! /usr/bin/env python3
"""This module contains the Alert class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models import storage_type
import models
from models.system_user import SystemUser
from models.hospital.hosp_operator import Hospital
from models.ambulance.ambulance import Ambulance
from models.patient import Patient
from models.review import Review
from models.review import Review
from datetime import datetime

if storage_type == "db":
    alert_patient = Table('alert_patient', Base.metadata,
                            Column('alert_id', Integer,
                                    ForeignKey('alerts.id'),
                                    primary_key=True,
                                    nullable=False),
                            Column('patient_id', Integer,
                                    ForeignKey('patients.id'),
                                    primary_key=True,
                                    nullable=False)
                            )


class Alert(BaseModel, Base):
    """This is the Alert class"""
    if storage_type == "db":
        __tablename__ = 'alerts'
        hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)
        ambulance_id = Column(Integer, ForeignKey('ambulances.id'), nullable=False)
        alert_type = Column(String(100), nullable=False)
        alert_status = Column(Enum('comfirmed', 'pending', 'resolved'), nullable=False)
        patients = relationship("Patient", secondary=alert_patient,
                               viewonly=False)
    else:
        hospital_id = ""
        ambulance_id = ""
        alert_type = ""
        alert_time = ""
        alert_status = ""
        patients = []

        @property
        def patients(self):
            """This method returns a list of all patients associated with this alert"""
            if len(self.patients) > 0:
                return self.patients