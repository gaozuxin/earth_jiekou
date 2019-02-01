import json
import threading

import requests


def create_17918():
    url = "http://123.206.21.176/earth-api/order/create"
    data = {
        "orderStoreInfoList": [{
            "distributeType": 80,
            "goodsList": [{
                "goodsId": "18122",
                "goodsSkuId": "17918",
                "num": 5,
                "fareType": 0,
                "proId": 0,
                "proType": 0
            }],
            "shippingType": "110",
            "storeId": "97",
            "storeType": 62
        }],
        "cardValue": "150",
        "shopId": "10041",
        "payAmount": "150",
        "packAmount": "0",
        "shippingAmount": "50",
        "thirdPayAmount": "0",
        "payType": "497",
        "orderType": "0",
        "score": "0",
        "memberAddrId": "4711",
        "taxPrice": "0",
        "isException": "0",
        "token":  "ba1a5cb988d646098dc0030f6f7e1a66",
        "memberId": "1145",
        "channel": 218,
        "warehouseId": "10056",
        "centerShopId": "10000",
        "centerWarehouseId": "10034",
        "v": 1
    }
    r = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})  # 发送请求
    data_eval = json.loads(r.text)
    print(data_eval)


if __name__ == '__main__':
    threads = []
    for index in range(300):
        t1 = threading.Thread(target=create_17918)
        threads.append(t1)
    for t in threads:
        t.start()
