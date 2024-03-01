#! /usr/bin/python3
"""This is the Ambulance Operator module"""
from sqlalchemy import Column, ForeignKey, String
import models
from sqlalchemy.orm import relationship
from models.base_model import Base, BaseModel


class AmbulanceOwner(BaseModel, Base):
    """This is the Ambulance Operator class"""
    if models.storage_type == "db":
        __tablename__ = 'operators'
        company_id = Column(String(60), ForeignKey('companies.id'),
                            nullable=False)
    else:
        company_id = ""