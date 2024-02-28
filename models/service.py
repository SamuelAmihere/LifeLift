#! /usr/bin/env python3
""" This module contains the Service class """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from models import storage_type
from models.review import Review, ReviewService


class Service(BaseModel, Base):
    """This is the Service class.
    It contains services provided by the system
    to patients
    """
    if storage_type == "db":
        __tablename__ = "services"
        status = Column(Enum('Pending', 'ongoing', 'Resolved', 'Cancelled'), default='Pending',
                        nullable=False)
        incident_id = Column(Integer, ForeignKey('incidents.id'),
                             nullable=True)
        ambulance_id = Column(Integer, ForeignKey('ambulances.id'),
                              nullable=True)
        request_time = Column(String(128), nullable=False)
        accepted_time = Column(String(128), nullable=True)
        dispatch_time = Column(String(128), nullable=True)
        arrival_time_pat = Column(String(128), nullable=True)
        arrival_time_hos = Column(String(128), nullable=True)
        reviews = relationship("ReviewService", backref="services", cascade="all, delete")
    else:
        service_type = ""
        status = ""
        incident_id = ""
        Patient_id = ""
        ambulance_id = ""
        request_time = ""
        accepted_time = ""
        dispatch_time = ""
        arrival_time_pat = ""
        arrival_time_hos = ""
        all_reviews = []
        @property
        def reviews(self):
            """Getter for reviews"""
            for rev in models.storage.all("ReviewService").values():
                if rev.service_id == self.id and rev not in self.all_reviews:
                    self.all_reviews.append(rev)
            return self.all_reviews

        @reviews.setter
        def reviews(self, value):
            """Setter for reviews"""
            if type(value) == str and value not in self.all_reviews:
                self.all_reviews.append(value)