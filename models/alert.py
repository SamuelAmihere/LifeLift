#! /usr/bin/env python3
"""This module contains the Alert class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import storage_type


class Alert(BaseModel, Base):
    """This is the Alert class"""
    if storage_type == "db":
        __tablename__ = 'alerts'
        alert_type = Column(String(100), nullable=False)
        alert_status = Column(Enum('comfirmed', 'pending', 'resolved'), nullable=False)
        hospital_id = Column(String(60), ForeignKey('hospitals.id'),
                             nullable=False)
        incident_id = Column(String(60), ForeignKey('incidents.id'),
                             nullable=False)
        site_id = Column(String(60), ForeignKey('sites.id'), nullable=False)
        hospital = relationship("Hospital", back_populates="alerts", cascade="delete")
        site = relationship("Site", back_populates="alerts")
        incident = relationship("Incident", back_populates="alerts", cascade="delete")
    else:
        incident_id = ""
        alert_type = ""
        alert_status = ""
        alerts_locations = []

        @property
        def locations(self):
            """This method returns a list of all locations associated
            with this alert
            """
            if len(self.alerts_locations) > 0:
                return self.alerts_locations

        @locations.setter
        def locations(self, value):
            """This method sets the locations associated with this alert"""
            if value not in self.alerts_locations:
                self.alerts_locations.append(value)