from model.MysqlModel import MysqlModel


class RegisterModel(MysqlModel):
    def __init__(self):
        self.mysql = MysqlModel.instance()

    def del_phone_register(self, register_phone):
        register_phone = '234' + register_phone
        sql = "delete from user_local_auth where username = '%s' limit 1" % register_phone
        rs1 = self.mysql.execute_db(sql)
        sql = "delete from user where phone = '%s' limit 1" % register_phone
        rs2 = self.mysql.execute_db(sql)
        return rs1 and rs2

    def del_email_register(self, register_email):
        sql = "delete from user_local_auth where username = '%s' limit 1" % register_email
        rs1 = self.mysql.execute_db(sql)
        sql = "delete from user where mail = '%s' limit 1" % register_email
        rs2 = self.mysql.execute_db(sql)
        return rs1 and rs2

    def get_email_code(self, register_email):
        sql = "select code from user_email_verify_code where email = '%s' order by send_time desc limit 1" % register_email
        data = self.mysql.query_db(sql, state='one')
        print(data)
        return data

    def get_sms_code(self, phone):
        phone = '234' + phone
        sql = "select code from user_sms_verify_code where phone = '%s' order by send_time desc limit 1" % phone
        data = self.mysql.query_db(sql, state='one')
        print(data)
        return data
