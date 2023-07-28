#!/usr/bin/python3
""" new class for sqlAlchemy """
import models
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import (create_engine)
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """ create tables in environmental"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        passwd = getenv("HBNB_MYSQL_PWD")
        db = getenv("HBNB_MYSQL_DB")
        host = getenv("HBNB_MYSQL_HOST")
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        dic = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            query = self.__session.query(cls)
            for elem in query:
                key = "{}.{}".format(type(elem).__name__, elem.id)
                dic[key] = elem
        else:
            lista = [State, City, User, Place, Review, Amenity]
            for clase in lista:
                query = self.__session.query(clase)
                for elem in query:
                    key = "{}.{}".format(type(elem).__name__, elem.id)
                    dic[key] = elem
        return (dic)

    def new(self, obj):
        """add a new element in the table
        """
        self.__session.add(obj)

    def save(self):
        """save changes
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete an element in the table
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """configuration
        """
        Base.metadata.create_all(self.__engine)
        sec = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sec)
        self.__session = Session()

    def close(self):
        """ calls remove()
        """
        self.__session.close()

    def get(self, cls, id):
        '''
            Retrieve an obj w/class name and id
        '''
        result = None
        try:
            cls_object = getattr(models, cls)
            objs = self.__session.query(cls_object).all()
            for obj in objs:
                if obj.id == id:
                    result = obj
                    break
        except Exception as e:
            print("Error:", e) #  this line is added to see exceptions raised
        return result

    def count(self, cls=None):
        '''
            Count num objects in DBstorage
        '''
        cls_counter = 0

        if cls is not None:
            cls_obj = getattr(models, cls)
            objs = self.__session.query(cls_obj).all()
            cls_counter = len(objs)
        else:
            for k, v in models.__dict__.items():
                if k != "BaseModel":
                    cls_obj = getattr(models, k)
                    objs = self.__session.query(cls_obj).all()
                    cls_counter += len(objs)
        return cls_counter
