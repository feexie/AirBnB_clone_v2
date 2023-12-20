#!/usr/bin/python3
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """dbstorage class"""
    engine = None
    session = None

    def __init__(self):
        envi = getenv('HBNB_ENV')
        usr = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}' \
                                    .format(usr, pwd, host, db), echo=False, pool_pre_ping=True)

        if envi == 'test':
            Base.metadata.drop_all(self.__engine)
        
    def all(self, cls=None):
        """all"""
        dict = {}
        classes = [User, State, City, Amenity, Place, Review]
        if cls is None:
            for item in classes:
                q = self.__session.query(item)
                for i in q.all():
                    key = '{}.{}'.format(type(i).__name__, i.id)
                    dict[key] = i
        else:
            if cls is str:
                cls = eval(cls)
            q = self.__session.query(cls)
            for item in q.all():
                key = '{}.{}'.format(type(item).__name__, item.id)
                dict[key] = item 
        return (dict)
    
    def new(self, obj):
        """adds new object to session"""
        self.__session.add(obj)
        
    def save(self):
        """"commit all changes """
        self.__session.commit()
    
    def delete(self, obj=None):
        """delete obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            
    def reload(self):
        """create all tables """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """close"""
        self.__session.close()
