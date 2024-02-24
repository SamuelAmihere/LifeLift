#! /usr/bin/python3
"""This is the Driver module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.dialects.postgresql import ENUM
from models.hospital.hospital import Hospital


class Driver(BaseModel, Base):
    """This is the Driver class"""
    __tablename__ = 'drivers'
    driver_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    phone = Column(String(20))
    license_number = Column(String(50), unique=True)
    status = Column(Enum('Active', 'Inactive'), default='Active')