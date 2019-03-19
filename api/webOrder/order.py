import json
import requests
from common import commonFunction
from config import configFunction

conf = configFunction.get_conf()

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

    sign = commonFunction.getSign(uToken, data=d)
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
        print("订单["+r["AppendData"]["OrderCode"]+"]提交成功，￥"+str(r["AppendData"]["AmountPayable"])+"，等待付款...")

    return r


def cancelOrder(uToken,studentCode,orderCode):
    '''
    取消订单
    :param uToken:
    :param studentCode:
    :param orderCode:
    :return:
    '''
    '''初始化数据'''
    url = conf["domain_test"] + conf["cancel_order"]

    '''传参'''
    d = {
        "StudentCode": studentCode,
        "OrderCode": orderCode,
    }

    sign = commonFunction.getSign(uToken, data=d)
    h = {"sign": sign, "partner": "10016", "Content-Type": "application/json;charset=utf-8", "uToken": uToken}

    '''发送请求'''
    resp = requests.post(url=url, data=json.dumps(d), headers=h)
    r = resp.json()

    '''取消后返回响应'''
    try:
        assert r["ResultType"] == 0
    except AssertionError:
        print("取消订单失败，错误类型:" + str(r["ResultType"]) + ",错误信息:" + r["Message"])
    else:
        print("订单[" + orderCode + "]取消成功")

    return r