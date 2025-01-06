#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None

    classes = [
            User,
            State,
            City,
            Amenity,
            Place,
            Review
        ]

    def __init__(self):
        """Initialize a new DBStorage instance."""
        username, passwd = getenv('HBNB_MYSQL_USER'), getenv('HBNB_MYSQL_PWD')
        host, db = getenv('HBNB_MYSQL_HOST'), getenv('HBNB_MYSQL_DB')
        env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(username,
                                             passwd,
                                             host,
                                             db),
                                      pool_pre_ping=True)

        if env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        This queries all objects on the current database session
        depending of the class name

        If cls is None, queries all types of objects.

        Args:
            cls: class whose objects are to be queried

        Return:
            Dictinary of queried classes in
            the format <class name>.<obj id> = obj.
        """
        dic = dict()
        # queries the class object passed as an argument
        if cls:
            objs = self.__session.query(cls).all()
            for obj in objs:
                dic[cls.__name__ + '.' + obj.id] = obj
            return dic

        # queries all class objects one after the other
        for cls_name in self.classes:
            objs = self.__session.query(cls_name).all()
            for obj in objs:
                dic[cls_name.__name__ + '.' + obj.id] = obj
        return dic

    def new(self, obj):
        """Adds the object to the current database session

        Args:
            obj: object to be added to the db
        """
        self.__session.add(obj)

    def save(self):
        """Commits all changes of the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes object from the current database session

        Args:
            obj: object to be deleted
        """
        if obj:
            self.__session.delete()

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)

        # create new session object from the engine
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)

        Session = scoped_session(session_factory)
        self.__session = Session()
