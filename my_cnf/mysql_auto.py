# coding=utf-8
# select * from tdms_batch_order_item where order_id='100024905932';
# 根据订单查询批次

# 导入pymysql的包
import pymysql

from my_cnf.config_auto import MYSQL_HOST,MYSQL_USER,MYSQL_PASSWD,MYSQL_DB,MYSQL_PORT
from my_cnf.logging_auto import my_log


class My_mysql (object):
    def __init__(self):
        pass

    def mysql_conn(self):
        self.conn = pymysql.connect (host=MYSQL_HOST,
                                     user=MYSQL_USER,
                                     passwd=MYSQL_PASSWD,
                                     db=MYSQL_DB,
                                     port=MYSQL_PORT,
                                     charset='utf8')
        self.cur = self.conn.cursor()  # 获取一个游标

    def mysql_exec(self, sql1):
        self.cur.execute (sql1)
        # row_3 = cur.execute(sql1)
        # print(row_3)  # 影响行数
        # row_1 = cur.fetchone()  # 获取第一行数据
        # print(row_1)
        # row_n = cur.fetchmany(3)  # 获取前n行数据
        # print(row_n)
        row_data = self.cur.fetchall()  # 获取所有数据
        self.conn.commit()
        my_log.debug('MYSQL查询数据' + str(row_data))
        return row_data
        # for d in row_data:
        #     # 注意int类型需要使用str函数转义
        #     print("货位：" + str(d[0]) + ' 货位名称：' + d[1] + " 货位条码：" + d[2])
        # conn.commit() # 提交，不然无法保存新建或者修改的数据

    def mysql_commit(self):
        self.conn.commit()

    def mysql_close(self):
        self.cur.close()  # 关闭游标
        self.conn.close()  # 释放数据库资源
        # return row_data


if __name__ == "__main__":
    # sql = "select * from twms_cargospace where cargospace_name = 'DCHJ999';"
    # print(connect_mysql(sql))
    orderid = 100367414789
    Sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM tcustomer_service c 
                          LEFT JOIN trefund_info r ON c.order_id = r.order_id WHERE c.order_id = %s;""" % orderid

    my = My_mysql ()
    my.mysql_conn ()


    sql_data = my.mysql_exec (Sql5)
    sql_data=list(sql_data)
    data0 = [(443, 957, 1130, 40),]
    if sql_data  == data0:
        print("aaa")
    else:
        print("bbbb")

    # sql_data1 = my1.mysql_exec (sql1)

    my.mysql_close ()
    # my.mysql_close ()
    # sql = "select * from twms_cargospace WHERE bar_code IN ('HH001');"
    # sql1 = "select * from twms_cargospace WHERE  bar_code IN ('HH001ZJ');"

    # print (sql_data)
    # print (sql_data1)
    # print(sql_data[0][0], sql_data[0][1])
