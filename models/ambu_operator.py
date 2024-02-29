#! /usr/bin/python3
"""This is the Ambulance Operator module"""
import models
from sqlalchemy.orm import relationship
from models.company import Company


class AmbulanceOwner(Company):
    """This is the Ambulance Operator class"""
    if models.storage_type == "db":
        __tablename__ = 'operators'
    else:
        pass