from my_cnf.config_auto import EARTHAPI_URL
from my_func.my_request import my_request


# 获取会员码
def get_member_code(token_c):
    url =EARTHAPI_URL + '/member/createexclusivecode'
    data = {
        "token": token_c,
        "memberId": "1145",
        "channel": 218,
        "shopId": "10041",
        "warehouseId": "10056",
        "centerShopId": "10000",
        "centerWarehouseId": "10034",
        "v": 2,
        "exclusiveCodeType": "797"
    }
    data_eval = my_request(url, data)
    res = data_eval['_data']['exclusiveCode']
    return res


if __name__ == "__main__":
    token_c ='3b672d272d2b412aa245662579af00db'
    data_eval = get_member_code(token_c)
    print(data_eval)