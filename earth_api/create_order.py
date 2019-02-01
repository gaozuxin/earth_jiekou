import time
from my_cnf.logging_auto import my_log
from my_cnf.config_auto import EARTHAPI_URL
from my_func.my_request import my_request


class Create_Order_Online:

    def __init__(self, token_c):
        self.token_c = token_c
        get_now_time = int(time.time())
        self.get_start_time = (get_now_time % 3600 // 900 * 900 + 2700 + (get_now_time - get_now_time % 3600)) * 1000
        self.get_end_time = self.get_start_time + 1800000

    def create_ps_21861(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33637",
                    "goodsSkuId": "21861",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "270",
            "shopId": "10041",
            "payAmount": "270",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21861(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33637",
                    "goodsSkuId": "21861",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "220",
            "shopId": "10041",
            "payAmount": "220",
            "packAmount": "0",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21863(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33639",
                    "goodsSkuId": "21863",
                    "num": 1,
                    "weightValue": 1700,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "84",
            "shopId": "10041",
            "payAmount": "84",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21863(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33639",
                    "goodsSkuId": "21863",
                    "num": 1,
                    "weightValue": 1700,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "34",
            "shopId": "10041",
            "payAmount": "34",
            "packAmount": "0",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21865(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33641",
                    "goodsSkuId": "21865",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "270",
            "shopId": "10041",
            "payAmount": "270",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21865(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33641",
                    "goodsSkuId": "21865",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "220",
            "shopId": "10041",
            "payAmount": "220",
            "packAmount": "0",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21868(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33644",
                    "goodsSkuId": "21868",
                    "num": 1,
                    "weightValue": 1700,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "84",
            "shopId": "10041",
            "payAmount": "84",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21868(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33644",
                    "goodsSkuId": "21868",
                    "num": 1,
                    "weightValue": 1700,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "34",
            "shopId": "10041",
            "payAmount": "34",
            "packAmount": "0",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21873(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33649",
                    "goodsSkuId": "21873",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "281",
            "shopId": "10041",
            "payAmount": "281",
            "packAmount": "11",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21873(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33649",
                    "goodsSkuId": "21873",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "231",
            "shopId": "10041",
            "payAmount": "231",
            "packAmount": "11",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21875(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33651",
                    "goodsSkuId": "21875",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "281",
            "shopId": "10041",
            "payAmount": "281",
            "packAmount": "11",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21875(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33651",
                    "goodsSkuId": "21875",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "231",
            "shopId": "10041",
            "payAmount": "231",
            "packAmount": "11",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21877(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33653",
                    "goodsSkuId": "21877",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "281",
            "shopId": "10041",
            "payAmount": "281",
            "packAmount": "11",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21877(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33653",
                    "goodsSkuId": "21877",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "231",
            "shopId": "10041",
            "payAmount": "231",
            "packAmount": "11",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21878(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33654",
                    "goodsSkuId": "21878",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "281",
            "shopId": "10041",
            "payAmount": "281",
            "packAmount": "11",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21878(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33654",
                    "goodsSkuId": "21878",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "231",
            "shopId": "10041",
            "payAmount": "231",
            "packAmount": "11",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21879(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33655",
                    "goodsSkuId": "21879",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "281",
            "shopId": "10041",
            "payAmount": "281",
            "packAmount": "11",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21879(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33655",
                    "goodsSkuId": "21879",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "231",
            "shopId": "10041",
            "payAmount": "231",
            "packAmount": "11",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_ps_21880(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33656",
                    "goodsSkuId": "21880",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "281",
            "shopId": "10041",
            "payAmount": "281",
            "packAmount": "11",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_zt_21880(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "33656",
                    "goodsSkuId": "21880",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingEndTime": self.get_end_time,
                "shippingStartTime": self.get_start_time,
                "shippingType": "111",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "231",
            "shopId": "10041",
            "payAmount": "231",
            "packAmount": "11",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res


class Create_Order_Offline:

    def __init__(self, token_c):
        self.token_c = token_c

    def create_17918(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 0,
                "goodsList": [{
                    "goodsId": "18122",
                    "goodsSkuId": "17918",
                    "num": 11,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "0",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "220",
            "shopId": "10041",
            "payAmount": "220",
            "packAmount": "0",
            "shippingAmount": "0",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "2",
            "score": "0",
            "taxPrice": "0",
            "token": self.token_c,
            "memberId": "1145",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        # print(data_eval)
        res = data_eval['_data']['orderId']

        # print(res)

        return res


class Create_Order_ProOnline:
    def __init__(self, token_c):
        self.token_c = token_c

    def create_21884(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33660",
                    "goodsSkuId": "21884",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1749,
                    "proType": 284
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "3450",
            "shopId": "10041",
            "payAmount": "3450",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21885(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33661",
                    "goodsSkuId": "21885",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1751,
                    "proType": 285
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "3450",
            "shopId": "10041",
            "payAmount": "3450",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21886(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33662",
                    "goodsSkuId": "21886",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1752,
                    "proType": 286
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "2750",
            "shopId": "10041",
            "payAmount": "2750",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21887(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33663",
                    "goodsSkuId": "21887",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1754,
                    "proType": 289
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "2050",
            "shopId": "10041",
            "payAmount": "2050",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21888(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33664",
                    "goodsSkuId": "21888",
                    "num": 1,
                    "fareType": 0,
                    "proId": 1756,
                    "proType": 1178
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "450",
            "shopId": "10041",
            "payAmount": "450",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21889(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33665",
                    "goodsSkuId": "21889",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1757,
                    "proType": 288
                }, {
                    "goodsId": "33666",
                    "goodsSkuId": "21890",
                    "num": 1,
                    "fareType": 1,
                    "proId": 1757,
                    "proType": 288
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "2850",
            "shopId": "10041",
            "payAmount": "2850",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21890(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33666",
                    "goodsSkuId": "21890",
                    "num": 2,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "2400",
            "shopId": "10041",
            "payAmount": "2450",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21891(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33667",
                    "goodsSkuId": "21891",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1750,
                    "proType": 284
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "1550",
            "shopId": "10041",
            "payAmount": "1550",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": "06ae5280da144e0eabd06fd55435867b",
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21893(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33669",
                    "goodsSkuId": "21893",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1753,
                    "proType": 286
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "1010",
            "shopId": "10041",
            "payAmount": "1010",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21894(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33670",
                    "goodsSkuId": "21894",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1755,
                    "proType": 289
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "650",
            "shopId": "10041",
            "payAmount": "650",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21896(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33672",
                    "goodsSkuId": "21896",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1758,
                    "proType": 288
                }, {
                    "goodsId": "33667",
                    "goodsSkuId": "21891",
                    "num": 1,
                    "fareType": 1,
                    "proId": 1758,
                    "proType": 288
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "950",
            "shopId": "10041",
            "payAmount": "950",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_21897(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33673",
                    "goodsSkuId": "21897",
                    "num": 2,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }],
            "cardValue": "400",
            "shopId": "10041",
            "payAmount": "450",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res

    def create_goods_all(self):
        url = EARTHAPI_URL + "/order/create"
        data = {
            "orderStoreInfoList": [{
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33667",
                    "goodsSkuId": "21891",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1750,
                    "proType": 284
                }, {
                    "goodsId": "33669",
                    "goodsSkuId": "21893",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1753,
                    "proType": 286
                }, {
                    "goodsId": "33670",
                    "goodsSkuId": "21894",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1755,
                    "proType": 289
                }, {
                    "goodsId": "33672",
                    "goodsSkuId": "21896",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1758,
                    "proType": 288
                }, {
                    "goodsId": "33667",
                    "goodsSkuId": "21891",
                    "num": 1,
                    "fareType": 1,
                    "proId": 1758,
                    "proType": 288
                }, {
                    "goodsId": "33673",
                    "goodsSkuId": "21897",
                    "num": 2,
                    "fareType": 0,
                    "proId": 0,
                    "proType": 0
                }],
                "shippingType": "112",
                "storeId": "173",
                "storeType": 63
            }, {
                "distributeType": 80,
                "goodsList": [{
                    "goodsId": "33660",
                    "goodsSkuId": "21884",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1749,
                    "proType": 284
                }, {
                    "goodsId": "33661",
                    "goodsSkuId": "21885",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1751,
                    "proType": 285
                }, {
                    "goodsId": "33662",
                    "goodsSkuId": "21886",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1752,
                    "proType": 286
                }, {
                    "goodsId": "33663",
                    "goodsSkuId": "21887",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1754,
                    "proType": 289
                }, {
                    "goodsId": "33664",
                    "goodsSkuId": "21888",
                    "num": 1,
                    "fareType": 0,
                    "proId": 1756,
                    "proType": 1178
                }, {
                    "goodsId": "33665",
                    "goodsSkuId": "21889",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1757,
                    "proType": 288
                }, {
                    "goodsId": "33666",
                    "goodsSkuId": "21890",
                    "num": 1,
                    "fareType": 1,
                    "proId": 1757,
                    "proType": 288
                }, {
                    "goodsId": "33666",
                    "goodsSkuId": "21890",
                    "num": 2,
                    "fareType": 0,
                    "proId": 1757,
                    "proType": 288
                }],
                "shippingType": "110",
                "storeId": "97",
                "storeType": 62
            }],
            "cardValue": "21460",
            "shopId": "10041",
            "payAmount": "21510",
            "packAmount": "0",
            "shippingAmount": "50",
            "thirdPayAmount": "0",
            "payType": "497",
            "orderType": "0",
            "score": "0",
            "memberAddrId": "4720",
            "taxPrice": "0",
            "isException": "0",
            "token": self.token_c,
            "memberId": "1689",
            "channel": 218,
            "warehouseId": "10056",
            "centerShopId": "10000",
            "centerWarehouseId": "10034",
            "v": 2
        }
        data_eval = my_request(url, data)
        my_log.debug('创建订单数据' + str(data_eval))
        res = data_eval['_data']['orderId']
        return res


if __name__ == '__main__':
    token_c = '06ae5280da144e0eabd06fd55435867b'
    online = Create_Order_Online(token_c)
    proonline = Create_Order_ProOnline(token_c)
    # proonline.create_21884()
    # time.sleep(5)
    # proonline.create_21885()
    # time.sleep(5)
    # proonline.create_21886()
    # time.sleep(5)
    # proonline.create_21887()
    # time.sleep(5)
    # proonline.create_21888()
    # time.sleep(5)
    # proonline.create_21889()
    # time.sleep(5)
    # proonline.create_21890()
    # time.sleep(5)
    # proonline.create_21891()
    # time.sleep(5)
    # proonline.create_21893()
    # time.sleep(5)
    # proonline.create_21894()
    # time.sleep(5)
    # proonline.create_21896()
    # time.sleep(5)
    # proonline.create_21897()
    # time.sleep(5)
    # proonline.create_goods_all()
    # online = Create_Order_Online(token_c)
    online.create_ps_21861()
    # time.sleep(5)
    # online.create_zt_21861()
    # time.sleep(5)
    # online.create_ps_21863()
    # time.sleep(5)
    # online.create_zt_21863()
    # time.sleep(5)
    # online.create_ps_21865()
    # time.sleep(5)
    # online.create_zt_21865()
    # time.sleep(5)
    # online.create_ps_21868()
    # time.sleep(5)
    # online.create_zt_21868()
    # time.sleep(5)
    # online.create_ps_21873()
    # time.sleep(5)
    # online.create_zt_21873()
    # time.sleep(5)
    # online.create_ps_21875()
    # time.sleep(5)
    # online.create_zt_21875()
    # time.sleep(5)
    # online.create_ps_21877()
    # time.sleep(5)
    # online.create_zt_21877()
    # time.sleep(5)
    # online.create_ps_21878()
    # time.sleep(5)
    # online.create_zt_21878()
    # time.sleep(5)
    # online.create_ps_21879()
    # time.sleep(5)
    # online.create_zt_21879()
    # time.sleep(5)
    # online.create_ps_21880()
    # time.sleep(5)
    # online.create_zt_21880()
    online = Create_Order_Online("febbaa74c52d46bba3422196ca4473a8").create_ps_21863()
# checkResult (integer, optional): 本次核验结果：0不核验、1-成功、2-失败 ,
# checkState (integer, optional): 核验状态：0未核验、1-成功、2-失败 ,