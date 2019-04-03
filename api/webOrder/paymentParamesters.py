import requests
from config import configFunction
from common import getSign

conf = configFunction.get_conf()

def alipayAppPaymentParamesters(host,uToken,orderCode):
    '''

    :param orderCode:
    :return:
    '''
    '''初始化'''
    url = host + conf["alipay_app_payment_paramesters"]

    '''传参'''
    p = {"orderCode":orderCode,"appId":"2016091901925114"}
    sign = getSign.getSign(uToken, params=p)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken": uToken}

    '''发送请求'''
    resp = requests.get(url=url, params=p, headers=h)
    r = resp.json()
    print(r["AppendData"])

    return r