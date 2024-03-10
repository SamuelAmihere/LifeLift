#! /usr/bin/env python
"""This is the Contact module"""
import models
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Contact(BaseModel, Base):
    """This is the Contact class"""
    fields_errMSG = {
        'email': 'Missing email',
        'phone': 'Missing phone_number',
        # to create address
        'street': 'Missing street',
        'city': 'Missing city',
        'state': 'Missing state',
        'zipcode': 'Missing zipcode',
        'country': 'Missing country',
    }
    if models.storage_type == "db":
        __tablename__ = 'contacts'
        email = Column(String(100), nullable=True)
        phone_number = Column(String(100), nullable=True)
        address_id = Column(String(60), ForeignKey('addresses.id'),
                            nullable=False)
        address = relationship("Address", back_populates="contacts")
    else:
        email = ""
        phone_number = ""
        address_id = ""