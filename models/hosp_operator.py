#! /usr/bin/env python
"""This is the Hospital Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.orm import relationship
from models.company import Company
from models.system_user import Staff
from models.location import location_hospitals

class HealthTopic(BaseModel, Base):
    """This is the Health Topic class"""
    if models.storage_type == "db":
        __tablename__ = 'health_topics'
        topic = Column(String(100), nullable=False)
    else:
        topic = ""


class StaffMessage(BaseModel, Base):
    """This is the Health Topic message class"""
    if models.storage_type == "db":
        __tablename__ = 'staff_messages'
        health_topic_id = Column(String(60), ForeignKey('health_topics.id'),
                                 nullable=False)
        staff_id = Column(String(60), ForeignKey('hospital_staff.id'),
                          nullable=False)
        message = Column(String(2000), nullable=False)


class HospitalStaff(Staff):
    """This is the Hospital Staff class"""
    if models.storage_type == "db":
        __tablename__ = 'hospital_staff'
        health_messages = relationship("StaffMessage",
                                       backref="hospital_staff")
    else:
        health_messages = []

        @property
        def health_messages(self):
            """This method returns a list of all health messages
            for this staff member
            """
            if len(self.health_messages) > 0:
                return self.health_messages
            return None

        @health_messages.setter
        def health_messages(self, value):
            """This method sets the list of all health messages
            for this staff member
            """
            if value not in self.health_messages:
                self.health_messages = value


class Hospital(Company):
    """This is the Hospital Operator class"""
    if models.storage_type == "db":
        __tablename__ = 'hospitals'
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        alerts = relationship("Alert", backref="hospital",
                              cascade="all, delete-orphan",
                              nullable=True)
        locations = relationship(location_hospitals, backref="hospital_staff")
    else:
        latitude = ""
        longitude = ""
        active_alerts = []
        current_locations = []

        @property
        def alerts(self):
            """This method returns a list of all alerts"""
            if len(self.active_alerts) > 0:
                return self.active_alerts
            return None
        @property
        def locations(self):
            """This method returns a list of all temporal locations
            the hospital is in
            """
            if len(self.current_locations) > 0:
                return self.current_locations
            return None

        @alerts.setter
        def alerts(self, value):
            """This method sets the list of all alerts"""
            if type(value) == str and value not in self.active_alerts:
                self.alerts.append(value)

        @locations.setter
        def locations(self, value):
            """This method sets the list of all alerts"""
            if type(value) == str and value not in self.current_locations:
                self.current_locations.append(value)

    def accept_alert(self):
        """This method accepts an alert"""
        # TODO: Implement this method
        pass