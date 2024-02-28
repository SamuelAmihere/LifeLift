#! /usr/bin/python3
"""This is the Ambulance Operator module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from models.company import Company
from system_user import Staff


class AmbulanceOwner(Company):
    """This is the Ambulance Operator class"""
    if models.storage_type == "db":
        __tablename__ = 'operators'
    else:
        pass