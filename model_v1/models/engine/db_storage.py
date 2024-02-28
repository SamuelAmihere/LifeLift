#! /usr/bin/env python3
"""This module contains the DBStorage class"""
from os import getenv
from models.base_model import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.ambulance import Ambulance
from models.hospital import Hospital
from models.location import Location
from models.patient import Patient
from models.incident import Incident
from dotenv import load_dotenv

load_dotenv()


class DBStorage:
    """ This class is the storage engine for the project """
    __engine = None
    __session = None

    def __init__(self):
        """ This method initializes a new instance of the DBStorage class """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('LFTLIFT_MYSQL_USER'),
                                                getenv('LFTLIFT_MYSQL_PWD'),
                                                getenv('LFTLIFT_MYSQL_HOST'),
                                                getenv('LFTLIFT_MYSQL_DB')),
                                      pool_pre_ping=True)

        if getenv('LFTLIFT_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ This method returns a dictionary of all instances of a class """
        classes = [User, Ambulance, Hospital, Location, Patient, Incident]
        new_dict = {}
        if cls:
            for obj in self.__session.query(cls):
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                new_dict[key] = obj
        else:
            for c in classes:
                for obj in self.__session.query(c):
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    new_dict[key] = obj
        return new_dict
    
    def new(self, obj):
        """ This method adds a new instance to the session """
        self.__session.add(obj)

    def save(self):
        """ This method commits all changes to the database """
        self.__session.commit()

    def delete(self, obj=None):
        """ This method deletes an instance from the session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ This method creates all tables in the database """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ This method closes the session """
        self.__session.close()

    def get(self, cls, id):
        """ This method retrieves an instance from the session """
        return self.__session.query(cls).get(id)
    
    def count(self, cls=None):
        """ This method returns the number of instances of a class """
        if cls:
            return self.__session.query(cls).count()
        else:
            classes = [User, Ambulance, Hospital, Location, Patient, Incident]
            count = 0
            for c in classes:
                count += self.__session.query(c).count()
            return count
        
    def get_all(self, cls):
        """ This method returns a list of all instances of a class """
        return self.__session.query(cls).all()
    
    def get_first(self, cls):
        """ This method returns the first instance of a class """
        return self.__session.query(cls).first()
    
    def get_last(self, cls):
        """ This method returns the last instance of a class """
        return self.__session.query(cls).order_by(cls.id.desc()).first()
    
    def get_by(self, cls, **kwargs):
        """ This method returns the first instance of a class that meets the criteria """
        return self.__session.query(cls).filter_by(**kwargs).first()
    
    def get_all_by(self, cls, **kwargs):
        """ This method returns a list of all instances of a class that meet the criteria """
        return self.__session.query(cls).filter_by(**kwargs).all()
    
    def get_count_by(self, cls, **kwargs):
        """ This method returns the number of instances of a class that meet the criteria """
        return self.__session.query(cls).filter_by(**kwargs).count()
    
    def get_all_by_order(self, cls, order):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order).all()
    
    def get_all_by_order_desc(self, cls, order):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order.desc()).all()
    
    def get_all_by_order_by(self, cls, order, by):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order).order_by(by).all()
    
    def get_all_by_order_by_desc(self, cls, order, by):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order.desc()).order_by(by.desc()).all()
    
    def get_all_by_order_by_order(self, cls, order, by, order2):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order).order_by(by).order_by(order2).all()
    
    def get_all_by_order_by_order_desc(self, cls, order, by, order2):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order.desc()).order_by(by.desc()).order_by(order2.desc()).all()
    
    def get_all_by_order_by_order_by(self, cls, order, by, order2, by2):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order).order_by(by).order_by(order2).order_by(by2).all()
    
    def get_all_by_order_by_order_by_desc(self, cls, order, by, order2, by2):
        """ This method returns a list of all instances of a class in a specific order """
        return self.__session.query(cls).order_by(order.desc()).order_by(by.desc()).order_by(order2.desc()).order_by(by2.desc()).all()