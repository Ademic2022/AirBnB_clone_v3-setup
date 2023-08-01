#!/usr/bin/python3
"""This is the user class"""
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.place import Place
from models.review import Review
import hashlib


class User(BaseModel, Base):
    """This is the class for user
    Attributes:
        email: email address
        password: password for you login
        first_name: first name
        last_name: last name
    """

    __tablename__ = "users"
    __table_args__ = {"mysql_default_charset": "latin1"}
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", cascade="all, delete, delete-orphan",
                          backref="user")
    reviews = relationship(
        "Review", cascade="all, delete, delete-orphan", backref="user"
    )

    def __init__(self, *args, **kwargs):
        """Instantiation of User class.

        If 'password' is provided in kwargs, hash it using MD5 before saving.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if "password" in kwargs:
            kwargs["password"] = hashlib.md5(
                kwargs["password"].encode()).hexdigest()
        super().__init__(*args, **kwargs)

    def save(self):
        """Hash the password and save the user to the database."""
        if "password" in self.__dict__:
            self.password = hashlib.md5(self.password.encode()).hexdigest()
        super().save()
