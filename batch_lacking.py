import requests
import time

from my_cnf.config_auto import AFTERSALE_URL


def earth_pack(token_pda, empNo_pda):
    def get_batch_id():  # 自动获取拣货任务
        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": token_pda,
            "memberId": empNo_pda,
            "shopId": "0",
            "warehouseId": warehouse_id,
            "isTestUser": 1,
            "isDc": 0,
            "assignmentType": "O2O拣货",
            "pickerId": empNo_pda
        }
        r = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})  # 发送请求
        eval_data = eval(r.text.replace("null", "None"))
        _data = eval_data["_data"]
        if eval_data["_msg"] == "操作成功":
            if eval_data["_data"] is None:
                print("batch_data：当前没有O2O拣货任务!")
                time.sleep(20)
                return 1
            else:
                data_processing(_data)
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
            return 0

    def data_processing(_data):  # 批次数据处理
        pickingType = _data["pickingType"]  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
        pickingBatchId = _data["pickingBatchId"]
        if pickingBatchId == 188493:
            exit()
        n = len(_data["items"])  # 拣货任务子项个数
        for i in range(n):
            cargospaceId = _data["items"][i]["suggestCargos"][0]["cargospaceId"]
            goodsBarcode = _data["items"][i]["goodsBarcode"]
            goodsProperty = _data["items"][i]["goodsProperty"]
            pickingId = _data["items"][i]["pickingId"]
            goodsId = _data["items"][i]["goodsId"]
            goodsName = _data["items"][i]["goodsName"]
            goodsSku = _data["items"][i]["goodsSku"]
            shouldCount = _data["items"][i]["shouldCount"]
            # lockedStockValue = _data["items"][i]["lockedStockValue"]  # 商品锁定库存
            goodsType = _data["items"][i]["goodsType"]
            sellWay = _data["items"][i]["sellWay"]  # 商铺经营类型:60-自营, 61-联营
            pickWay = _data["items"][i]["pickWay"]  # 拣货方式：1-按商品(标品),2-按订单(餐食)
            pricingMethod = _data["items"][i]["pricingMethod"]  # 计价方式:390计数 391 计重
            if pickWay == 1:  # 1-按商品(标品)
                pickingItemsIds = _data["items"][i]["pickingItemsId"]
                orderStoreId = _data["items"][i]["orderStoreId"]
            elif pickWay == 2:  # 2-按订单(餐食)
                orderStoreId = _data["items"][i]["orderStoreId"]
                pickingItemsIds = _data["items"][i]["pickingItemsId"]
                orderItemList = _data["items"][i]["orderItemList"]
            if i == n - 1:  # 批次拣货子任务最后一个商品
                finished_status = 1  # 整个拣货任务是否完成(1完成，0未完成)
            else:
                finished_status = 0
            lacking(cargospaceId, goodsBarcode, shouldCount, orderStoreId, goodsId, goodsName, goodsProperty, goodsSku,
                    goodsType, pickWay, pickingBatchId, pickingId, pickingItemsIds, pickingType, finished_status)

    def lacking(cargospaceId, goodsBarcode, shouldCount, orderStoreId, goodsId, goodsName, goodsProperty, goodsSku,
                goodsType, pickWay, pickingBatchId, pickingId, pickingItemsIds, pickingType, finished_status):
        url = AFTERSALE_URL + "/picking/lacking"
        uuid = int(time.time()) * 1000
        data = {
                "contianerCode":"JL999",
                "cargospaceId": cargospaceId,
                "deferenceCount": shouldCount,
                "finished": finished_status,
                "goodsBarCode": goodsBarcode,
                "orderStoreId": orderStoreId,
                "goodsId": goodsId,
                "goodsName": goodsName,
                "goodsProperty": goodsProperty,
                "goodsSkuid": goodsSku,
                "goodsType": goodsType,
                "pickWay": pickWay,
                "pickerId": empNo_pda,
                "pickingBatchId": pickingBatchId,
                "pickingId": pickingId,
                "pickingItemsId": pickingItemsIds,
                "pickingType": pickingType,
                "pluCode": goodsBarcode,
                "realCount": "0",
                "shouldCount": shouldCount,
                "uuid": uuid,
                "token": token_pda,
                "memberId": empNo_pda,
                "shopId": "0",
                "warehouseId": warehouse_id,
                "isTestUser": 0,
                "isDc": 0,
                "platformType": 1587,
                # "timestamp": "1522399442746",
                "storeId": "0"
            }
        r = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})  # 发送请求
        # eval_data = eval(r.text.replace("null", "None"))
        # _data = eval_data["_data"]
        print("批次" + str(pickingBatchId) + r.text)

    get_batch_id()


if __name__ == '__main__':
    warehouse_id = "10003"
    empNo_pda = "6"
    get_token ="791677cedea1452ca451e4dcb3de9d3b"
    while(1):
        earth_pack(get_token, empNo_pda)