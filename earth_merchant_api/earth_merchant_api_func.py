import time

from earth_api.earth_api_func import get_member_code
from my_cnf.config_auto import MERCHANT_URL
from my_cnf.logging_auto import my_log
from my_func.my_request import my_request


# 闪电付待核销订单查询
def quickpayinfo(token_b, memberCode):
    url= MERCHANT_URL + '/verification/quickpayinfo'
    data = {
        "memberCode": memberCode,
        "autoPass": False,
        "checkDeviceNo": "729",
        "maxInterval": 60,
        "token": token_b,
        "userId": "729",
        "isTestUser": "0",
        "shopId": "10041",
        "storeId": "104"
    }
    data_eval = my_request(url, data)
    my_log.debug('闪电付待核销订单查询' + str(data_eval))
    return data_eval


# 闪电付订单核销
def quickpaycheck(token_b, orderId):
    url =MERCHANT_URL + '/verification/quickpaycheck'
    data  = {
        "checkDeviceNo": "729",
        "orderId": orderId,
        "orderStoreId": "",
        "memberId": "1145",
        "token": token_b,
        "userId": "729",
        "isTestUser": "0",
        "shopId": "10041",
        "storeId": "104"
    }
    data_eval = my_request(url, data)
    my_log.debug('闪电付订单核销' + str(data_eval))
    return data_eval['_data']['checkResult']


# 获取B端堂食待出餐订单
def order_list(token_b):
    timeStamp = time.time()
    timeArray = time.localtime(timeStamp)
    queryDate = time.strftime("%Y-%m-%d", timeArray)
    url = MERCHANT_URL + '/order/list'
    data ={
        "listType": "EAT",
        "orderStoreId": "",
        "page": "1",
        "queryDate": queryDate,
        "rows": "40",
        "token": token_b,
        "userId": "729",
        "isTestUser": "0",
        "shopId": "10041",
        "storeId": "104"
    }
    data_eval = my_request(url, data)
    my_log.debug('B端堂食待出餐订单' + str(data_eval))
    res ={
        "orderItemIdList": data_eval['_data']['orderDTOList'][0]['id'],
        "shippingType": data_eval['_data']['orderDTOList'][0]['shippingType'],
        "orderStoreId": data_eval['_data']['orderDTOList'][0]['orderItemDTOList'][0]['id']
    }
    return res


# B端确认出餐
def confirmMeal(token_b, res_data):
    url = MERCHANT_URL + '/order/confirmMeal'
    data = {
        "orderItemIdList": [res_data["orderStoreId"]],
        "orderStoreId": res_data["orderItemIdList"],
        "shippingType": res_data["shippingType"],
        "userName": "YZZY",
        "token": token_b,
        "userId": "729",
        "isTestUser": "0",
        "shopId": "10041",
        "storeId": "104"
    }
    data_eval = my_request(url, data)
    my_log.debug('B端确认出餐' + str(data_eval))
    return data_eval


# B端仅供堂食核销
def confirm(token_b, res_data):
    url = MERCHANT_URL + '/verification/confirm'
    data = {
        "listType": "EAT",
        "storeOrderIdList": [res_data["orderItemIdList"]],
        "orderItemIdList": [res_data["orderStoreId"]],
        "shippingType": res_data["shippingType"],
        "token": token_b,
        "userId": "729",
        "isTestUser": "0",
        "shopId": "10041",
        "storeId": "104"
    }
    data_eval = my_request(url, data)
    my_log.debug('B端仅供堂食核销' + str(data_eval))
    res = data_eval["_data"]["orderDTOList"][0]["shipmentStatus"]
    return res


if __name__=='__main__':
    # token_c = '8945904cb0a54000ab20cd651dd3eb8b'
    token_b = '6174acf11bb5494785470ec39a7458fc'
    listdata = order_list(token_b)
    confirmMeal(token_b, listdata)
