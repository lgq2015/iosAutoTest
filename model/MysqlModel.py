from utils.BaseMysql import MysqlDb
from utils.BaseReadConfig import ReadConfig

rc = ReadConfig()
db = rc.get_database('DATABASE1')


class MysqlModel:
    _mysql = None

    @classmethod
    def instance(cls):
        if cls._mysql:
            return cls._mysql
        else:
            obj = MysqlDb(db['host'], db['port'], db['user'], db['password'], 'ums')
            cls._mysql = obj
            return cls._mysql
