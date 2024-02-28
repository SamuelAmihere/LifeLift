#! /usr/bin/python3
"""This is the Patient module"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from models import storage_type


class Patient_119(BaseModel, Base):
    """This is the Patient class"""
    if storage_type == "db":
        __tablename__ = 'patients'
        full_name = Column(String(100), nullable=False)
        email = Column(String(100), unique=True)
        phone = Column(String(20), nullable=True)
        address_id = Column(Integer, ForeignKey('addresses.id'), nullable=False)
        relative_phone = Column(String(20), nullable=True)
    else:
        full_name = ""
        email = ""
        phone = ""
        address_id = ""
        relative_phone = ""