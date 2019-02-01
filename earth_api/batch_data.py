import requests
import time

from my_cnf.config_auto import AFTERSALE_URL, WAREHOUSE_ID
from my_cnf.logging_auto import my_log
from my_func.my_request import my_request


class Order_Batch_001_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932925",
            "longitude": "116.469303",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_002_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218617",
                        "goodsId": "33637",
                        "goodsName": "ZDH实物普通商品计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21861",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218617",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "9",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932925",
            "longitude": "116.469303",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_003_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "8",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932925",
            "longitude": "116.469303",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_004_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                return pickingBatchId
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1125,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": 21861
            }],
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由退货",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_005_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                return pickingBatchId
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 434,
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_006_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218617",
                        "goodsId": "33637",
                        "goodsName": "ZDH实物普通商品计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21861",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218617",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "6",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1125,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": 21861
            }],
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由退货",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_007_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186301750123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186301750123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186301750123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186301750123450"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_008_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300500123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300500123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300900123456",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300900123456",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218631",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218631",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300500123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300500123450"
                }, {
                    "count": 1,
                    "pluCode": "992186300900123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186300900123456",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsSpec": "计重001",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186300900123456"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21863",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_009_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300300123452",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300300123452",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300500123450",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300500123450",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186300900123456",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186300900123456",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300500123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300500123450"
                }, {
                    "count": 1,
                    "pluCode": "992186300900123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186300900123456",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsSpec": "计重001",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186300900123456"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21863",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_010_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300300123452",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300300123452",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300500123450",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300500123450",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186301000123452",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186301000123452",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300500123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300500123450"
                }, {
                    "count": 1,
                    "pluCode": "992186301000123452"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186301000123452",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsSpec": "计重001",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186301000123452"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21863",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_011_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186301650123451",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186301650123451",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "1",
                        "goodsBarCode": "2110304218631",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "orderStoreId": orderStoreId,
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218631",
                        "realCount": "0",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186301650123451",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186301650123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))

            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1127,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": 21863
            }],
            "memberId": "335",
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "没理由",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_012_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186301750123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186301750123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186301750123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186301750123450"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 434,
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_013_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300500123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300500123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300900123456",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300900123456",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218631",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218631",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300900123456",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300900123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1127,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": 21863
            }],
            "memberId": "335",
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "没理由",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_014_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932925",
            "longitude": "116.469303",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_015_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218655",
                        "goodsId": "33641",
                        "goodsName": "ZDH实物生产加工计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21865",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218655",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "9",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932925",
            "longitude": "116.469303",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_016_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "8",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932925",
            "longitude": "116.469303",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_017_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                return pickingBatchId
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1125,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": 21865
            }],
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由退货",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_018_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                return pickingBatchId
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 434,
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_019_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218655",
                        "goodsId": "33641",
                        "goodsName": "ZDH实物生产加工计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21865",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218655",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "6",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1125,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": 21865
            }],
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由退货",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_020_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186801750123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186801750123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186801750123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186801750123455"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_021_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800500123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800500123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800900123451",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800900123451",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218686",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218686",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800500123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800500123455"
                }, {
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186800900123451",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsSpec": "计重002",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186800900123451"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21868",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_022_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800300123457",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800300123457",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800500123455",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800500123455",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186800900123451",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186800900123451",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800500123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800500123455"
                }, {
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186800900123451",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsSpec": "计重002",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186800900123451"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21868",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_023_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800300123457",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800300123457",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800500123455",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800500123455",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186801000123457",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186801000123457",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800500123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800500123455"
                }, {
                    "count": 1,
                    "pluCode": "992186801000123457"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186801000123457",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsSpec": "计重002",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186801000123457"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21868",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 1409,
            "latitude": "39.932943",
            "longitude": "116.469291",
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_024_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186801650123456",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186801650123456",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "1",
                        "goodsBarCode": "2110304218686",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "orderStoreId": orderStoreId,
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218686",
                        "realCount": "0",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186801650123456",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186801650123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))

            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1127,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": 21868
            }],
            "memberId": "335",
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "没理由",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_025_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186801750123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186801750123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186801750123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186801750123455"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 0,
            "batchId": self.batch_id,
            "distributeType": 434,
            "memberId": self.empNo_ps,
            "orderId": order_id,
            "orderStoreId": store_id,
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_026_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800500123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800500123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800900123451",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800900123451",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218686",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218686",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800900123451",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1127,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": 21868
            }],
            "memberId": "335",
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "没理由",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")


