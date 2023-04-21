class CustomMeta(type):
    def __new__(mcs, name, bases, dct):
        new_dct = {}
        for key, value in dct.items():
            if not key.startswith("__") or not key.endswith('__'):
                new_dct["custom_" + key] = value
            else:
                new_dct[key] = value

        new_class = super().__new__(mcs, name, bases, new_dct)

        def custom_setattr(self, name, value):
            if (not name.startswith("__") or not name.endswith('__')) and not hasattr(self, name):
                name = "custom_" + name

            self.__dict__[name] = value

        new_class.__setattr__ = custom_setattr
        return new_class
