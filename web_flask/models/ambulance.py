#! /usr/bin/python3
"""This is the Ambulance module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from models.location import Location
from models.driver import Driver


class Ambulance(BaseModel, Base):
    """This is the Ambulance class"""
    def __init__(self, *args, **kwargs):
        """This method initializes a new instance of the Ambulance class"""
        super().__init__(*args, **kwargs)
    
    if models.storage_type == "db":
        __tablename__ = 'ambulances'
        ambulance_id = Column(Integer, primary_key=True, autoincrement=True)
        registration_number = Column(String(20), nullable=False)
        model = Column(String(50))
        make = Column(String(50))
        capacity = Column(Integer)
        status = Column(Enum('Available', 'Busy', 'Out of Service'), default='Available')
        location_id = Column(Integer, ForeignKey('locations.location_id'))
        driver_id = Column(Integer, ForeignKey('drivers.driver_id'), nullable=True)

    else:
        registration_number = ""
        model = ""
        make = ""
        capacity = 0
        status = "Available"
        location_id = ""
        driver_id = ""

    def assign_driver(self, driver):
        """This method assigns a driver to the ambulance"""
        self.driver_id = driver.driver_id
        models.storage.save()

    def unassign_driver(self):
        """This method unassigns a driver from the ambulance"""
        self.driver_id = None
        models.storage.save()



# Path: web_flask/models/ambulance.py
# Compare this snippet from web_flask/models/base_model.py:
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, DateTime
# import uuid
# from datetime import datetime
# import models
# from models import storage
#
# Base = declarative_base()

# class BaseModel:
#     """This class is the base class for all other classes in this project"""
#     id = Column(String(60), primary_key=True, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
#     updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

#     def __init__(self, *args, **kwargs):
#         """This method initializes a new instance of the BaseModel class"""
#         if kwargs:
#             for key, value in kwargs.items():
#                 if key == 'created_at' or key == 'updated_at':
#                     value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
#                 if key != '__class__':
#                     setattr(self, key, value)
#             if 'id' not in kwargs:
#                 setattr(self, 'id', str(uuid.uuid4()))
#             time = datetime.now()
#             if 'created_at' not in kwargs:
#                 setattr(self, 'created_at', time)
#             if 'updated_at' not in kwargs:
#                 setattr(self, 'updated_at', time)

#     def __str__(self):
#         """This method returns a string representation of the BaseModel instance"""
#         return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
#     def save(self):
#         """This method updates the updated_at attribute with the current datetime"""
#         self.updated_at = datetime.now()
#         models.storage.new(self)
#         models.storage.save()

#     def to_dict(self):
#         """This method returns a dictionary representation of the BaseModel instance"""
#         new_dict = self.__dict__.copy()
#         new_dict['__class__'] = self.__class__.__name__
#         new_dict['created_at'] = self.created_at.isoformat()
#         new_dict['updated_at'] = self.updated_at.isoformat()
#         if '_sa_instance_state' in new_dict:
#             del new_dict['_sa_instance_state']
#         return new_dict
    
#     def delete(self):
#         """This method deletes the current instance from the storage"""
#         models.storage.delete(self)
