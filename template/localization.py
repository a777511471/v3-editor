import yaml



class Localization:
    def __init__(self, language):
        self.language = language
        self.map = {}

    def get_property(self, key):
        if key not in self.map:
            raise Exception(f"Key {key} not found in localization")
        return self.map[key]
    
    def __getitem__(self, key):
        return self.get_property(key)
    
    def load(self, base_path):
        pass
            
