import requests, json


def my_request(url, data):
    r = requests.post(url=url, json=data, headers={"Content-Type": "application/json"})  # 发送请求
    data_eval = json.loads(r.text)  # 字符串转成字典类型
    return data_eval


if __name__ == '__main__':
    url = "https://cs.api.eartharbor.com/earth-api/valueCard/getValueCardShare"
    data = {
        "shareChannel": 220,
        "path": "/pages/myCard/bindCard/bindCard",
        "valueCardCode": "DQG1000052102",
        "memberId": 1145,
        "token": "X6d1eed96d11f452caa8eded231c81e00",
        "shopId": 10002,
        "centerShopId": 10000,
        "warehouseId": 10003,
        "centerWarehouseId": 10034,
        "sourceType": 220,
        "channel": 220,
        "rows": 40,
        "v": 2
    }

    data_eval = my_request(url, data)
    print(data_eval)
