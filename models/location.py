#! /usr/bin/python3
"""This is the Location module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Table
from sqlalchemy.orm import relationship


# This is the association table for the many-to-many relationship between
# locations and ambulances
if models.storage_type == "db":
    location_sites = Table('location_sites', Base.metadata,
                                Column('location_id', Integer,
                                    ForeignKey('locations.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('site_id', Integer,
                                    ForeignKey('sites.id'),
                                    primary_key=True,
                                    nullable=False)
                                )

    location_alerts = Table('location_alerts', Base.metadata,
                                Column('location_id', Integer,
                                    ForeignKey('locations.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('alert_id', Integer,
                                    ForeignKey('alerts.id'),
                                    primary_key=True,
                                    nullable=False)
                                )
    location_hospitals = Table('location_hospitals', Base.metadata,
                                Column('location_id', Integer,
                                    ForeignKey('locations.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('hospital_id', Integer,
                                    ForeignKey('hospitals.id'),
                                    primary_key=True,
                                    nullable=False)
                                )
    site_ambulances = Table('site_ambulances', Base.metadata,
                                Column('site_id', Integer,
                                    ForeignKey('sites.id'),
                                    primary_key=True,
                                    nullable=False),
                                Column('ambulance_id', Integer,
                                    ForeignKey('ambulances.id'),
                                    primary_key=True,
                                    nullable=False)
                                )

class Address(BaseModel, Base):
    """This is the Address class"""
    if models.storage_type == "db":
        __tablename__ = 'addresses'
        street = Column(String(100), nullable=False)
        city = Column(String(100), nullable=True)
        state = Column(String(100), nullable=False)
        zipcode = Column(String(100), nullable=False)
        country = Column(String(100), nullable=False)
    else:
        street = ""
        city = ""
        state = ""
        zipcode = ""
        country = ""


class Site(BaseModel, Base):
    """This is the Site class"""
    if models.storage_type == "db":
        __tablename__ = 'sites'
        address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        ambulances = relationship("Ambulance", secondary=site_ambulances,
                                    backref="site", cascade="all, delete-orphan", nullable=True)

    else:
        address_id = ""
        latitude = ""
        longitude = ""

        @property
        def ambulances(self):
            """This method returns a list of all ambulances at this site"""
            ambulances = models.storage.all()
            data =[]
            results = []
            for ambulance in ambulances.values():
                if ambulance.site_id == self.id:
                    data.append(ambulance)
            for ambulance in data:
                results.append(ambulance.to_dict())
            return results


class Location(BaseModel, Base):
    """This is the Location class"""
    if models.storage_type == "db":
        __tablename__ = 'locations'
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        radius = Column(Float, nullable=False)
        hospitals = relationship("Hospital", secondary=location_hospitals,
                                    backref="location", cascade="all, delete-orphan", nullable=True)
        sites = relationship("Site", secondary=location_sites,
                                backref="location", cascade="all, delete-orphan", nullable=True)
        alerts = relationship("Alert", secondary=location_alerts,
                                backref="location", cascade="all, delete-orphan", nullable=True)
    else:
        latitude = ""
        longitude = ""
        radius = ""
        active_hospitals = []
        active_sites = []
        active_alerts = []
        
        @property
        def sites(self):
            """This method returns a list of all sites at this location"""
            if len(self.active_sites) > 0:
                return self.active_sites
            return None
        
        @property
        def hospitals(self):
            """This method returns a list of all hospitals at this location"""
            if len(self.active_hospitals) > 0:
                return self.active_hospitals
            return None
        
        @property
        def alerts(self):
            """This method returns a list of all alerts at this location"""
            if len(self.active_alerts) > 0:
                return self.active_alerts
            return None
        
        @sites.setter
        def sites(self, value):
            """This method sets the list of all sites at this location"""
            if value not in self.active_sites:
                self.active_sites = value

        @hospitals.setter
        def hospitals(self, value):
            """This method sets the list of all hospitals at this location"""
            if value not in self.active_hospitals:
                self.active_hospitals = value

        @alerts.setter
        def alerts(self, value):
            """This method sets the list of all alerts at this location"""
            if value not in self.active_alerts:
                self.active_alerts = value