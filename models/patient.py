#! /usr/bin/python3
"""This is the Patient module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.ambulance.ambulance import ambulance_patient


class Patient(BaseModel, Base):
    """This is the Patient class"""
    __tablename__ = 'patients'
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    status = Column(Enum('Active', 'Inactive'), default='Active')
    patient_ambulances = relationship("Ambulance", secondary=ambulance_patient, nullable=True)