from concurrent.futures import ThreadPoolExecutor


class ThreadSet:
    _instance = None
    Threadset = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    # 创建线程池
    def __init__(self):
        self.Threadset = ThreadPoolExecutor(max_workers=6)
        
