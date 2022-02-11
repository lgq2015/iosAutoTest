import pymysql
from warnings import filterwarnings

from utils.BaseReadConfig import ReadConfig
from utils.BaseLog import Log

filterwarnings("ignore", category=pymysql.Warning)  # 忽略mysql警告信息


class MysqlDb:
    logger = Log('mysql', level='info')

    def __init__(self, host, port, user, password, database):
        # 建立数据库连接
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=password,
            database=database,
            charset='utf8'
        )
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()

    def select_db(self, db_name):
        """
        选择数据库
        :return:
        """
        try:
            self.conn.select_db(db_name)
            self.logger.i("选择 {0} 执行成功".format(db_name))
        except Exception as e:
            self.logger.exception("操作出现错误：{0}".format(e))

    def query_db(self, sql, state="all"):
        """
        查询
        :param sql:sql语句
        :param state:all查询所有，outhor查询单条
        :return:
        """
        # 使用 execute() 执行sql
        self.logger.i(sql)
        self.cur.execute(sql)
        if state == "all":
            # 使用 fetchall() 获取查询结果
            data = self.cur.fetchall()
        else:
            data = self.cur.fetchone()
        return data

    def execute_db(self, sql):
        """更新/插入/删除"""
        try:
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
            self.logger.i("{0} 执行成功".format(sql))
        except Exception as e:
            self.logger.exception("操作出现错误：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()
        # 返回受影响行数
        return self.cur.rowcount


if __name__ == '__main__':
    db = ReadConfig().get_database('DATABASE1')
    mysql = MysqlDb(db['host'], db['port'], db['user'], db['password'], db['database'])
    sql = "select code from user_sms_verify_code where phone = '2347017202204' order by send_time desc limit 1"
    data = mysql.query_db(sql, state='one')
    print(data)