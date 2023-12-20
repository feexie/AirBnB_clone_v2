# storage.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class Storage:
    """This class provides common storage functionality."""
    def __init__(self, engine_url):
        self.__engine = create_engine(engine_url, pool_pre_ping=True)
        self.__session = None

    def all(self, cls=None):
        if cls is not None:
            return self.__session.query(cls).all()
        # Your existing logic for getting all objects

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

