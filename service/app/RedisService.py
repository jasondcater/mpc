import redis

class RedisService:

    def __init__(self):
        
        self.host = "127.0.0.1"
        self.port = 6379
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=1)
        self.conn = redis.Redis(connection_pool=self.pool)

    def getConnection(self):

        return self.conn

    def setList(self, key, lst):

        if self.conn.exists(key):
            index = 0
            while index < len(lst):
                self.conn.lset(key, index, lst[index])
                index += 1

        else:
            index = 0
            while index < len(lst):
                self.conn.rpush(key, lst[index])
                index += 1

    def getList(self, key):

        if self.conn.exists(key):
            return self.conn.lrange(key, 0, -1)

        else:
            return None

    def getAllKeys(self):
        
        return self.conn.keys("*")

    def deleteKey(self, key):
        
        self.conn.delete(key) 

    def clearTLE(self):

        keys = self.getAllKeys()

        for key in keys:
            self.deleteKey(key)

        meta = [
            "id",
            "name",
            "tle1",
            "tle2",
            "timestamp",
            "type",
            "country",
            "launch",
            "site",
            "decay",
            "period",
            "inclination",
            "apogee",
            "perigee",
        ]

        self.setList("meta", meta)
