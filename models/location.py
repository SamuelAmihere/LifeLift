#! /usr/bin/python3
"""This is the Location module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Float, Table
from sqlalchemy.orm import relationship

# This is the association table for the many-to-many relationship
# between locations and ambulances
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

    site_alerts = Table('site_alerts', Base.metadata,
                                Column('site_id', Integer,
                                    ForeignKey('sites.id'),
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
        address_id = Column(Integer, ForeignKey('addresses.id'),
                            nullable=False)
        location_id = Column(String(60), ForeignKey('locations.id'), nullable=False)
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        ambulances = relationship("Ambulance", backref="site",
                                    nullable=True)
        alerts = relationship("Alert", secondary=site_alerts,
                                viewonly=False, nullable=True)
        locations = relationship(location_sites, backref="sites")
    else:
        address_id = ""
        latitude = ""
        longitude = ""
        active_ambulances = []
        active_alerts = []
        current_locations = []

        @property
        def ambulances(self):
            """This method returns a list of all ambulances at 
            this site
            """
            for ambu in models.storage.all("Ambulance").values():
                if ambu.site_id == self.id and ambu not in self.active_ambulances:
                    self.active_ambulances.append(ambu)
            return self.active_ambulances

        @property
        def alerts(self):
            """This method returns a list of all alerts at this
            site
            """
            for alert in models.storage.all("Alert").values():
                if self.id in alert.sites and alert not in self.active_alerts:
                    self.active_alerts.append(alert)
            return self.active_alerts

        @property
        def locations(self):
            """This method returns a list of all temporal locations
            at this site
            """
            for loc in models.storage.all("Location").values():
                if self.id in loc.sites and loc not in self.current_locations:
                    self.current_locations.append(loc)
            return self.current_locations

        @ambulances.setter
        def ambulances(self, value):
            """This method sets a list of all ambulances at 
            this site
            """
            if type(value) == str and value not in self.active_ambulances:
                self.active_ambulances.append(value)

        @alerts.setter
        def alerts(self, value):
            """This method sets the list of all alerts at this
            site
            """
            if type(value) == str and value not in self.active_alerts:
                self.active_alerts.append(value)
        
        @locations.setter
        def locations(self, value):
            """This method sets the list of all temporal locations
            at this site
            """
            if type(value) == str and value not in self.current_locations:
                self.current_locations.append(value)


class Location(BaseModel, Base):
    """This is the Location class"""
    if models.storage_type == "db":
        __tablename__ = 'locations'
        latitude = Column(Float, nullable=False)
        longitude = Column(Float, nullable=False)
        radius = Column(Float, nullable=False)
        hospitals = relationship("Hospital",
                                    backref="location", 
                                    nullable=True)
        sites = relationship("Site", secondary=location_sites,
                                viewonly=False, backref="location")
    else:
        latitude = ""
        longitude = ""
        radius = ""
        active_hospitals = []
        active_sites = []

        @property
        def sites(self):
            """This method returns a list of all sites at this
            location
            """
            for site in models.storage.all("Site").values():
                if self.id in site.locations and site not in self.active_sites:
                    self.active_sites.append(site)
            return self.active_sites
        
        @property
        def hospitals(self):
            """This method returns a list of all hospitals at
            this location
            """
            for hosp in models.storage.all("Hospital").values():
                if self.id in hosp.locations and hosp not in self.active_hospitals:
                    self.active_hospitals.append(hosp)
            return self.active_hospitals

        @hospitals.setter
        def hospitals(self, value):
            """This method sets the list of all hospitals at this
            location
            """
            if type(value) == str and value not in self.active_hospitals:
                self.active_hospitals.append(value)

        @sites.setter
        def sites(self, value):
            """This method sets the list of all sites at this
            location
            """
            if type(value) == str and value not in self.active_sites:
                self.active_sites.append(value)