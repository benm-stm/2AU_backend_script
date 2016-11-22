import MySQLdb

#create a singleton for the DB connection
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class dao():
    __metaclass__ = Singleton
    def __init__(self, host, user, passwd, db):
        self._db_connection = MySQLdb.connect(host, user, passwd, db)
        self._db_cur = self._db_connection.cursor()
        
    def getDao(self):
        return self._db_cur
