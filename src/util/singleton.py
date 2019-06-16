class Singleton(type):
    '''
    Singleton metaclass.
    '''
    def __new__(cls, name, base, attrs):
        attrs['_Singleton__instance'] = None
        return super().__new__(cls, name, base, attrs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            new_instance = super().__call__(*args, **kwargs)
            cls.__instance = new_instance
        return cls.__instance
