# write your CIDict here
# Used generative AI to get back into the flow of the definitions and structures of classes

class CIDict(dict):     # Subclass of dict
    def __init__(self, **kwargs):
        dict.__init__(self)
        for key, value in kwargs.items():       # Initializing all values
            self[key] = value

    def __setitem__(self, key, value):
        if(isinstance(key, str)):       # Lower case sensitive
            key = key.lower()
        dict.__setitem__(self, key, value)
        
    def __getitem__(self, key):
        if(isinstance(key, str)):       # Lower case sensitive
            key = key.lower()
        return dict.__getitem__(self, key)
    
    def __delitem__(self, key):
        if(isinstance(key, str)):       # Lower case sensitive
            key = key.lower()
        dict.__delitem__(self, key)

    def  update_all(self, func):
        for key in list(self.keys()):       # Grabs all the old values, run it through the given function and then changes the values accordingly
            old_value = self[key]
            new_value = func(old_value)
            self[key] = new_value
