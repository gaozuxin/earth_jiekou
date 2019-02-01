import requests
import time

from my_cnf.config_auto import AFTERSALE_URL, WAREHOUSE_ID


def batch_17918(token_pda, empNo_pda):
    def get_batch_id():  # 自动获取拣货任务

        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": token_pda,
            "memberId": empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
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
                time.sleep(10)
                get_batch_id()#没有获取到拣货任务，等待10S重新获取
            else:
                data_processing(_data)
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
            global status,msg
            status = 0
            msg = "拣货任务获取失败"
            return 0
    def data_processing(_data):  # 批次数据处理
        pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
        pickingBatchId = _data["pickingBatchId"]
        cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
        pickingId = _data["items"][0]["pickingId"]
        pickingItemsId = _data["items"][0]["pickingItemsId"]
        batch_picked(cargospaceId,pickingItemsId,pickingBatchId, pickingId, pickingType)

    def batch_picked(cargospaceId,pickingItemsId,pickingBatchId, pickingId, pickingType):  # 提交拣货信息
        url = AFTERSALE_URL + "/picking/picked"
        uuid = int (time.time ()) * 1000
        data = {
            "cargospaceId": cargospaceId,
            "contianerCode": "J9099",
            "deferenceCount": "0",
            "goodsBarCode": 5800000009010,
            "goodsId": "18122",
            "goodsName": "GZX佛山照明10W",
            "goodsProperty": "367",
            "goodsSkuid": "17918",
            "goodsType": "62",
            "pickWay": 1,
            "pickerId":empNo_pda,
            "pickingBatchId": pickingBatchId,
            "pickingId": pickingId,
            "pickingItemsId": pickingItemsId,
            "pickingType": pickingType,
            "pluCode": "5800000009010",
            "realCount": "5",
            "shouldCount": "5",
            "uuid": str(uuid),
            "token": token_pda,
            "memberId": empNo_pda,
            "shopId": "0",
            "warehouseId": "10056",
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            # "timestamp": "1534745014603",
            "storeId": "0",
            # "deviceID": "72a3985b"
            }
        r = requests.post (url=url, json=data, headers={"Content-Type": "application/json"})  # 发送请求
        eval_data = eval(r.text.replace ("null", "None"))
        print(eval_data)
        if str(eval_data["_code"]) == "000000":

            if str((eval_data["_data"]["finished"])) == "1":
                global status, msg
                status = 1
                msg = eval_data["_msg"]
            else:
                status = 0
                msg = "拣货未完成"#判断可能不够严谨
        else:
            status = 0
            msg = eval_data["_msg"]
    get_batch_id()
    res = {
        "status": status,
        "msg": msg
    }
    return res

def batch_17918(token_pda, empNo_pda):
    def get_batch_id():  # 自动获取拣货任务

        url = AFTERSALE_URL + "/picking/assignment/O2O"
        data = {
            "token": token_pda,
            "memberId": empNo_pda,
            "shopId": "0",
            "warehouseId": WAREHOUSE_ID,
            "isTestUser": 0,
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
                time.sleep(10)
                get_batch_id()#没有获取到拣货任务，等待10S重新获取
            else:
                data_processing(_data)
        else:
            print("batch_data：获取拣货任务失败:" + eval_data["_msg"])
            global status,msg
            status = 0
            msg = "拣货任务获取失败"
            return 0
    def data_processing(_data):  # 批次数据处理
        pickingType = str(_data["pickingType"])  # 拣货类型 240：前仓拣货， 241：后仓拣货， 1：快速打包
        pickingBatchId = _data["pickingBatchId"]
        cargospaceId = _data["items"][0]["suggestCargos"][0]["cargospaceId"]
        pickingId = _data["items"][0]["pickingId"]
        pickingItemsId = _data["items"][0]["pickingItemsId"]
        batch_picked(cargospaceId,pickingItemsId,pickingBatchId, pickingId, pickingType)

    def batch_picked(cargospaceId,pickingItemsId,pickingBatchId, pickingId, pickingType):  # 提交拣货信息
        url = AFTERSALE_URL + "/picking/picked"
        uuid = int (time.time ()) * 1000
        data = {
            "cargospaceId": cargospaceId,
            "contianerCode": "J9099",
            "deferenceCount": "0",
            "goodsBarCode": 5800000009010,
            "goodsId": "18122",
            "goodsName": "GZX佛山照明10W",
            "goodsProperty": "367",
            "goodsSkuid": "17918",
            "goodsType": "62",
            "pickWay": 1,
            "pickerId":empNo_pda,
            "pickingBatchId": pickingBatchId,
            "pickingId": pickingId,
            "pickingItemsId": pickingItemsId,
            "pickingType": pickingType,
            "pluCode": "5800000009010",
            "realCount": "5",
            "shouldCount": "5",
            "uuid": str(uuid),
            "token": token_pda,
            "memberId": empNo_pda,
            "shopId": "0",
            "warehouseId": "10056",
            "isTestUser": 0,
            "isDc": 0,
            "platformType": 1587,
            # "timestamp": "1534745014603",
            "storeId": "0",
            # "deviceID": "72a3985b"
            }
        r = requests.post (url=url, json=data, headers={"Content-Type": "application/json"})  # 发送请求
        eval_data = eval(r.text.replace ("null", "None"))
        print(eval_data)
        if str(eval_data["_code"]) == "000000":

            if str((eval_data["_data"]["finished"])) == "1":
                global status, msg
                status = 1
                msg = eval_data["_msg"]
            else:
                status = 0
                msg = "拣货未完成"#判断可能不够严谨
        else:
            status = 0
            msg = eval_data["_msg"]
    get_batch_id()
    res = {
        "status": status,
        "msg": msg
    }
    return res