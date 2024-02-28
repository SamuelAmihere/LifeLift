#! /usr/bin/env python3
""" This module contains the Service class """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from models import storage_type
from models.review import Review, ReviewService

if storage_type == "db":
    Service_reviews = Table('service_review', Base.metadata,
                            Column('service_id', Integer,
                                    ForeignKey('services.id'),
                                    primary_key=True,
                                    nullable=False),
                            Column('review_id', Integer,
                                    ForeignKey('reviews.id'),
                                    primary_key=True,
                                    nullable=False)
                            )


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
        reviews = relationship("Review", secondary=Service_reviews,
                               back_populates="services", nullable=True)
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
        reviews = []
        @property
        def reviews(self):
            """Getter for reviews"""
            if len(self.reviews) > 0:
                return self.reviews
            return None

        @reviews.setter
        def reviews(self, value: ReviewService):
            """Setter for reviews"""
            if type(value) == Review and value not in self.reviews:
                self.reviews.append(value)