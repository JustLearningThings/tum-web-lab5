import json

class Cache:
    def __init__(self) -> None:
        self.filename = 'cache.json'

    def get(self, key):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                
                return data[key] if key in data else None
        except FileNotFoundError:
            return {}
        
    def add(self, key, value):
        cache = {}

        with open(self.filename, 'r') as f:
            cache = json.load(f)
            print(cache)

        cache[key] = value

        with open(self.filename, 'w') as f:
            json.dump(cache, f)
    
    def has(self, key):
        with open(self.filename, 'r') as f:
            cache = json.load(f)

            return key in cache