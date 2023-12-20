# file_storage.py
import json
from models.base_model import BaseModel

class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}
    __classes = {
        'BaseModel': 'BaseModel', 'User': 'User', 'Place': 'Place',
        'State': 'State', 'City': 'City', 'Amenity': 'Amenity',
        'Review': 'Review'
    }

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls != None:
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
        """Deserialize the JSON file to __objects (only if the JSON file exists)"""
        try:
            with open(FileStorage.__file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for key, value in data.items():
                class_name = key.split('.')[0]
                instance = eval("{}".format(class_name))(**value)
                storage.all()[key] = instance
        except FileNotFoundError:
            pass
        except Exception as e:
            pass

    def save(self):
        """Commit all changes to both file and database"""
        super().save()  # Commit changes to the database
        self.save_to_file()  # Save changes to the file

    def delete(self, obj=None):
        """Deletes obj from both file and database"""
        super().delete(obj)
        self.save_to_file()

