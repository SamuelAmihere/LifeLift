#! /usr/bin/python3
"""This is the Ambulance module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from models.incident import incident_ambulances


class Ambulance(BaseModel, Base):
    """This is the Ambulance class"""
    if models.storage_type == "db":
        __tablename__ = 'ambulances'
        registration_number = Column(String(20), nullable=False)
        site_id = Column(Integer, ForeignKey('sites.id'),nullable=False)
        model = Column(String(50))
        capacity = Column(Integer, nullable=True, default=0)
        status = Column(Enum('Available', 'Busy', 'Out of Service'),
                        default='Available')
        operator_id = Column(Integer, ForeignKey('operators.id'),
                               nullable=False)
        staff = relationship("Staff", secondary="ambulance_staff",
                             back_populates="ambulances", nullable=True)
        incidents = relationship(incident_ambulances, backref="ambulances",
                                 nullable=True)
    else:
        registration_number = ""
        model = ""
        capacity = 0
        status = ""
        ambu_owner_id = 0
        staff = []

        @property
        def staff(self):
            """Getter for staff"""
            if len(self.staff) > 0:
                return self.staff
            return None
        
        @staff.setter
        def staff(self, value):
            """Setter for staff"""
            if value not in self.staff:
                self.staff.append(value)