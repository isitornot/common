import asyncio_redis


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Pool(metaclass=Singleton):
    """A context manager for a transaction pool. This is also a Singleton class so we only get one pool per process.
       You can set the config member to a configuration dict (arguments to Pool) prior to the first instantiation
       or pass it as a config={} argument during the first instantiation.
    """
    config = {}

    def __init__(self, config=None):
        self.pool = None
        if config:
            self.config = config

    async def __aenter__(self):
        self.pool = await asyncio_redis.Pool.create(**self.config)
        return self.pool

    async def __aexit__(self, *args):
        self.pool = None

