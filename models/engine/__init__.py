from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models.base_model import Base
storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()

