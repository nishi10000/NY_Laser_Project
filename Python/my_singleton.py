class MySingleton():        
    _instance = None        

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MySingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def set_name(self, name):
        self._name = name
        return self._name

    def set_read_path(self, read_path):
        self._read_path = read_path
        return self._read_path

    def set_write_path(self, write_path):
        self._write_path = write_path
        return self._write_path

    def get_name(self):
        return self._name

    def get_read_path(self):
        return self._read_path

    def get_write_path(self):
        return self._write_path