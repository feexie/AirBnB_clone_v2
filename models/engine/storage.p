from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

class Storage:
    """This class provides common storage functionality."""
    def __init__(self, engine_url=None):
        if engine_url:
            self.__engine = create_engine(engine_url, pool_pre_ping=True)
            Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
            self.__session = Session()
        else:
            self.__engine = None
            self.__session = None

    def all(self, cls=None):
        if cls:
            return self.__session.query(cls).all()
        else:
            # Handle case when using FileStorage or no specific class is provided
            # Use your existing logic for getting all objects in FileStorage

    def new(self, obj):
        if self.__session:
            self.__session.add(obj)

    def save(self):
        if self.__session:
            self.__session.commit()

    def delete(self, obj=None):
        if self.__session and obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        if self.__session:
            self.__session.close()
        if self.__engine:
            Base.metadata.create_all(self.__engine)
            Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
            self.__session = Session()

