# /home/yusuf/alx/AirBnB_clone_v2/models/engine/storage.py

class Storage:
    """This class defines the storage engine for HBNB"""

    __engine = None
    __session = None

    def __init__(self):
        """Creates the engine and session to interact with the database"""
        self.reload()

    @property
    def get(self):
        """Returns the current storage engine"""
        return self.__engine

    @property
    def get_session(self):
        """Returns the current session"""
        return self.__session

    def reload(self):
        """Create all tables in the database and create the current
        database session from the engine
        """
        from sqlalchemy.orm import sessionmaker, scoped_session
        from models.base_model import Base

        if "HBNB_MYSQL_USER" in environ and "HBNB_MYSQL_PWD" in environ and \
                "HBNB_MYSQL_HOST" in environ and "HBNB_MYSQL_DB" in environ:
            user = environ["HBNB_MYSQL_USER"]
            pwd = environ["HBNB_MYSQL_PWD"]
            host = environ["HBNB_MYSQL_HOST"]
            db = environ["HBNB_MYSQL_DB"]
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                          format(user, pwd, host, db),
                                          pool_pre_ping=True)
        else:
            self.__engine = create_engine('sqlite:///:memory:')

        if environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = Session()

    def all(self, cls=None):
        """Query on the current database session"""
        from models.base_model import BaseModel

        if cls is not None:
            return self.__session.query(cls).all()

        classes = [BaseModel]
        objs = []
        for cls in classes:
            objs.extend(self.__session.query(cls).all())
        return {obj.__class__.__name__ + '.' + obj.id: obj for obj in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

