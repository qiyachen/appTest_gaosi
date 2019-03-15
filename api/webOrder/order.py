import json
import requests
from common import commonAction
from config import configAction

conf = configAction.get_conf()

def placeOrder(uToken,studentCode,goldCoinAmount,accountBalanceAmount,items):
    """
    提交订单，并返回订单编号和应付金额
    :param uToken:
    :param studentCode:
    :param goldCoinAmount: 高思币
    :param accountBalanceAmount: 余额
    :param items: 课程信息
    :return:
    """

    '''初始化数据'''
    url = conf["domain_test"] + conf["place_order"]

    '''传参'''
    d = {
        "StudentCode": studentCode,
        "Channel": 6,
        "Items": items,
        "GoldCoinAmount":goldCoinAmount,
        "AccountBalanceAmount":accountBalanceAmount
    }

    sign = commonAction.getSign(uToken, data=d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken": uToken}

    '''发送请求'''
    resp = requests.post(url=url, data=json.dumps(d), headers=h)
    r = resp.json()

    '''提交后返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("提交订单失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print(r["AppendData"]["OrderCode"]+"订单提交成功，￥"+r["AppendData"]["AmountPayable"]+"，等待付款...")
