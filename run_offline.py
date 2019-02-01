# coding=utf-8
'''
Created on 2018-8-20
@author: gzx
Project:接口测试
'''
import logging
import time

import sys
import unittest

import HTMLTestRunner

from earth_api.create_order import *
from earth_merchant_api.earth_merchant_api_func import *
from my_cnf.logging_auto import my_log
from my_cnf.mysql_auto import My_mysql
from my_cnf.redis_auto import My_redis


class EarthTest (unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("************************start************************\n")
        cls.my = My_mysql()
        cls.my.mysql_conn()
        cls.my_redis = My_redis()
        cls.memberID = "1145"
        cls.token_c = "d406084b1c99429fbea2d1200d45bbba"
        cls.token_b = "16757541e08646bdb429cfd342fbfb90"
        cls. empNo_pda = "247"
        cls.token_pda = "efd95c8a1a0e446f801de0a7d9fe64a8"
        cls.empNo_ps = "263"
        cls.token_ps = "be729a5baaf14ac785fcb4c5e22995f8"
        cls.offline_order = Create_Order_Offline(cls.token_c)


#自营实物计件商品
    """
    skip装饰器一共有三个 unittest.skip(reason)、unittest.skipIf(condition, reason)、unittest.skipUnless(condition, reason)，
    skip无条件跳过，skipIf当condition为True时跳过，skipUnless当condition为False时跳过。
    """

    # @unittest.skip
    def test_order_offline_001(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询前仓减超卖库存
        sql0 = """select b.stock_value - a.stock_less FROM (select stock_less from twms_stock where stock_id  in (
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 17918)) a,
                  (select stock_value from twms_stock_item  where  warehouse_type = 240 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 17918)) b """
        redis_stock0 = self.my_redis.get_redis(17918)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        sql_data0 = self.my.mysql_exec(sql0)
        stock_warehouse0 = sql_data0[0][0]
        my_log.debug('下单前仓库实物库存' + str(stock_warehouse0))
        orderid = self.offline_order.create_17918()  # 闪电付下单
        time.sleep(2)
        redis_stock1 = self.my_redis.get_redis(17918)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        sql_data1 = self.my.mysql_exec(sql0)
        stock_warehouse1 = sql_data1[0][0]
        my_log.debug('下单后仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物计件商品线上库存扣减有误")
        self.assertEqual(110000, stock_warehouse0-stock_warehouse1, msg="自营实物计件商品下单实物库存扣减有误")
        # 获取会员码
        # member_code = get_member_code(self.token_c)
        # print(member_code)
        #核销闪电付订单
        res = quickpaycheck(self.token_b, orderid)
        self.assertEqual(1, res, msg='自营实物计件商品订单核销失败')
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    # @unittest.skip
    def test_order_offline_002(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询前仓减超卖库存
        sql0 = """select b.stock_value - a.stock_less FROM (select stock_less from twms_stock where stock_id  in (
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 18025)) a,
                  (select stock_value from twms_stock_item  where  warehouse_type = 240 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 18025)) b """
        redis_stock0 = self.my_redis.get_redis(18025)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        sql_data0 = self.my.mysql_exec(sql0)
        stock_warehouse0 = sql_data0[0][0]
        my_log.debug('下单前仓库实物库存' + str(stock_warehouse0))
        orderid = self.offline_order.create_18025()  # 闪电付下单
        time.sleep(2)
        redis_stock1 = self.my_redis.get_redis(18025)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        sql_data1 = self.my.mysql_exec(sql0)
        stock_warehouse1 = sql_data1[0][0]
        my_log.debug('下单后仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营实物生产加工商品线上库存扣减有误")
        self.assertEqual(110000, stock_warehouse0-stock_warehouse1, msg="自营实物计件生产加工下单实物库存扣减有误")
        # 获取会员码
        # member_code = get_member_code(self.token_c)
        # print(member_code)
        #核销闪电付订单
        res = quickpaycheck(self.token_b, orderid)
        self.assertEqual(1, res, msg='自营实物生产加工商品订单核销失败')
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    # @unittest.skip
    def test_order_offline_003(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询前仓减超卖库存
        sql0 = """select b.stock_value - a.stock_less FROM (select stock_less from twms_stock where stock_id  in (
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 17923)) a,
                  (select stock_value from twms_stock_item  where  warehouse_type = 240 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id = 17923)) b """
        redis_stock0 = self.my_redis.get_redis(17923)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        sql_data0 = self.my.mysql_exec(sql0)
        stock_warehouse0 = sql_data0[0][0]
        my_log.debug('下单前仓库实物库存' + str(stock_warehouse0))
        orderid = self.offline_order.create_17923()  # 闪电付下单
        time.sleep(2)
        redis_stock1 = self.my_redis.get_redis(17923)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        sql_data1 = self.my.mysql_exec(sql0)
        stock_warehouse1 = sql_data1[0][0]
        my_log.debug('下单后仓库实物库存' + str(stock_warehouse1))
        self.assertEqual(57000,redis_stock0-redis_stock1, msg="自营实物生产加工商品线上库存扣减有误")
        self.assertEqual(57000, stock_warehouse0-stock_warehouse1, msg="自营实物计件生产加工下单实物库存扣减有误")
        # 获取会员码
        # member_code = get_member_code(self.token_c)
        # print(member_code)
        #核销闪电付订单
        res = quickpaycheck(self.token_b, orderid)
        self.assertEqual(1, res, msg='自营实物生产加工商品订单核销失败')
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')

    # @unittest.skip
    def test_order_offline_004(self):
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '开始执行****************************')
        """
        1.下单前后验证线上库存；
        2.拣货前后验证临时区库存；
        3.揽件前后验证仓库库存；
        """
        # 查询原材料前仓减超卖库存
        sql0 = """select b.stock_value - a.stock_less FROM (select stock_less,stock_id stock_id_a from twms_stock where stock_id  in (
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id in (18024,20930))) a,
                  (select s.stock_value,s.stock_id stock_id_b from twms_stock_item s  where  warehouse_type = 240 and stock_id in 	(
                    select twms_stock.stock_id from twms_stock where warehouse_id = 10056 and goods_sku_id  in (18024,20930))) b 
                  where a.stock_id_a = b.stock_id_b"""
        redis_stock0 = self.my_redis.get_redis(18022)
        my_log.debug('下单前redis线上库存' + str(redis_stock0))
        orderid = self.offline_order.create_18022()  # 闪电付下单
        time.sleep(2)
        redis_stock1 = self.my_redis.get_redis(18022)
        my_log.debug('下单后redis线上库存' + str(redis_stock1))
        self.assertEqual(110000,redis_stock0-redis_stock1, msg="自营餐食计件生产加工商品线上库存扣减有误")
        # 获取堂食待出餐订单
        listdata = order_list(self.token_b)
        sql_data0 = self.my.mysql_exec(sql0)
        sku1_stock_warehouse0 = sql_data0[0][0]
        sku2_stock_warehouse0 = sql_data0[1][0]
        my_log.debug('B端确认出餐前原材料1、原材料2仓库实物库存%s,%s'%(sku1_stock_warehouse0, sku2_stock_warehouse0))
        # 堂食订单确认出餐
        confirmMeal(self.token_b, listdata)
        time.sleep(2)
        sql_data1 = self.my.mysql_exec(sql0)
        sku1_stock_warehouse1 = sql_data1[0][0]
        sku2_stock_warehouse1 = sql_data1[1][0]
        my_log.debug('B端确认出餐后原材料1、原材料2仓库实物库存%s,%s' % (sku1_stock_warehouse1, sku2_stock_warehouse1))
        self.assertEqual(33000, sku1_stock_warehouse0 - sku1_stock_warehouse1, msg="自营餐食计件生产加工拣货原材料18024库存扣减有误")
        self.assertEqual(44000, sku2_stock_warehouse0 - sku2_stock_warehouse1, msg="自营餐食计件生产加工拣货原材料20930库存扣减有误")
        # B端餐食堂食核销
        confirm_data = confirm(self.token_b, listdata)
        my_log.debug('B端核销后订单状态%s' % confirm_data)
        self.assertEqual(46, confirm_data, msg='自营餐食计件生产加工商品订单核销失败')
        my_log.info('*****************************用例' + sys._getframe().f_code.co_name + '执行结束****************************')


    @classmethod
    def tearDownClass(cls):
        cls.my.mysql_close ()
        print("*************************end*************************")


if __name__ == '__main__':
    # unittest.main()
    filename = 'report\earth_TestReport.html'    #测试报告的存放路径及文件名

    fp = open(filename, 'wb')    # 创测试报告html文件，此时还是个空文件

    suite = unittest.TestSuite()   # 调用unittest的TestSuite(),理解为管理case的一个容器（测试套件）
    suite.addTest(EarthTest('test_order_offline_001'))  # 向测试套件中添加用例，"TestMethod"是上面定义的类名，"test01"是用例名
    # suite.addTest(EarthTest('test_order_offline_002'))
    # suite.addTest(EarthTest('test_order_offline_003'))
    # suite.addTest(EarthTest('test_order_offline_004'))

    # runner = unittest.TextTestRunner()   # 执行套件中的用例
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='接口测试报告', description='测试结果如下: ')
    #  stream = fp  引用文件流
    #  title  测试报告标题
    #  description  报告说明与描述
    runner.run(suite)   # 执行测试
    fp.close()   # 关闭文件流，将HTML内容写进测试报告文件