class Config:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.isService = False
        self.ip = None
        self.port = None
        self.isConnect = False
        self.name = "Name"
        
