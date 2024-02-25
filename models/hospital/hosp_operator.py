#! /usr/bin/env python
"""This is the Hospital Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Float,Enum
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


if models.storage_type == "db":
    hospital_topic = Table('hospital_topic', Base.metadata,
                            Column('hospitals_id', Integer,
                                ForeignKey('hospitals.id'),
                                primary_key=True,
                                nullable=False),
                            Column('health_topics_id', Integer,
                                ForeignKey('health_topics.id'),
                                primary_key=True,
                                nullable=False)
                            )
    hospital_alerts = Table('hospital_alerts', Base.metadata,
                            Column('hospitals_id', Integer,
                                ForeignKey('hospitals.id'),
                                primary_key=True,
                                nullable=False),
                            Column('alerts_id', Integer,
                                ForeignKey('alerts.id'),
                                primary_key=True,
                                nullable=False)
                            )
    staff_topic = Table('staff_topic', Base.metadata,
                        Column('hospital_staffs_id', Integer,
                            ForeignKey('hospital_staffs.id'),
                            primary_key=True,
                            nullable=False),
                        Column('health_topics_id', Integer,
                            ForeignKey('health_topics.id'),
                            primary_key=True,
                            nullable=False)
                        )

class HealthTopic(BaseModel, Base):
    """This is the Health Topic class"""
    if models.storage_type == "db":
        __tablename__ = 'health_topics'
        topic = Column(String(100), nullable=False)
        hospital_staff_id = Column(Integer, ForeignKey('hospital_staff.id'), nullable=False)
        message = Column(String(2000), nullable=False)
    else:
        topic = ""
        hospital_staff_id = ""
        message = ""


class HospitalStaff(BaseModel, Base):
    """This is the Hospital Staff class"""
    if models.storage_type == "db":
        __tablename__ = 'hospital_staff'
        full_name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True)
        phone = Column(String(20))
        hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)
        role = Column(String(100), nullable=False)
        health_topics = relationship("HealthTopic", secondary=staff_topic,
                                     viewonly=False)
    else:
        full_name = ""
        email = ""
        phone = ""
        hospital_id = ""
        role = ""
        health_topics = []

        @property
        def health_topics(self):
            """This method returns a list of all health topics
            for this staff member
            """
            if len(self.health_topics) > 0:
                return self.health_topics
            return None
        
        @health_topics.setter
        def health_topics(self, value):
            """This method sets the list of all health topics
            for this staff member
            """
            if value not in self.health_topics:
                self.health_topics = value


class Hospital(BaseModel, Base):
    """This is the Hospital Operator class"""
    if models.storage_type == "db":
        __tablename__ = 'hospitals'
        name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True)
        phone = Column(String(20))
        address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        status = Column(Enum('Active', 'Inactive'), default='Active')
        staff = relationship("HospitalStaff", backref="hospitals",
                                      cascade="all, delete-orphan")
        alerts = relationship("Alert", secondary=hospital_alerts,
                              backref="hospitals", cascade="all, delete-orphan")
    else:
        name = ""
        email = ""
        phone = ""
        address_id = ""
        status = ""
        latitude = ""
        longitude = ""
        available_staff = []
        current_allerts_alerts = []

        @property
        def staff(self):
            """This method returns a list of all hospitals"""
            if len(self.available_staff) > 0:
                return self.available_staff
            return None
        
        @property
        def alerts(self):
            """This method returns a list of all alerts"""
            if len(self.current_allerts_alerts) > 0:
                return self.current_allerts_alerts
            return None
        
        @staff.setter
        def staff(self, value):
            """This method sets the list of all hospitals"""
            if value not in self.available_staff:
                self.available_staff = value
        
        @alerts.setter
        def alerts(self, value):
            """This method sets the list of all alerts"""
            if value not in self.current_allerts_alerts:
                self.current_allerts_alerts = value

    def remove_staff(self, value):
        """This method removes a staff member from the list of all staff"""
        # TODO: Implement this method
        pass

    def accept_alert(self):
        """This method accepts an alert"""
        # TODO: Implement this method
        pass