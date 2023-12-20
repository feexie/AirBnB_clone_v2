# file_storage.py
import json
from storage import Storage

class FileStorage(Storage):
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'

    def __init__(self, engine_url, file_path=__file_path):
        super().__init__(engine_url)
        self.__file_path = file_path

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is not None:
            filtered = {k: v for k, v in self.all().items() if isinstance(v, cls)}
            return filtered

        return self.all()

    def new(self, obj):
        """Adds new object to storage dictionary"""
        super().new(obj)
        self.save_to_file()

    def save_to_file(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            temp = {}
            for key, val in self.all().items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload_from_file(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    cls_name = val['__class__']
                    cls = eval(cls_name)
                    self.all()[key] = cls(**val)
        except FileNotFoundError:
            pass

    def reload(self):
        """Load data from both file and database"""
        super().reload()  # Load data from the database
        self.reload_from_file()  # Load data from file

    def save(self):
        """Commit all changes to both file and database"""
        super().save()  # Commit changes to the database
        self.save_to_file()  # Save changes to the file

    def delete(self, obj=None):
        """Deletes obj from both file and database"""
        super().delete(obj)
        self.save_to_file()

