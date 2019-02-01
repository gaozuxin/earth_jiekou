# coding=utf-8

import redis

from my_cnf.config_auto import REDIS_HOST,REDIS_PASSWORD,REDIS_PORT,WAREHOUSE_ID


class My_redis (object):
    # WAREHOUSE_ID= 10056
    def __init__(self):
        self.pool = redis.ConnectionPool (host=REDIS_HOST, password=REDIS_PASSWORD, port=REDIS_PORT,
                                          decode_responses=True)
        self.r = redis.Redis (connection_pool=self.pool)

    def set_redis(self, skuid, stock_value):
        s = 'stock_%d_%s' % (WAREHOUSE_ID, skuid)
        self.r.set (s, stock_value * 10000)

    def get_redis(self, skuid):
        s = 'stock_%d_%s' % (WAREHOUSE_ID, skuid)
        goodsstock = float (self.r.get (s))
        return goodsstock


if __name__ == '__main__':
    my_redis = My_redis ()
    # my_redis.set_redis(17923, 5)
    print (my_redis.get_redis(17918)/10000)