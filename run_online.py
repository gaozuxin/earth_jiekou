# coding=utf-8
'''
Created on 2018-8-20
@author: gzx
Project:接口测试
'''

import unittest, sys

import HTMLTestRunner

from earth_api.batch_data import *
from earth_api.create_order import *
from my_cnf.mysql_auto import My_mysql
from my_cnf.redis_auto import My_redis
from my_func.my_token import *


class EarthTest (unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        print("************************start************************\n")
        cls.my = My_mysql()
        cls.my.mysql_conn()
        cls.my_redis = My_redis()
        cls. empNo_pda = "334"
        cls.empNo_ps = "335"
        # cls.token_c = "594fdbfb97274656b6c1db77b0cced68"
        # cls.token_pda = "b3a39a8fa24347c6a045414981624f1d"
        # cls.token_ps = "3c2bc8240a97403695dce1a1526baeda"
        cls.token_b = login_b()
        cls.token_c = login_c()
        cls.token_pda = login_pda()
        cls.token_ps = login_ps()
        cls.online_order = Create_Order_Online(cls.token_c)
#自营实物计件商品
    """
    skip装饰器一共有三个 unittest.skip(reason)、unittest.skipIf(condition, reason)、unittest.skipUnless(condition, reason)，
    skip无条件跳过，skipIf当condition为True时跳过，skipUnless当condition为False时跳过。
    """
    # @unittest.skip
    def test_order_001_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order001_ps = Order_Batch_001_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order001_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order001_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order001_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = () # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_002_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order002_ps = Order_Batch_002_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order002_ps.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order002_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(90000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order002_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 40),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_003_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                     select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                     SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21861()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000, redis_stock0 - redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order003_ps = Order_Batch_003_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order003_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order003_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(80000, stock_warehouse1 - stock_warehouse0, msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order003_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 60),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_004_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order004_ps = Order_Batch_004_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order004_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order004_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order004_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_005_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order005_ps = Order_Batch_005_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order005_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order005_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order005_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 270),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_006_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order006_ps = Order_Batch_006_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order006_ps.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order006_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(60000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order006_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80), (443, 957, 1130, 40), (443, 610, 1131, 60)) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_007_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order007_ps = Order_Batch_007_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order007_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (17500, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order007_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order007_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = () # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_008_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order008_ps = Order_Batch_008_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order008_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (14000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order008_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order008_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 6),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_009_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order009_ps = Order_Batch_009_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order009_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (17000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order009_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order009_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 6),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_010_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order010_ps = Order_Batch_010_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order010_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (18000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order010_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(15000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order010_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 4),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_011_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order011_ps = Order_Batch_011_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order011_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (16500, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order011_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(16500, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order011_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 1), (443, 608, 566, 33)) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        # my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_012_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order012_ps = Order_Batch_012_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order012_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (17500, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order012_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order012_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 84),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")



        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_013_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order013_ps = Order_Batch_013_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order013_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (14000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order013_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(9000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order013_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 6), (443, 610, 1131, 10), (443, 608, 566, 18)) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_014_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order014_ps = Order_Batch_014_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order014_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order014_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order014_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = () # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_015_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order015_ps = Order_Batch_015_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order015_ps.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order015_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(90000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order015_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 40),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_016_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                     select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                     SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21865()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000, redis_stock0 - redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order016_ps = Order_Batch_016_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order016_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order016_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(80000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order016_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 60),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_017_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order017_ps = Order_Batch_017_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order017_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order017_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order017_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_018_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order018_ps = Order_Batch_018_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order018_ps.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order018_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order018_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 270),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_019_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order019_ps = Order_Batch_019_PS(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order019_ps.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order019_ps.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(60000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order019_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                      LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;"""% orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80), (443, 957, 1130, 40), (443, 610, 1131, 60)) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_020_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order020_ps = Order_Batch_020_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order020_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(17500, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order020_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order020_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ()  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_021_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order021_ps = Order_Batch_021_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order021_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(14000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order021_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order021_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 6),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_022_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order022_ps = Order_Batch_022_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order022_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(17000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order022_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order022_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 6),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_023_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order023_ps = Order_Batch_023_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order023_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(18000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order023_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(15000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order023_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 4),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_024_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order024_ps = Order_Batch_024_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order024_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(16500, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order024_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(16500, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order024_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 1), (443, 608, 566, 33))  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        # my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_025_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order025_ps = Order_Batch_025_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order025_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(17500, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order025_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order025_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 84),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")

        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_026_ps(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order026_ps = Order_Batch_026_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order026_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(14000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order026_ps.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(9000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order026_ps.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = (
            (443, 957, 1130, 6), (443, 610, 1131, 10),
            (443, 608, 566, 18))  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    # @unittest.skip
    def test_order_027_ps(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询原材料仓库总库存
        sql0 = """SELECT (stock_warehouse-stock_less) AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                        SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id IN (21869,21870,21871,21872));"""
        sql1 = """select (stock_warehouse-stock_less) as stock_warehouse from twms_stock where stock_id  in ( 
                        select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id in (21869,21870,21871,21872))"""
        redis_stock0 = self.my_redis.get_redis(21873)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_ps_21873()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21873)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000, redis_stock0 - redis_stock1, msg="自营餐食计件商品线上库存扣减有误")
        time.sleep(30)
        order027_ps = Order_Batch_027_PS(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        order027_ps.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        time.sleep(2)  # 增加等待时间，避免数据库缓存问题
        order027_ps.batch_pack()  # 调用打包揽件接口
        batchId = order027_ps.batch_accept(self.token_pda, self.empNo_pda, self.token_ps, self.empNo_ps)
        sql3 = 'SELECT status from tdms_batch_order where id= %s;' % batchId
        sql_data3 = self.my.mysql_exec(sql3)
        status = sql_data3[0][0]
        my_log.debug('批次揽件状态%s' % status)
        self.assertEqual(25, status, msg="自营餐食计件生产加工批次揽件失败")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    ############################################################################################################

    @unittest.skip
    def test_order_001_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order001_zt = Order_Batch_001_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order001_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order001_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order001_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = () # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_002_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order002_zt = Order_Batch_002_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order002_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order002_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(90000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order002_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 40),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")

        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_003_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order003_zt = Order_Batch_003_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order003_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order003_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(80000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order003_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 60),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")

        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_004_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order004_zt = Order_Batch_004_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order004_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order004_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        time.sleep(3)
        confirm_data = order004_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_005_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order005_zt = Order_Batch_005_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order005_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order005_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        time.sleep(3)
        confirm_data = order005_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 220),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_006_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21861) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21861);"""
        redis_stock0 = self.my_redis.get_redis(21861)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21861()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21861)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order006_zt = Order_Batch_006_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order006_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物计件商品拣货库存扣减有误")
        order006_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(60000, stock_warehouse1 - stock_warehouse0,msg="自营实物计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order006_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80), (443, 957, 1130, 40), (443, 610, 1131, 60))  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")

        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_007_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order007_zt = Order_Batch_007_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order007_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (17500, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order007_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order007_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = () # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_008_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order008_zt = Order_Batch_008_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order008_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (14000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order008_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order008_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 6),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_009_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order009_zt = Order_Batch_009_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order009_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (17000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order009_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order009_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 6),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_010_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order010_zt = Order_Batch_010_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order010_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (18000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order010_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(15000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order010_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 4),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_011_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order011_zt = Order_Batch_011_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order011_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (16500, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order011_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(16500, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order011_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 1), (443, 608, 566, 33)) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_012_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order012_zt = Order_Batch_012_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order012_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (17500, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order012_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order012_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 34),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_013_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21863) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21863);"""
        redis_stock0 = self.my_redis.get_redis(21863)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21863()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21863)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000,redis_stock0-redis_stock1, msg="自营实物计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order013_zt = Order_Batch_013_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order013_zt.batch_picked() # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (14000, stock_temporary1 - stock_temporary0, msg="自营实物计重商品拣货库存扣减有误")
        order013_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(9000, stock_warehouse1 - stock_warehouse0,msg="自营实物计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order013_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 6), (443, 610, 1131, 10), (443, 608, 566, 18)) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计重商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_014_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order014_zt = Order_Batch_014_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order014_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order014_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order014_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物生产加工计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = () # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_015_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order015_zt = Order_Batch_015_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order015_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order015_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(90000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order015_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物生产加工计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 40),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_016_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order016_zt = Order_Batch_016_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order016_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order016_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(80000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order016_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物生产加工计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 60),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_017_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order017_zt = Order_Batch_017_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order017_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order017_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        time.sleep(3)
        confirm_data = order017_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # self.assertEqual(46, confirm_data, msg='自营实物生产加工计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_018_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order018_zt = Order_Batch_018_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order018_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (110000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order018_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(110000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        time.sleep(3)
        confirm_data = order018_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 220),) # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_019_zt(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21865) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21865);"""
        redis_stock0 = self.my_redis.get_redis(21865)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21865()  #需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21865)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工计件商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  #临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order019_zt = Order_Batch_019_ZT(self.empNo_pda,self.token_pda,self.empNo_ps,self.token_ps)#创建批次对象
        batch_id = order019_zt.batch_picked()  # 调用拣货接口
         # 验证拣货任务信息
        sql_data1 =self.my.mysql_exec (sql0 +" UNION ALL " + sql1 )
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual (90000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计件商品拣货库存扣减有误")
        order019_zt.batch_pack() # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec (sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(60000, stock_warehouse1 - stock_warehouse0,msg="自营实物生产加工计件商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order019_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 80), (443, 957, 1130, 40), (443, 610, 1131, 60))  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计件商品退款单信息有误")
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_020_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order020_zt = Order_Batch_020_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order020_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(17500, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order020_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order020_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ()  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_021_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order021_zt = Order_Batch_021_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order021_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(14000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order021_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order021_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 6),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_022_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order022_zt = Order_Batch_022_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order022_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(17000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order022_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(14000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order022_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 6),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_023_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order023_zt = Order_Batch_023_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order023_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(18000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order023_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(15000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        confirm_data = order023_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        self.assertEqual(46, confirm_data, msg='自营实物计件商品订单核销失败')
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 610, 1131, 4),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_024_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order024_zt = Order_Batch_024_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order024_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(16500, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order024_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(16500, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order024_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 957, 1130, 1), (443, 608, 566, 33))  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    @unittest.skip
    def test_order_025_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order025_zt = Order_Batch_025_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order025_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(17500, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order025_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(17500, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order025_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = ((443, 608, 566, 34),)  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    # @unittest.skip
    def test_order_026_zt(self):
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询临时区库存
        sql0 = """select sum(stock_value) from twms_stock_item  where  warehouse_type = 640 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 21868) """
        # 查询仓库总库存
        sql1 = """SELECT stock_warehouse AS stock_warehouse FROM twms_stock WHERE stock_id IN ( 
                    SELECT twms_stock.stock_id FROM twms_stock WHERE warehouse_id = 10056 AND goods_sku_id = 21868);"""
        redis_stock0 = self.my_redis.get_redis(21868)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        self.online_order.create_zt_21868()  # 需要校验返回值
        redis_stock1 = self.my_redis.get_redis(21868)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(17000, redis_stock0 - redis_stock1, msg="自营实物生产加工计重商品线上库存扣减有误")
        time.sleep(30)
        sql_data0 = self.my.mysql_exec(sql0)
        stock_temporary0 = sql_data0[0][0]  # 临时区库存
        my_log.debug('拣货前临时区实物库存' + str(stock_temporary0))
        order026_zt = Order_Batch_026_ZT(self.empNo_pda, self.token_pda, self.empNo_ps, self.token_ps)  # 创建批次对象
        batch_id = order026_zt.batch_picked()  # 调用拣货接口
        # 验证拣货任务信息
        sql_data1 = self.my.mysql_exec(sql0 + " UNION ALL " + sql1)
        stock_temporary1 = sql_data1[0][0]
        stock_warehouse1 = sql_data1[1][0]
        my_log.debug('拣货后临时区实物库存' + str(stock_temporary1))
        my_log.debug('揽件前仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(14000, stock_temporary1 - stock_temporary0, msg="自营实物生产加工计重商品拣货库存扣减有误")
        order026_zt.batch_pack()  # 调用打包揽件接口
        sql_data2 = self.my.mysql_exec(sql1)
        stock_warehouse0 = sql_data2[0][0]
        my_log.debug('揽件后仓库实物库存' + str(stock_warehouse0))
        self.assertEqual(9000, stock_warehouse1 - stock_warehouse0, msg="自营实物生产加工计重商品揽件库存扣减有误")
        order_sql = """ SELECT ti.`order_id`,ti.`order_store_id`,ti.`id`FROM torder_item ti WHERE  ti.`jd_batch_id` = %s;""" % batch_id
        order_data = self.my.mysql_exec(order_sql)
        orderid = order_data[0][0]
        store_id = order_data[0][1]
        id = order_data[0][2]
        order026_zt.batch_delivery(orderid, store_id, id)  # 调用妥投接口
        # 查询退款单商品情况
        sql5 = """SELECT r.refund_status, c.storage_state, c.application_reason, r.amount_due FROM trefund_info r 
                              LEFT JOIN  tcustomer_service  c ON r.customer_service_id = c.id WHERE  c.order_id = %s;""" % orderid
        time.sleep(3)
        refund_info = self.my.mysql_exec(sql5)
        refund_data_ex = (
            (443, 957, 1130, 6), (443, 610, 1131, 10),
            (443, 608, 566, 18))  # ((443:退货状态, 957：入库状态, 1130：申请原因, 40：实际退款),)
        self.assertEqual(refund_data_ex, refund_info, msg="自营实物生产加工计重商品退款单信息有误")
        my_log.info(
            '*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    ############################################################################################################
    @classmethod
    def tearDownClass(cls):
        # order_delivery(cls.token_ps, cls.empNo_ps)
        cls.my.mysql_close ()
        print("*************************end*************************")




if __name__=='__main__':
    unittest.main()

    # filename = 'report\earth_TestReport.html'  # 测试报告的存放路径及文件名
    # fp = open(filename, 'wb')  # 创测试报告html文件，此时还是个空文件
    # suite = unittest.TestSuite()  # 调用unittest的TestSuite(),理解为管理case的一个容器（测试套件）
    # suite.addTest(EarthTest('test_order_001_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_002_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_003_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_004_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_005_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_006_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_007_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_008_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_009_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_010_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_011_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_012_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_013_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_014_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_015_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_016_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_017_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_018_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_019_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_020_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_021_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_022_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_023_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_024_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_025_ps'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_026_ps'))  # 向测试套件中添加用例
    #
    # suite.addTest(EarthTest('test_order_001_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_002_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_003_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_004_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_005_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_006_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_007_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_008_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_009_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_010_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_011_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_012_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_013_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_014_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_015_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_016_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_017_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_018_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_019_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_020_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_021_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_022_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_023_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_024_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_025_zt'))  # 向测试套件中添加用例
    # suite.addTest(EarthTest('test_order_026_zt'))  # 向测试套件中添加用例
    #
    # # runner = unittest.TextTestRunner()   # 执行套件中的用例
    # runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='接口测试报告', description='测试结果如下: ')
    # #  stream = fp  引用文件流
    # #  title  测试报告标题
    # #  description  报告说明与描述
    # runner.run(suite)   # 执行测试
    # fp.close()   # 关闭文件流，将HTML内容写进测试报告文件