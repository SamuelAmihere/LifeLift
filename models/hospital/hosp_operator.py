#! /usr/bin/env python
"""This is the Hospital Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.hospital.hospital import Hospital
from models.ambulance.ambulance import Ambulance


class HealthTopic(BaseModel, Base):
    """This is the Health Topic class"""
    __tablename__ = 'health_topics'
    topic_id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    message = Column(String(100), nullable=False)


class HospitalStaff(BaseModel, Base):
    """This is the Hospital Staff class"""
    __tablename__ = 'hospital_staff'
    staff_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    hospital_id = Column(Integer, ForeignKey('hospitals.hospital_id'), nullable=False)
    role = Column(String(100), nullable=False)


class Hospital(BaseModel, Base):
    """This is the Hospital Operator class"""
    __tablename__ = 'hospitals'
    hosp_owner_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    address_id = Column(Integer, ForeignKey('addresses.address_id'), nullable=False)

    status = Column(Enum('Active', 'Inactive'), default='Active')
    incoming = Column(ENUM('True', 'False'), default='False')

    if models.storage_type != "db":
        hospitals = relationship("Hospital", backref="hospitals",
                              cascade="all, delete-orphan")
    else:
        @property
        def hospitals(self):
            """This method returns a list of all hospitals
            owned by this operator
            """
            hospitals = models.storage.all(Hospital)
            data = []
            results = []
            for hospital in hospitals:
                if hospital.hosp_owner_id == self.id:
                    data.append(hospital)
            for hospital in data:
                results.append(hospital.to_dict())
            return results