class Order_Batch_027_PS:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800500123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800500123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800900123451",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800900123451",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218686",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218686",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800900123451",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_ps,
            "memberId": self.empNo_ps,
            "batchId": self.batch_id,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID
        }
        eval_data = my_request(url, data)
        my_log.debug('批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            pass
        else:
            print("batch_data：" + str(self.batch_id) + "批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/distributeresult"
        data = {
            "applicationReason": 1127,
            "batchId": self.batch_id,
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": 21868
            }],
            "memberId": "335",
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "没理由",
            "shopId": "0",
            "token": self.token_ps,
            "warehouseId": WAREHOUSE_ID,
        }
        eval_data = my_request(url, data)
        my_log.debug('订单妥投数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            my_log.debug("支付单号：" + str(order_id) + "订单妥投成功")




###########################################################################################


class Order_Batch_001_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_002_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218617",
                        "goodsId": "33637",
                        "goodsName": "ZDH实物普通商品计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21861",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218617",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "9",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_003_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "8",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_004_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": "21861"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_005_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 434,
            "goodsList": [{
                "count": 11,
                "orderItemId": id,
                "skuId": "21861"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_006_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218617",
                    "goodsId": "33637",
                    "goodsName": "ZDH实物普通商品计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21861",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218617",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218617",
                        "goodsId": "33637",
                        "goodsName": "ZDH实物普通商品计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21861",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218617",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218617",
                "goodsId": "33637",
                "goodsName": "ZDH实物普通商品计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "6",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21861",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": "21861"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_007_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186301750123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186301750123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186301750123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186301750123450"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_008_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300500123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300500123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300900123456",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300900123456",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218631",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218631",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300500123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300500123450"
                }, {
                    "count": 1,
                    "pluCode": "992186300900123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186300900123456",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsSpec": "计重001",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186300900123456"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21863",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_009_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300300123452",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300300123452",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300500123450",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300500123450",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186300900123456",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186300900123456",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300500123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300500123450"
                }, {
                    "count": 1,
                    "pluCode": "992186300900123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186300900123456",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsSpec": "计重001",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186300900123456"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21863",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_010_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300300123452",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300300123452",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300500123450",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300500123450",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186301000123452",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186301000123452",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300500123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300500123450"
                }, {
                    "count": 1,
                    "pluCode": "992186301000123452"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186301000123452",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsSpec": "计重001",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186301000123452"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21863",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_011_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186301650123451",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186301650123451",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "1",
                        "goodsBarCode": "2110304218631",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "orderStoreId": orderStoreId,
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218631",
                        "realCount": "0",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186301650123451",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186301650123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))

            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": "21863"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_012_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186301750123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186301750123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186301750123450",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186301750123450"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 434,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": "21863"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_013_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186300500123450",
                    "goodsId": "33639",
                    "goodsName": "ZDH实物普通商品计重001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21863",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186300500123450",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186300900123456",
                        "goodsId": "33639",
                        "goodsName": "ZDH实物普通商品计重001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21863",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186300900123456",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218631",
                            "goodsId": "33639",
                            "goodsName": "ZDH实物普通商品计重001-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21863",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218631",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186300900123456",
                "goodsId": "33639",
                "goodsName": "ZDH实物普通商品计重001-自营",
                "goodsSpec": "计重001",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186300900123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21863",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": "21863"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_014_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_015_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218655",
                        "goodsId": "33641",
                        "goodsName": "ZDH实物生产加工计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21865",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218655",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "9",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_016_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "8",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_017_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": "21865"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_018_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待10S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "11",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "11",
                "shopId": "0",
                "shouldCount": "11",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 434,
            "goodsList": [{
                "count": 11,
                "orderItemId": id,
                "skuId": "21865"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_019_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "2",
                    "goodsBarCode": "2110304218655",
                    "goodsId": "33641",
                    "goodsName": "ZDH实物生产加工计数001-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21865",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "2110304218655",
                    "realCount": "9",
                    "shouldCount": "11",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": "10056",
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534745014603",
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": "1867",
                        "contianerCode": "J9099",
                        "deferenceCount": "2",
                        "goodsBarCode": "2110304218655",
                        "goodsId": "33641",
                        "goodsName": "ZDH实物生产加工计数001-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21865",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": "334",
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218655",
                        "realCount": "9",
                        "shouldCount": "11",
                        "uuid": uuid,
                        "token": self.token_pda,
                        "memberId": "334",
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "2110304218655",
                "goodsId": "33641",
                "goodsName": "ZDH实物生产加工计数001-自营",
                "goodsSpec": "计数001",
                "packBoxBarcode": "P9099",
                "pricingMethod": 390,
                "realCount": "6",
                "shopId": "0",
                "shouldCount": "9",
                "skuId": "21865",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1534759879014",
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 4,
                "orderItemId": id,
                "skuId": "21865"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_020_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186801750123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186801750123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186801750123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186801750123455"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_021_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800500123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800500123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800900123451",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800900123451",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218686",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218686",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800500123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800500123455"
                }, {
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186800900123451",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsSpec": "计重002",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186800900123451"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21868",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_022_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800300123457",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800300123457",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800500123455",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800500123455",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186800900123451",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186800900123451",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800500123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800500123455"
                }, {
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186800900123451",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsSpec": "计重002",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186800900123451"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21868",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_023_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800300123457",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800300123457",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800500123455",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800500123455",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/picked"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "0",
                            "goodsBarCode": "992186801000123457",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": pickingType,
                            "pluCode": "992186801000123457",
                            "realCount": "1",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": WAREHOUSE_ID,
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800500123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800500123455"
                }, {
                    "count": 1,
                    "pluCode": "992186801000123457"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                url = AFTERSALE_URL + "/pack/save"
                data = {
                    "batchId": self.batch_id,
                    "goodsBarcode": "992186801000123457",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsSpec": "计重002",
                    "packBoxBarcode": "P9099",
                    "pluOutputList": [{
                        "count": 1,
                        "pluCode": "992186801000123457"
                    }],
                    "pricingMethod": 391,
                    "realCount": "1",
                    "shopId": "0",
                    "shouldCount": "1",
                    "skuId": "21868",
                    "warehouseId": WAREHOUSE_ID,
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次商品打包' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    # 调用打包完成接口
                    url = AFTERSALE_URL + "/pack/complete"
                    data = {
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        # "timestamp": "1534760641698",
                        "storeId": "0",
                        "deviceID": "gaozuxin",
                        "batchId": self.batch_id
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次打包完成' + str(eval_data))
                    if eval_data["_msg"] == "操作成功":
                        self.batch_accept()  # 打包完成，自动调取揽件
                    else:
                        print("批次打包完成失败")
                else:
                    print("打包信息提交失败")
            else:
                print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/verification/confirm"
        data = {
            "storeOrderIdList": [store_id],
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] is None:
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            return res
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_024_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186801650123456",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186801650123456",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/lacking"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "1",
                        "goodsBarCode": "2110304218686",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "orderStoreId": orderStoreId,
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": "241",
                        "pluCode": "2110304218686",
                        "realCount": "0",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": "10056",
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186801650123456",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186801650123456"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": "10056",
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))

            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": "21868"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_025_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186801750123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186801750123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186801750123455",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186801750123455"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 434,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": "21868"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")


class Order_Batch_026_ZT:
    def __init__(self, empNo_pda, token_pda, empNo_ps, token_ps):
        self.empNo_pda = empNo_pda
        self.token_pda = token_pda
        self.empNo_ps = empNo_ps
        self.token_ps = token_ps
        self.batch_id = None

    def batch_picked(self):  # 获取拣货任务——拣货完成
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": self.empNo_pda
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次拣货任务' + str(eval_data))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(5)
                self.batch_picked()  # 没有获取到拣货任务，等待5S重新获取
            else:
                pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
                self.batch_id = pickingBatchId = _data["pickingBatchId"]
                cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
                pickingId = _data["items"][0]["pickingId"]
                pickingItemsId = _data["items"][0]["pickingItemsId"]
                orderStoreId = _data["items"][0]["orderStoreId"]
                # 拣货信息提交
                url = AFTERSALE_URL + "/picking/picked"
                uuid = int(time.time()) * 1000
                data = {
                    "cargospaceId": cargospaceId,
                    "contianerCode": "J9099",
                    "deferenceCount": "0",
                    "goodsBarCode": "992186800500123455",
                    "goodsId": "33644",
                    "goodsName": "ZDH实物生产加工计重002-自营",
                    "goodsProperty": "367",
                    "goodsSkuid": "21868",
                    "goodsType": "62",
                    "pickWay": 1,
                    "pickerId": self.empNo_pda,
                    "pickingBatchId": pickingBatchId,
                    "pickingId": pickingId,
                    "pickingItemsId": pickingItemsId,
                    "pickingType": pickingType,
                    "pluCode": "992186800500123455",
                    "realCount": "1",
                    "shouldCount": "1",
                    "uuid": str(uuid),
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    "storeId": "0",
                    "deviceID": "gaozuxin"
                }
                eval_data = my_request(url, data)
                my_log.debug('批次拣货数据' + str(eval_data))
                if str(eval_data["_data"]["finished"]) == "0":
                    url = AFTERSALE_URL + "/picking/picked"
                    data = {
                        "cargospaceId": cargospaceId,
                        "contianerCode": "J9099",
                        "deferenceCount": "0",
                        "goodsBarCode": "992186800900123451",
                        "goodsId": "33644",
                        "goodsName": "ZDH实物生产加工计重002-自营",
                        "goodsProperty": "367",
                        "goodsSkuid": "21868",
                        "goodsType": "62",
                        "pickWay": 1,
                        "pickerId": self.empNo_pda,
                        "pickingBatchId": pickingBatchId,
                        "pickingId": pickingId,
                        "pickingItemsId": pickingItemsId,
                        "pickingType": pickingType,
                        "pluCode": "992186800900123451",
                        "realCount": "1",
                        "shouldCount": "1",
                        "uuid": str(uuid),
                        "token": self.token_pda,
                        "memberId": self.empNo_pda,
                        "shopId": "0",
                        "warehouseId": WAREHOUSE_ID,
                        "isTestUser": 0,
                        "isDc": 0,
                        "platformType": 1587,
                        "storeId": "0",
                        "deviceID": "gaozuxin"
                    }
                    eval_data = my_request(url, data)
                    my_log.debug('批次拣货数据' + str(eval_data))
                    if str(eval_data["_data"]["finished"]) == "0":
                        url = AFTERSALE_URL + "/picking/lacking"
                        data = {
                            "cargospaceId": cargospaceId,
                            "contianerCode": "J9099",
                            "deferenceCount": "1",
                            "goodsBarCode": "2110304218686",
                            "goodsId": "33644",
                            "goodsName": "ZDH实物生产加工计重002-自营",
                            "goodsProperty": "367",
                            "goodsSkuid": "21868",
                            "goodsType": "62",
                            "orderStoreId": orderStoreId,
                            "pickWay": 1,
                            "pickerId": self.empNo_pda,
                            "pickingBatchId": pickingBatchId,
                            "pickingId": pickingId,
                            "pickingItemsId": pickingItemsId,
                            "pickingType": "241",
                            "pluCode": "2110304218686",
                            "realCount": "0",
                            "shouldCount": "1",
                            "uuid": str(uuid),
                            "token": self.token_pda,
                            "memberId": self.empNo_pda,
                            "shopId": "0",
                            "warehouseId": "10056",
                            "isTestUser": 0,
                            "isDc": 0,
                            "platformType": 1587,
                            "storeId": "0",
                            "deviceID": "gaozuxin"
                        }
                        eval_data = my_request(url, data)
                        my_log.debug('批次缺货数据' + str(eval_data))
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
        return self.batch_id

    def batch_pack(self):  # 批次打包
        url = AFTERSALE_URL + "/pack/topack"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "containerBarcode": "J9099"
        }
        eval_data = my_request(url, data)
        my_log.debug('获取批次待打包数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            self.batch_id = eval_data["_data"]["batchId"]
            url = AFTERSALE_URL + "/pack/save"
            data = {
                "batchId": self.batch_id,
                "goodsBarcode": "992186800900123451",
                "goodsId": "33644",
                "goodsName": "ZDH实物生产加工计重002-自营",
                "goodsSpec": "计重002",
                "packBoxBarcode": "P9099",
                "pluOutputList": [{
                    "count": 1,
                    "pluCode": "992186800900123451"
                }],
                "pricingMethod": 391,
                "realCount": "1",
                "shopId": "0",
                "shouldCount": "1",
                "skuId": "21868",
                "warehouseId": WAREHOUSE_ID,
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin"
            }
            eval_data = my_request(url, data)
            my_log.debug('批次商品打包' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                # 调用打包完成接口
                url = AFTERSALE_URL + "/pack/complete"
                data = {
                    "token": self.token_pda,
                    "memberId": self.empNo_pda,
                    "shopId": "0",
                    "warehouseId": WAREHOUSE_ID,
                    "isTestUser": 0,
                    "isDc": 0,
                    "platformType": 1587,
                    # "timestamp": "1534760641698",
                    "storeId": "0",
                    "deviceID": "gaozuxin",
                    "batchId": self.batch_id
                }
                eval_data = my_request(url, data)
                my_log.debug('批次打包完成' + str(eval_data))
                if eval_data["_msg"] == "操作成功":
                    self.batch_accept()  # 打包完成，自动调取揽件
                else:
                    print("批次打包完成失败")
            else:
                print("打包信息提交失败")
        else:
            print("获取打包信息失败")

    def batch_accept(self):  # 批次揽件
        url = AFTERSALE_URL + "/distribution/accept"
        data = {
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin",
            "batchId": self.batch_id,
            "scanFlag": "1"
        }
        eval_data = my_request(url, data)
        my_log.debug('自提批次揽件数据' + str(eval_data))
        if eval_data["_msg"] == "操作成功":
            url = AFTERSALE_URL + "/distribution/updateTakeYourself"
            data = {
                "token": self.token_pda,
                "memberId": self.empNo_pda,
                "shopId": "0",
                "warehouseId": WAREHOUSE_ID,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                "storeId": "0",
                "deviceID": "gaozuxin",
                "pickBatchId": self.batch_id,
            }
            eval_data = my_request(url, data)
            my_log.debug('自提批次接收数据' + str(eval_data))
            if eval_data["_msg"] == "操作成功":
                pass
            else:
                print("batch_data：" + str(self.batch_id) + "自提批次接收失败！" + eval_data["_msg"])
        else:
            print("batch_data：" + str(self.batch_id) + "自提批次揽件失败！" + eval_data["_msg"])

    def batch_delivery(self, order_id, store_id, id):  # 批次妥投
        url = AFTERSALE_URL + "/distribution/takeYourselfResult"
        data = {
            "distributeType": 435,
            "goodsList": [{
                "count": 1,
                "orderItemId": id,
                "skuId": "21868"
            }],
            "orderId": order_id,
            "orderStoreId": store_id,
            "remark": "无理由拒收",
            "token": self.token_pda,
            "memberId": self.empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            "storeId": "0",
            "deviceID": "gaozuxin"
        }
        eval_data = my_request(url, data)
        my_log.debug('订单核销数据' + str(eval_data))
        if eval_data["_code"] == "000000" and eval_data["_msg"] == "操作成功":
            my_log.debug("订单号：" + str(store_id) + "订单核销成功")
            # res = eval_data["_data"]["orderDTOList"][0]["shipmentStatus"]
            # return res
            return None
        else:
            print("订单号：" + str(store_id) + "订单核销失败")
