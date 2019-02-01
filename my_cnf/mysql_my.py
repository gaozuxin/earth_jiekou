#批量注册会员


# coding=utf-8
# select * from tdms_batch_order_item where order_id='100024905932';
# 根据订单查询批次

# 导入pymysql的包
from time import sleep

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
        # SQL 插入语句

        # try:
        # 执行sql语句
        self.cur.execute(sql1)
        # 提交到数据库执行
        self.conn.commit()
        # except:
        #     # Rollback in case there is any error
        #     self.conn.rollback()

    def mysql_exec1(self, sql1):
        self.cur.execute(sql1)
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

    #
    def mysql_commit(self):
        self.conn.commit()

    def mysql_close(self):
        self.cur.close()  # 关闭游标
        self.conn.close()  # 释放数据库资源
        # return row_data


if __name__ == "__main__":
    my = My_mysql()
    my.mysql_conn()
    for num in range(16966662201,16966662501):
        tel = num

        sql = """INSERT INTO `tmember` (`tel`, `passwd`, `nick_name`, `sex`, `photo`, `birth`, `member_status`, `user_agent`, `device_type`, `device_code`, `register_time`, `salesman`, `sell_time`, `city_name`, `shop_id`, `device`, `is_unsubscribe`)
           VALUES
            (%s, 'bcb15f821479b4d5772bd0ca866c00ad5f926e3580720659cc80d39c9d09802a', %s, 1, '', '2017-09-14', 95, NULL, 1, '', '2017-07-13 22:47:58', NULL, '2018-01-15 14:47:48', NULL, NULL, NULL, 0);""" % (tel,tel)
        print(sql)
        my.mysql_exec(sql)

        sql2 = """select member_id from tmember where  tel= %s; """ % tel

        sql_data = my.mysql_exec1(sql2)
        member_id = sql_data[0][0]

        print(member_id)
        sql3 = """INSERT INTO `tmember_assets` (`member_id`, `balance`, `lock_balance`, `value_card`, `level_id`, `history_score`, `consume_score`, `balance_score`, `growth_value`, `member_type`, `deadline`)
    VALUES
        (%s, 0, 0, 0, 1, 0, 0, 0, 1, 92, NULL);""" % member_id
        print(sql3)
        my.mysql_exec(sql3)

