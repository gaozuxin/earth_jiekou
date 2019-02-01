from my_cnf.config_auto import MERCHANT_URL, EARTHAPI_URL, AFTERSALE_URL
from my_func.my_request import my_request


def login_b():
    url = MERCHANT_URL + '/user/login'
    data = {
        "deviceCode": "",
        "deviceType": "1",
        "pwd": "p6C/0G6SroCAB7GRqBG+e5f0ULmN6d+YiLVs8s6WL+QUryTEPK1kLGpyjDvsEs0Tx6eNysxtwmboYW5ValmLMeKfcmnhkwKlWbPPKiuhpIbGiU+bmWPCTFXgvO9ryuzRsVJR293k3VcB1r3uZxkgQmGk/br4vmGID9l4wuzscIs=",
        "ua": "",
        "userName": "YZZY"
    }
    data_eval = my_request(url, data)
    res = data_eval['_data']['token']
    return res

def login_c():
    url = EARTHAPI_URL + '/member/login'
    data  = {
        "token": "",
        "memberId": "",
        "channel": "218",
        "shopId": "10041",
        "warehouseId": "10056",
        "centerShopId": "10000",
        "centerWarehouseId": "10034",
        "v": 2,
        "mobile": "16966662500",
        "pwd": "pxxJtko/3vbooB4HLCVUnBY8UWpsAJlPEaUYGLL0sgGIytOknP63D8/JvRCvMSU7iCQQSudt46yC6WDjBg7LiHFoutczfDC0HaMjNzRAflFX5nEBCyoFfX9gJP7CM5yNarEgDhfQYL+/BmvVgKWekF4h7jwRNVVoUPwCfQlKnsw=",
        "deviceCode": "AlZIy7Qw-3Nq9UFWN1XZTlwaROLeiOkl1dYB9imET4Gp",
        "deviceType": "1"
    }
    data_eval = my_request(url, data)
    res = data_eval['_data']['token']
    return res


def login_pda():
    url = AFTERSALE_URL + '/user/login'
    data  = {
        "token": "",
        "memberId": "334",
        "empNo": "334",
        "password": "123456",
        "shopId": "0",
        "warehouseId": "10056",
        "type": "1"
    }
    data_eval = my_request(url, data)
    res = data_eval['_data']['token']
    return res


def login_ps():
    url = AFTERSALE_URL + '/user/login'
    data = {
        "token": "",
        "memberId": "335",
        "empNo": "335",
        "password": "123456",
        "shopId": "0",
        "warehouseId": "10056",
        "type": "2"
    }
    data_eval = my_request(url, data)
    res = data_eval['_data']['token']
    return res


if __name__ == '__main__':
    token_b = login_b()
    token_c = login_c()
    token_pda = login_pda()
    token_ps = login_ps()
    print("token_pda:" + token_pda)
    print("token_ps:" + token_ps)
    print("token_b:" + token_b)
    print("token_c:" + token_c)