#! /usr/bin/env python3
"""This module contains the BaseModel class"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import uuid
from datetime import datetime
import models
from models import storage

Base = declarative_base()


class BaseModel:
    """This class is the base class for all other classes in this project"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(), nullable=False)

    def __init__(self, *args, **kwargs):
        """This method initializes a new instance of the BaseModel class"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if key != '__class__':
                    setattr(self, key, value)
            if 'id' not in kwargs:
                setattr(self, 'id', str(uuid.uuid4()))
            time = datetime.now()
            if 'created_at' not in kwargs:
                setattr(self, 'created_at', time)
            if 'updated_at' not in kwargs:
                setattr(self, 'updated_at', time)

    def __str__(self):
        """This method returns a string representation of the BaseModel instance"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    
    def save(self):
        """This method updates the updated_at attribute with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """This method returns a dictionary representation of the BaseModel instance"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']
        return new_dict
    
    def delete(self):
        """This method deletes the current instance from the storage"""
        models.storage.delete(self)

    def __repr__(self):
        """This method returns a string representation of the BaseModel instance"""
        return self.__str__()
    
    def __eq__(self, other):
        """This method checks if two instances of BaseModel are equal"""
        return self.id == other.id
    
    def __ne__(self, other):
        """This method checks if two instances of BaseModel are not equal"""
        return self.id != other.id
    
    def __lt__(self, other):
        """This method checks if one instance of BaseModel is less than another"""
        return self.id < other.id
    
    def __le__(self, other):
        """This method checks if one instance of BaseModel is less than or equal to another"""
        return self.id <= other.id
    
    def __gt__(self, other):
        """This method checks if one instance of BaseModel is greater than another"""
        return self.id > other.id
    
    def __ge__(self, other):
        """This method checks if one instance of BaseModel is greater than or equal to another"""
        return self.id >= other.id
    
    def __hash__(self):
        """This method returns the hash value of the BaseModel instance"""
        return hash(self.id)
    
    def __contains__(self, item):
        """This method checks if an item is in the BaseModel instance"""
        return item in self.__dict__
    
    def __len__(self):
        """This method returns the length of the BaseModel instance"""
        return len(self.__dict__)
    
    def __getitem__(self, key):
        """This method returns the value of a key in the BaseModel instance"""
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        """This method sets the value of a key in the BaseModel instance"""
        self.__dict__[key] = value

    def __delitem__(self, key):
        """This method deletes a key from the BaseModel instance"""
        del self.__dict__[key]

    def __iter__(self):
        """This method returns an iterator for the BaseModel instance"""
        return iter(self.__dict__)
    
    def __reversed__(self):
        """This method returns a reversed iterator for the BaseModel instance"""
        return reversed(self.__dict__)
    
    def __copy__(self):
        """This method returns a shallow copy of the BaseModel instance"""
        return self.__dict__.copy()
    
    def __deepcopy__(self, memo):
        """This method returns a deep copy of the BaseModel instance"""
        return self.__dict__.copy()
    
    def __contains__(self, item):
        """This method checks if an item is in the BaseModel instance"""
        return item in self.__dict__
    
    def __len__(self):
        """This method returns the length of the BaseModel instance"""
        return len(self.__dict__)
    
    def __getitem__(self, key):
        """This method returns the value of a key in the BaseModel instance"""
        return self.__dict__[key]
    
    def __setitem__(self, key, value):
        """This method sets the value of a key in the BaseModel instance"""
        self.__dict__[key] = value

    def __delitem__(self, key):
        """This method deletes a key from the BaseModel instance"""
        del self.__dict__[key]

    def __iter__(self):
        """This method returns an iterator for the BaseModel instance"""
        return iter(self.__dict__)